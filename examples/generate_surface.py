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

from povray import *

d = 3
radius = 0.5
spheres1 = Union([Sphere(np.random.random(d), radius) for i in range(d)])
print(spheres1)
spheres2 = Union(*[Sphere(np.random.random(d), radius) for i in range(d)])
print(spheres2)
print(Merge(spheres1, spheres2))

print(Macro('abc', Sphere(np.random.random(d), 'radius'), arguments=['radius']))
print(Declare('abc', Sphere(np.random.random(d), radius)))

N = 25
x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)
Z = X*(1-X) * Y*(1-Y)

coordinates, triangles = triangulate_grid(X, Y, Z)
print(Mesh2(coordinates, triangles))
