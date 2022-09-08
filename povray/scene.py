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

from .primitives import *
from .directives import *

class GlobalSettings(Primitive): pass
class AssumedGamma(Attribute): pass
class MaxTraceLevel(Attribute): pass
class AmbientLight(Attribute): pass

class Camera(Primitive): pass
class Perspective(Flag): pass
class Orthographic(Flag): pass
class Location(Attribute): pass
class LookAt(Attribute): pass
class Sky(Attribute): pass
class Right(Attribute): pass
class Up(Attribute): pass

class LightSource(Primitive):
    def __init__(self, light_position, *args, **kwargs):
        super().__init__(*args, value=light_position, **kwargs)
class Parallel(Flag): pass
class Shadowless(Flag): pass
class PointAt(Attribute): pass

class Scene(Primitive):
    def __init__(self,
                 version=3.7, assumed_gamma=2.2, max_trace_level=256, ambient_light='White'):
        super().__init__()
        self += [Version(version),
                 Include('shapes.inc'),
                 Include('colors.inc'),
                 GlobalSettings( AssumedGamma(assumed_gamma),
                                 MaxTraceLevel(max_trace_level),
                                 AmbientLight(ambient_light) )]

    @property
    def header(self):
        return ''

    @property
    def body_open(self):
        return ''

    @property
    def body_close(self):
        return ''

    @property
    def indent(self):
        return ''

    @property
    def start_nest(self):
        return -1
