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
from scipy import interpolate
from .primitives import *

def stipple_coordinates(coordinates, resolutions=None, exclude_out_of_bounds=False, eps=1e-12):
    if resolutions is None: return coordinates
    ds = np.linalg.norm(np.diff(coordinates, axis=0), axis=1)
    path_lengths = np.concatenate(([0], np.cumsum(ds, axis=0)))
    f = interpolate.interp1d(path_lengths, coordinates.T)

    stencil_size = np.sum(resolutions)
    stencil = np.cumsum(resolutions)
    sample_points = np.arange(0, path_lengths[-1], stencil_size)
    sample_points = (np.tile(sample_points.reshape(-1,1), len(stencil)) + stencil).reshape(-1)

    out_of_bounds = sample_points > path_lengths[-1]
    if exclude_out_of_bounds:
        sample_points = sample_points[~out_of_bounds]
    else:
        sample_points[out_of_bounds] = path_lengths[-1]
        sample_points = sample_points[:1+np.where(out_of_bounds)[0][0]]

    return f(sample_points).T

def line(coordinates, line_width, *args, stipple=None, smooth=True, **kwargs):
    """Generates a line in 3d as the union of cylinders that can be rendered with ray-tracing."""

    objects = []

    if stipple is not None:
        coordinates = stipple_coordinates(coordinates, stipple)
        for coords in zip(coordinates[::2], coordinates[1::2]):
            objects += [child for child in line(coords, line_width, *args, smooth=False, **kwargs).children]

    else:

        # Create the line as a series of cylinders joining adjacent points.
        for v1, v2 in zip(coordinates, coordinates[1:]):
            if np.linalg.norm(v2 - v1) > 0:
                objects += [Cylinder(pov_vector(v1), pov_vector(v2), line_width)]

    if smooth:
        # Round the edges of the cylinders where the lines join to make it smooth.
        for v in np.unique(coordinates, axis=0):
            objects += [Sphere(pov_vector(v), line_width)]

    return Merge(*objects, *args, **kwargs)

def arrowed_line(coordinates, line_width, arrow_separation, arrow_length, arrow_width, *args, smooth=True, reverse=False, **kwargs):
    """Generates a line containing arrows in 3d as the union of cylinders and cones
    that can be rendered with ray-tracing."""

    objects = []

    # Create the line as a series of cylinders joining adjacent points.
    for v1, v2 in zip(coordinates, coordinates[1:]):
        if np.linalg.norm(v2 - v1) > 0:
            objects += [Cylinder(pov_vector(v1), pov_vector(v2), line_width)]

    arrow_coords = stipple_coordinates(coordinates, (arrow_separation, arrow_length), exclude_out_of_bounds=True)
    for a, b in zip(arrow_coords[::2], arrow_coords[1::2]):
        if reverse: a, b = b, a
        objects += [Cone(a, b, arrow_width, 0)]

    return Merge(*objects, *args, **kwargs)
