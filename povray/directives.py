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

from .primitives import Primitive

class Macro(Primitive):
    def __init__(self, name, *args, arguments=[], **kwargs):
        self.name = name
        self.arguments = arguments
        super().__init__(*args, **kwargs)

    @property
    def header(self):
        return '#{directive} {name}({arguments})'.format(directive=super().header, name=self.name,
                                                         arguments=','.join(self.arguments))

    @property
    def body_open(self):
        return ''

    @property
    def body_close(self):
        return '#end'

class Version(Primitive):
    def __init__(self, version, *args, **kwargs):
        self.version = version
        super().__init__(*args, **kwargs)

    @property
    def header(self):
        return '#{}'.format(super().header)

    @property
    def body_open(self):
        return ' '

    @property
    def body(self):
        return '{}'.format(self.version)

    @property
    def body_close(self):
        return ';'

class Include(Primitive):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super().__init__(*args, **kwargs)

    @property
    def header(self):
        return '#{}'.format(super().header)

    @property
    def body_open(self):
        return ' "'

    @property
    def body(self):
        return '{}'.format(self.path)

    @property
    def body_close(self):
        return '"'

class Declare(Primitive):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.arguments = []
        super().__init__(*args, **kwargs)

    @property
    def header(self):
        return '#{directive} {name}'.format(directive=super().header, name=self.name)

    @property
    def body_open(self):
        return ' = '

    @property
    def body_close(self):
        return ';'

def Local(Declare): pass
