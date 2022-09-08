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
from scipy.spatial.distance import pdist, squareform

from .primitives import *
from .directives import *
from .pigments import *
from .lines import *
from .scene import *

default_epsilon = 1e-12
default_diameter = 1
default_bond_threshold = default_diameter + default_epsilon

def ball_and_stick(coordinates, ball_radius, stick_radius, bonds=None, bond_threshold=default_bond_threshold):
    n, d = coordinates.shape

    balls = Merge()
    for x in coordinates:
        balls += [Sphere(x, ball_radius)]

    if bonds is None:
        bonds = squareform(pdist(coordinates) < bond_threshold)

    if not bonds.any():
        raise RuntimeError('no bonds found between particles!')

    sticks = Merge()
    for i in range(len(coordinates)):
        x1 = coordinates[i]
        for j in range(i+1, len(coordinates)):
            if bonds[i, j]:
                x2 = coordinates[j]
                sticks += line([x1, x2], stick_radius)

    return Union(balls, sticks)

def scene(coordinates, ball_radius=0.5, stick_radius=0.05,
          perspective=True, camera_distance=4,
          ball_colour='White', ball_alpha=0.8, stick_colour='Yellow',
          **kwargs):

    n, d = coordinates.shape
    assert d == 3

    max_distance = np.max(np.linalg.norm(coordinates, axis=1))
    camera_position = np.random.random(d)
    camera_position /= np.linalg.norm(camera_position)
    camera_position *= camera_distance*max_distance

    focus_position = np.zeros(d)

    camera_position_reference = 'cameraPos'
    focus_position_reference = 'focusPos'
    ball_pigment = Pigment( Colour(ball_colour), Transmit(ball_alpha) )
    stick_pigment = Pigment( Colour(stick_colour) )

    ball_finish_name = 'ballFinish'
    ball_finish_definition = Finish( Ambient(0.1), Diffuse(0.6), Phong(0.1), PhongSize(40),
                                     Reflection(value=0.1) )
    ball_finish_reference = Finish(value=ball_finish_name)

    stick_finish_name = 'stickFinish'
    stick_finish_definition = Finish( Ambient(0.1), Diffuse(0.8), Phong(0.1), PhongSize(40) )
    stick_finish_reference = Finish(value=stick_finish_name)

    balls, sticks = ball_and_stick(coordinates, ball_radius, stick_radius, **kwargs)
    balls += [ball_pigment, ball_finish_reference]
    sticks += [stick_pigment, stick_finish_reference]

    right_direction = np.eye(1,d,0).reshape(-1)
    up_direction = np.eye(1,d,1).reshape(-1)
    if perspective:
        projection = Perspective()
    else:
        dimensions = np.max(coordinates, axis=1) - np.min(coordinates, axis=1)
        rescale = camera_distance*np.max(dimensions)
        right_direction *= rescale
        up_direction *= rescale
        projection = Orthographic()

    #sky_direction = np.eye(1,d,d-1).reshape(-1)
    sky_direction = np.random.random(d)
    sky_direction /= np.linalg.norm(sky_direction)

    camera = Camera(projection, Location(camera_position_reference),
                    LookAt(focus_position_reference),
                    Sky(pov_vector(sky_direction)),
                    Right(pov_vector(right_direction)),
                    Up(pov_vector(up_direction)))
    light = LightSource(camera_position_reference, Colour('White'),
                        Parallel(),
                        PointAt(focus_position_reference),
                        Shadowless())

    scene = Scene()
    scene += [Declare(ball_finish_name, ball_finish_definition),
              Declare(stick_finish_name, stick_finish_definition),
              Declare(camera_position_reference, value=pov_vector(camera_position)),
              Declare(focus_position_reference, value=pov_vector(focus_position)),
              camera, light, balls, sticks]
    return scene
