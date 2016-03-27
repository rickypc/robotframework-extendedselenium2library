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
from ExtendedSelenium2Library.keywords import ExtendedJavascriptKeywords
from Selenium2Library.keywords import _JavaScriptKeywords


class ExtendedJavascriptTests(unittest.TestCase):
    """Extended Javascript keyword test class."""

    def setUp(self):
        """Instantiate the extended Javascript class."""
        self.js_code = 'return true'
        self.js_code_py = 'return True'
        self.js_code_vars = 'return ${true}'
        self.script = ExtendedJavascriptKeywords()
        # pylint: disable=protected-access
        self.script._current_browser = mock.Mock()
        self.script._debug = mock.Mock()
        self.script._warn = mock.Mock()

    def test_should_inherit_keywords(self):
        """Extended Javascript instance should inherit Selenium2 Javascript instances."""
        self.assertIsInstance(self.script, _JavaScriptKeywords)

    def test_execute_async_js_with_replaced_vars(self):
        """Should execute async js with replaced vars."""
        # pylint: disable=protected-access
        self.script._get_javascript_to_execute = mock.Mock()
        self.script._get_javascript_to_execute.return_value = self.js_code_vars
        self.script._replace_variables_in_javascript_code = mock.Mock()
        self.script._replace_variables_in_javascript_code.return_value = self.js_code
        self.script._current_browser().execute_async_script = mock.Mock()
        self.script._current_browser().execute_async_script.return_value = True
        self.assertTrue(self.script.
                        execute_async_javascript_with_replaced_variables(self.js_code_vars))
        self.script._get_javascript_to_execute.assert_called_with(self.js_code_vars)
        self.script._replace_variables_in_javascript_code.assert_called_with(self.js_code_vars)
        self.script._debug.assert_called_with('Executing Asynchronous JavaScript:\n%s' %
                                              self.js_code)
        self.script._current_browser().execute_async_script.assert_called_with(self.js_code)

    def test_execute_js_with_replaced_vars(self):
        """Should execute js with replaced vars."""
        # pylint: disable=protected-access
        self.script._get_javascript_to_execute = mock.Mock()
        self.script._get_javascript_to_execute.return_value = self.js_code_vars
        self.script._replace_variables_in_javascript_code = mock.Mock()
        self.script._replace_variables_in_javascript_code.return_value = self.js_code
        self.script._current_browser().execute_script = mock.Mock()
        self.script._current_browser().execute_script.return_value = True
        self.assertTrue(self.script.
                        execute_javascript_with_replaced_variables(self.js_code_vars))
        self.script._get_javascript_to_execute.assert_called_with(self.js_code_vars)
        self.script._replace_variables_in_javascript_code.assert_called_with(self.js_code_vars)
        self.script._debug.assert_called_with('Executing JavaScript:\n%s' % self.js_code)
        self.script._current_browser().execute_script.assert_called_with(self.js_code)

    def test_get_screen_size(self):
        """Should return the screen size."""
        # pylint: disable=protected-access
        self.script._current_browser().execute_script = mock.Mock()
        self.script._current_browser().execute_script.return_value = [0, 0]
        self.assertEqual(self.script.get_screen_size(), [0, 0])
        self.script._current_browser().execute_script.\
            assert_called_with('return [screen.width, screen.height]')

    def test_warn_any_js_errors(self):
        """Should render warn log message for any javascript errors."""
        logs = [{'message': 'Eeny'}, {'message': 'meeny'}, {'message': 'miny'}, {'message': 'moe'}]
        self.script.get_browser_logs = mock.Mock()
        self.script.get_browser_logs.return_value = logs
        self.script.warn_any_javascript_errors()
        self.script.get_browser_logs.assert_called_with()
        # pylint: disable=protected-access
        self.script._warn.assert_called_with(' %s' % logs)

    def test_warn_any_js_errors_with_excludes(self):
        """Should render warn log message for any javascript errors with exclusion list."""
        logs = [{'message': 'Eeny'}, {'message': 'meeny'}, {'message': 'miny'}, {'message': 'moe'}]
        filtered_logs = [{'message': 'Eeny'}, {'message': 'meeny'}, {'message': 'moe'}]
        self.script.get_browser_logs = mock.Mock()
        self.script.get_browser_logs.return_value = logs
        self.script.warn_any_javascript_errors(['miny'])
        self.script.get_browser_logs.assert_called_with()
        # pylint: disable=protected-access
        self.script._warn.assert_called_with(' %s' % filtered_logs)

    def test_warn_any_js_errors_with_label(self):
        """Should render warn log message for any javascript errors with label."""
        label = 'rhyme'
        logs = [{'message': 'Eeny'}, {'message': 'meeny'}, {'message': 'miny'}, {'message': 'moe'}]
        self.script.get_browser_logs = mock.Mock()
        self.script.get_browser_logs.return_value = logs
        self.script.warn_any_javascript_errors(label=label)
        self.script.get_browser_logs.assert_called_with()
        # pylint: disable=protected-access
        self.script._warn.assert_called_with('%s %s' % (label, logs))

    def test_replace_variables_in_js_code(self):
        """Should replace all variables in js code."""
        # pylint: disable=protected-access
        self.script._builtin = mock.Mock()
        self.script._builtin.replace_variables = mock.Mock()
        self.script._builtin.replace_variables.return_value = self.js_code_py
        self.assertEqual(self.script.
                         _replace_variables_in_javascript_code(self.js_code_vars), self.js_code)
        self.script._builtin.replace_variables.assert_called_with(self.js_code_vars)
