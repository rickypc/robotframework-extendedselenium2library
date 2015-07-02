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

from robot.utils import NormalizedDict
from Selenium2Library.locators import ElementFinder


class ExtendedElementFinder(ElementFinder):

    def __init__(self):
        ElementFinder.__init__(self)
        strategies = {
            'model': self._find_by_ng_model
        }
        self._strategies.update(strategies)
        self._default_strategies =  self._strategies.keys()
        self._ng_prefixes = ['ng-','data-ng-','ng_','x-ng-','ng\\:']

    def _find_by_ng_model(self, browser, model_name, tag, constraints):
        stem = 'model="%s"' % model_name
        joiner = '%s],[' % stem
        criteria = '[' + joiner.join(self._ng_prefixes) + stem + ']'
        return self._find_by_css_selector(browser, criteria, tag, constraints)
