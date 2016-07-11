#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Extended Selenium2 Library - a web testing library with AngularJS support.
#    Copyright (c) 2015, 2016 Richard Huang <rickypc@users.noreply.github.com>
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

from sys import path
path.append('src')
import unittest
import mock
from ExtendedSelenium2Library.locators import ExtendedElementFinder
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.locators import ElementFinder


class ExtendedElementFinderTests(unittest.TestCase):
    """Extended element finder keyword test class."""

    def setUp(self):
        """Instantiate the extended element finder class."""
        self.default_strategies = ['binding', 'button', 'css', 'default', 'dom',
                                   'id', 'identifier', 'jquery', 'link', 'model',
                                   'name', 'options', 'partial binding',
                                   'partial button', 'partial link', 'scLocator',
                                   'sizzle', 'tag', 'xpath']
        self.driver = mock.Mock()
        self.driver.session_id = 'session'
        self.finder = ExtendedElementFinder()
        self.finder._filter_elements = mock.Mock()
        self.finder._find_by_css_selector = mock.Mock()
        self.finder.BUTTON_TEXT_WRAPPER = 'return buttons;%(handler)s'
        self.finder.NG_BINDING_WRAPPER = 'return bindings;%(handler)s'
        self.ng_prefixes = ['ng-', 'data-ng-', 'ng_', 'x-ng-', 'ng\\:']
        self.web_element = WebElement(self.driver, 'element', False)
        self.finder._filter_elements.return_value = self.web_element
        self.finder._find_by_css_selector.return_value = self.web_element

    def test_should_inherit_finder(self):
        """Extended element finder instance should inherit Selenium2 element finder instances."""
        self.assertIsInstance(self.finder, ElementFinder)

    def test_should_inherit_attributes(self):
        """Extended element finder instance should inherit its parent attributes."""
        self.assertEqual(self.finder._default_strategies, self.default_strategies)
        self.assertEqual(self.finder._ng_prefixes, self.ng_prefixes)

    def test_should_find_by_button_text(self):
        """Should find by button text."""
        button_text = 'a-button'
        constrains = 'constrains'
        script = "return buttons;return text.replace(/^\s+|\s+$/g,'')==='%s'" % \
                 button_text
        tag = 'tag'
        self.finder._find_by_button_text(self.driver, button_text, tag, constrains)
        self.driver.execute_script.assert_called_with(script)
        self.finder._filter_elements.assert_called_with(self.driver.execute_script.return_value,
                                                        tag, constrains)

    def test_should_find_by_button_text_partial(self):
        """Should find by button partial text."""
        button_text = 'a-button'
        constrains = 'constrains'
        script = "return buttons;return text.indexOf('%s')>-1" % \
                 button_text
        tag = 'tag'
        self.finder._find_by_button_text_partial(self.driver, button_text, tag, constrains)
        self.driver.execute_script.assert_called_with(script)
        self.finder._filter_elements.assert_called_with(self.driver.execute_script.return_value,
                                                        tag, constrains)

    def test_should_find_by_ng_binding(self):
        """Should find by exact binding name."""
        binding_name = 'a-binding'
        constrains = 'constrains'
        script = ("return bindings;var matcher=new RegExp('({|\\s|^|\\|)'+'%s'."
                  "replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g,'\\$&')"
                  "+'(}|\\s|$|\\|)');return matcher.test(name)") % \
                  binding_name
        tag = 'tag'
        self.finder._find_by_ng_binding(self.driver, binding_name, tag, constrains)
        self.driver.execute_script.assert_called_with(script)
        self.finder._filter_elements.assert_called_with(self.driver.execute_script.return_value,
                                                        tag, constrains)

    def test_should_find_by_ng_binding_partial(self):
        """Should find by partial binding name."""
        binding_name = 'a-binding'
        constrains = 'constrains'
        script = "return bindings;return name.indexOf('%s')>-1" % \
                 binding_name
        tag = 'tag'
        self.finder._find_by_ng_binding_partial(self.driver, binding_name, tag, constrains)
        self.driver.execute_script.assert_called_with(script)
        self.finder._filter_elements.assert_called_with(self.driver.execute_script.return_value,
                                                        tag, constrains)

    def test_should_find_by_ng_model(self):
        """Should find by exact model name."""
        constrains = 'constrains'
        model_name = 'a-model'
        stem = 'model="%s"' % model_name
        joiner = '%s],[' % stem
        criteria = '[' + joiner.join(self.ng_prefixes) + stem + ']'
        tag = 'tag'
        self.finder._find_by_ng_model(self.driver, model_name, tag, constrains)
        self.finder._find_by_css_selector.assert_called_with(self.driver,
                                                             criteria, tag,
                                                             constrains)

    def test_should_find_by_ng_options(self):
        """Should find by exact descriptor."""
        constrains = 'constrains'
        descriptor = 'an-options'
        stem = 'options="%s"' % descriptor
        joiner = '%s] option,[' % stem
        criteria = '[' + joiner.join(self.ng_prefixes) + stem + '] option'
        tag = 'tag'
        self.finder._find_by_ng_options(self.driver, descriptor, tag, constrains)
        self.finder._find_by_css_selector.assert_called_with(self.driver,
                                                             criteria, tag,
                                                             constrains)
