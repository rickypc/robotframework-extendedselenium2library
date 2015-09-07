#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Extended Selenium2 Library - a web testing library with AngularJS support.
#    Copyright (C) 2015  Richard Huang <rickypc@users.noreply.github.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Extended Selenium2 Library - a web testing library with AngularJS support.
"""


def inherit_docs(cls):
    """Inherits method docstring from parent method."""
    for name, func in list(vars(cls).items()):
        if not func.__doc__:
            for parent in cls.__bases__:
                parent_func = getattr(parent, name, None)
                if parent_func and getattr(parent_func, '__doc__', None):
                    func.__doc__ = parent_func.__doc__
                    break
    return cls
