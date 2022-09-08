#!/usr/bin/env python3

# Copyright (C) 2022 Joshua Robinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from .syntax import pov_vector
from .primitives import Primitive, Attribute

def triangulate_grid(*args):
    """Triangulate a 2d grid of coordinates to obtain a triangle mesh.

    This only works on gridded coordinates because they can be easily
    turned into quadstrips.

    Args:
        Meshgrid coordinates (e.g. from output of numpy.meshgrid).
    Returns:
        coordinates: vertex coordinates referenced by triangulation.
        triangulation: (n x 3) int array giving vertex indices for each triangle.
    """
    nrows, ncols = args[0].shape
    triangles_per_strip = 2*(ncols - 1)
    nstrips = nrows - 1
    ntriangles = nstrips * triangles_per_strip

    triangulation = np.empty((ntriangles, 3), dtype=int)
    # Two basic triangles in a strip:
    triangulation[::2] = [0, ncols, 1]
    triangulation[1::2] = [1, ncols, ncols+1]
    # Shift vertex indices along the appropriate number of columns within a strip.
    triangulation += np.tile(np.repeat(np.arange(ncols - 1), 2), nstrips)[:, np.newaxis]
    # Shift vertex indices along the rows to get the correct indices for each strip.
    triangulation += np.repeat(ncols*np.arange(nstrips), triangles_per_strip)[:,np.newaxis]

    coordinates = np.array([x.flatten() for x in args]).T
    return coordinates, triangulation

def grid_lines(*args):
    """Coordinates of lines along a 2d grid of coordinates to obtain the grid lines.

    Args:
        Meshgrid coordinates (e.g. from output of numpy.meshgrid).
    Returns:
        xcoords: sequence of coordinates for first set of grid lines.
        ycoords: sequence of coordinates for second set of grid lines.
    """

    nrows, ncols = args[0].shape

    xcoords, ycoords = [], []
    for row in range(nrows): xcoords += [np.array([x[row] for x in args]).T]
    for col in range(ncols): ycoords += [np.array([x[:,col] for x in args]).T]
    return xcoords, ycoords

class VectorBundle(Primitive):
    def __init__(self, coordinates, *args, **kwargs):
        self.coordinates = coordinates
        self.vectors = [pov_vector(x) for x in self.coordinates]
        super().__init__(*args, **kwargs)

    @property
    def body(self):
        return '{}, {}'.format(len(self.vectors), ', '.join(self.vectors))

class VertexVectors(VectorBundle): pass
class NormalVectors(VectorBundle): pass
class FaceIndices(VectorBundle): pass
class InsideVector(Attribute): pass

class Mesh2(Primitive):
    """Generates a povray "mesh2" object ready to be rendered with ray-tracing."""

    def __init__(self, coordinates, triangulation, *args, inside_vector=None, **kwargs):
        """Create the mesh from raw data.

        Args:
            coordinates: vertex coordinates.
            triangulation: vertex indices.
            inside_vector: vector direction to cast rays in order to determine interior.
        """
        triangulation = np.atleast_2d(triangulation)
        ntriangles, d = triangulation.shape
        assert d == 3

        coordinates = np.array(coordinates).reshape(-1,d)
        A, B, C = coordinates[triangulation.T]
        self.face_normals = np.cross(B - A, C - A)
        vertex_normals = np.zeros(coordinates.shape)

        for vertices in triangulation.T:
            vertex_normals[vertices] += self.face_normals

        vertex_normals = (vertex_normals.T / np.linalg.norm(vertex_normals, axis=1)).T

        super().__init__(*args, **kwargs)
        self.vertex_vectors = VertexVectors(coordinates)
        self.normal_vectors = NormalVectors(vertex_normals)
        self.face_indices = FaceIndices(triangulation)
        self.children += [self.vertex_vectors, self.normal_vectors, self.face_indices]

        if inside_vector is not None:
            self.inside_vector = InsideVector(pov_vector(inside_vector))
            self.children += [self.inside_vector]
