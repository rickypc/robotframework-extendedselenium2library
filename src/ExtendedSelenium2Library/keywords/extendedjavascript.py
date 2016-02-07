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

from re import sub
from Selenium2Library.keywords import _JavaScriptKeywords


class ExtendedJavascriptKeywords(_JavaScriptKeywords):
    """ExtendedJavascriptKeywords are JavaScript related execution in the requested browser."""
    def __init__(self):
        super(ExtendedJavascriptKeywords, self).__init__()

    def execute_async_javascript_with_replaced_variables(self, *code):
        # pylint: disable=line-too-long
        """Replace variables and executes asynchronous the given JavaScript ``code``.

        Similar to `Execute Javascript` keyword except that the scripts executed with
        this keyword must explicitly signal when they are finished by invoking the
        provided callback. This callback is always injected into the executed
        function as the last argument.

        Scripts must complete within the script timeout or this keyword will
        fail. See the `Timeouts` section for more information.

        Arguments:
        - ``code``: It may contain multiple lines of JavaScript code and may be divided into
                    multiple cells in the test data. In that case, the parts are
                    catenated together without adding spaces.

                    If ``code`` is an absolute path to an existing file, the JavaScript
                    to execute will be read from that file. Forward slashes work as
                    a path separator on all operating systems.

                    The JavaScript executes in the context of the currently selected
                    frame or window as the body of an anonymous function. Use _window_ to
                    refer to the window of your application and _document_ to refer to the
                    document object of the current frame or window, e.g.
                    _document.getElementById('foo')_.

        Examples:
        | Execute Async JavaScript With Replaced Variables | var callback = arguments[arguments.length - 1] | window.setTimeout(callback, 2000) |
        | Execute Async JavaScript With Replaced Variables | ${CURDIR}/async_js_to_execute.js               |                                   |
        | ${retval} =              | Execute Async JavaScript With Replaced Variables                       |                                   |
        | ...                      | var callback = arguments[arguments.length - 1]                         |                                   |
        | ...                      | function answer(){callback("text");}                                   |                                   |
        | ...                      | window.setTimeout(answer, 2000)                                        |                                   |
        | Should Be Equal          | ${retval}                                                              | text                              |
        """
        # pylint: disable=line-too-long
        js_code = self._get_javascript_to_execute(''.join(code))
        js_code = self._replace_variables_in_javascript_code(js_code)
        # pylint: disable=no-member
        self._debug('Executing Asynchronous JavaScript:\n%s' % js_code)
        # pylint: disable=no-member
        return self._current_browser().execute_async_script(js_code)

    def execute_javascript_with_replaced_variables(self, *code):
        # pylint: disable=line-too-long
        """Replace variables and executes the given JavaScript ``code``.

        This keyword returns None unless there is a return statement in the
        JavaScript. Return values are converted to the appropriate type in
        Python, including WebElements.

        Arguments:
        - ``code``: It may contain multiple lines of JavaScript code and may be divided into
                    multiple cells in the test data. In that case, the parts are
                    catenated together without adding spaces.

                    If ``code`` is an absolute path to an existing file, the JavaScript
                    to execute will be read from that file. Forward slashes work as
                    a path separator on all operating systems.

                    The JavaScript executes in the context of the currently selected
                    frame or window as the body of an anonymous function. Use _window_ to
                    refer to the window of your application and _document_ to refer to the
                    document object of the current frame or window, e.g.
                    _document.getElementById('foo')_.

        Examples:
        | Execute JavaScript With Replaced Variables | window.my_js_function('arg1', '${arg2}')   |               |
        | Execute JavaScript With Replaced Variables | ${CURDIR}/js_to_execute.js                 |               |
        | ${sum} =                                   | Execute JavaScript With Replaced Variables | return 1 + 1; |
        | Should Be Equal                            | ${sum}                                     | ${2}          |
        """
        # pylint: disable=line-too-long
        js_code = self._get_javascript_to_execute(''.join(code))
        js_code = self._replace_variables_in_javascript_code(js_code)
        # pylint: disable=no-member
        self._debug('Executing JavaScript:\n%s' % js_code)
        # pylint: disable=no-member
        return self._current_browser().execute_script(js_code)

    def get_screen_size(self):
        """Returns current screen size as `width` and `height`.

        Examples:
        | ${width} | ${height} = | Get Screen Size |
        """
        # pylint: disable=no-member
        return self._current_browser().execute_script('return [screen.width, screen.height]')

    def warn_any_javascript_errors(self, excludes=None, label=''):
        """Log any JavaScript errors in the page as warning in the test report.

        Arguments:
        - ``excludes``: An exclusion list to be use to filter out error messages. (Default None)
        - ``label``: Label the JavaScript errors for easy reading. (Default '')

        Examples:
        | Warn Any Javascript Errors |              |              |
        | @{excludes} =              | Create List  | a | b | c    |
        | Warn Any Javascript Errors | ${None}      | MY_LABEL     |
        | Warn Any Javascript Errors | ${excludes}  | ${TEST NAME} |
        """
        excludes = excludes if excludes is not None else ()

        def include(value):
            """Filter out error messages based on exclusion list."""
            return not any(True for e in excludes if e in value)
        # pylint: disable=no-member
        logs = self.get_browser_logs()
        # opt-out approach
        logs = [error for error in logs if include(error['message'])]
        total_logs = len(logs)
        if total_logs > 0:
            message = '%s %s' % (label, logs)
            # pylint: disable=no-member
            self._warn(message)

    def _replace_variables_in_javascript_code(self, code):
        """Replace all variables in the given JavaScript ``code``
        for later JavaScript execution."""
        # pylint: disable=no-member
        code = self._builtin.replace_variables(code)
        code = sub(r'(False|True)', lambda match: match.group(1).lower(), code)
        return code
