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

import sys
import io

from .syntax import *

class Primitive:
    def __init__(self, *args, single_line=False, **kwargs):
        self.single_line = single_line
        self.children = []
        for arg in args:
            try: self.children += arg
            except: self.children += [arg]
        self.children = list(chain(self.children)) # flatten list of lists

    @property
    def header(self):
        return to_snake_case(self.__class__.__name__)

    @property
    def body_open(self):
        return '{'

    @property
    def body_close(self):
        return '}'

    @property
    def body(self):
        raise NotImplementedError

    def write(self, f=sys.stdout, nest=0):
        """Generate the povray script.

        Args:
            f: filestream to output to.
        """

        indent = '  ' * nest
        f.write('{}{}'.format(indent, self.header))

        if len(self.children):
            if len(self.body_open): f.write('\n{}{}'.format(indent, self.body_open))
            for child in self.children:
                f.write('\n')
                child.write(f, nest+1)
            f.write('\n{}{}'.format(indent, self.body_close))

        else:
            f.write(' {} {} {}'.format(self.body_open, self.body, self.body_close))

    def __repr__(self):
        f = io.StringIO()
        self.write(f)
        return f.getvalue()

class Attribute(Primitive):
    """Simple one line key-value attribute."""

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    @property
    def body_open(self):
        return ''

    @property
    def body(self):
        return '{}'.format(self.value)

    @property
    def body_close(self):
        return ''

# Basic combinations of objects:
class Union(Primitive): pass
class Merge(Primitive): pass
class Intersection(Primitive): pass
class Difference(Primitive): pass

class Sphere(Primitive):
    def __init__(self, position, radius, *args, **kwargs):
        self.position = pov_vector(position)
        self.radius = str(radius)
        super().__init__(*args, **kwargs)

    @property
    def body(self):
        return '{}, {}'.format(self.position, self.radius)

class Cylinder(Primitive):
    def __init__(self, position1, position2, radius, *args, **kwargs):
        self.position1 = pov_vector(position1)
        self.position2 = pov_vector(position2)
        self.radius = str(radius)
        super().__init__(*args, **kwargs)

    @property
    def body(self):
        return '{}, {}, {}'.format(self.position1, self.position2, self.radius)
