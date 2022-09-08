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

import re
from itertools import chain

def pov_vector(v):
    """Convert numpy vector into form parseable by povray.

    Args:
        v: numpy array.
    Returns:
        String representation of vector ready for povray.
    """
    if type(v) is str: return v
    else: return str(v.tolist()).replace('[', '<').replace(']', '>')

def to_snake_case(s):
    """Convert PascalCase or camelCase (AKA mixedCase in PEP 8) string to snake_case.

    snake_case is the povray object type naming convention, whereas we make use of PascalCase for
    class definitions. We can scrape the class names and convert to snake_case to create
    a 1:1 correspondence between python class and povray objects.

    >>> to_snake_case('myStringInitiallyInCamelCase')
    'my_string_initially_in_camel_case'

    Args:
        s: string in PascalCase or camelCase.
    Returns:
        String in snake_case.
    """

    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z])', '_', s).lower()
