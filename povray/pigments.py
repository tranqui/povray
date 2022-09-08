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

from .primitives import Primitive, Attribute

class Pigment(Primitive): pass
class Colour(Attribute): pass
class Transmit(Attribute): pass

class Finish(Primitive): pass
class Ambient(Attribute): pass
class Diffuse(Attribute): pass
class Specular(Attribute): pass
class Roughness(Attribute): pass
class Reflection(Primitive): pass
class Phong(Attribute): pass
class PhongSize(Attribute): pass

class Interior(Primitive): pass
class Ior(Attribute): pass
