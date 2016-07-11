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

from sys import exc_info
from time import sleep
from robot import utils
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of, visibility_of
from selenium.webdriver.support.ui import WebDriverWait
from Selenium2Library.keywords import _WaitingKeywords
from ExtendedSelenium2Library.decorators import inherit_docs


@inherit_docs
class ExtendedWaitingKeywords(_WaitingKeywords):
    """ExtendedWaitingKeywords are waiting related execution towards the requested browser."""
    def __init__(self):
        super(ExtendedWaitingKeywords, self).__init__()

    def fast_wait_until_page_contains(self, text, excludes=None, timeout=None, error=None):
        """Waits until ``text`` appears on current page.

        Fails if any item in the ``excludes`` list appears in the current page.

        Fails if ``timeout`` expires before the ``text`` appears.
        See introduction for more information about timeout and its default value.

        Arguments:
        - ``text``: The expected value.
        - ``excludes``: An exclusion list to be use to speed up the wait. (Default None)
        - ``timeout``: The maximum value to wait for ``text`` to appears.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Fast Wait Until Page Contains | text         |
        | @{excludes} =                 | Create List  | a | b | c   |
        | Fast Wait Until Page Contains | text         | ${excludes} |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Text '%s' did not appear in %s" %\
                    (text, self._format_timeout(timeout))
        excludes = excludes if excludes is not None else ()
        # pylint: disable=protected-access
        excluded = next((exclude for exclude in excludes
                         if self._is_text_present(exclude)), False)
        if excluded:
            raise AssertionError("Exclude text '%s' appears on the page." % excluded)
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until(lambda driver: driver._is_text_present(text), error)

    def wait_for_async_condition(self, condition, timeout=None, error=None):
        """Waits until the given asynchronous ``condition`` is true or ``timeout`` expires.

        Arguments:
        - ``condition``: The ``condition`` can be arbitrary JavaScript expression but
                         must explicitly signal when they are finished by invoking
                         the provided callback at the end. See `Execute Async Javascript`
                         for information about executing asynchronous JavaScript.
        - ``timeout``: The maximum value to wait for ``condition`` to come back true.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait For Condition`, `Wait Until Page Contains`, `Wait Until Page Contains
        Element`, `Wait Until Element Is Visible` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait For Async Condition | arguments[arguments.length-1](true) | 15s |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Condition '%s' did not become true in %s" % \
                (condition, self._format_timeout(timeout))
        # pylint: disable=no-member
        WebDriverWait(self._current_browser(), timeout, self._inputs['poll_frequency']).\
            until(lambda driver: driver.execute_async_script(condition), error)

    def wait_for_condition_with_replaced_variables(self, condition, timeout=None, error=None):
        """Replace variables and waits until the given ``condition`` is true or
        ``timeout`` expires.

        Arguments:
        - ``condition``: The ``condition`` can be arbitrary JavaScript expression but must contain
                         a return statement (with the value to be returned) at the end.
                         If ``condition`` is an absolute path to an existing file, the JavaScript
                         to execute will be read from that file. Forward slashes work as
                         a path separator on all operating systems.
                         See `Execute JavaScript With Replaced Variables` for information about
                         accessing the actual contents of the window through JavaScript.
        - ``timeout``: The maximum value to wait for ``condition`` to come back true.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait For Condition`, `Wait Until Page Contains`, `Wait Until Page Contains
        Element`, `Wait Until Element Is Visible` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait For Condition With Replaced Variables | arguments[arguments.length-1](true) | 15s |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Condition '%s' did not become true in %s" % \
                (condition, self._format_timeout(timeout))
        # pylint: disable=no-member
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until(lambda driver:
                  driver.execute_javascript_with_replaced_variables(condition) is True, error)

    def wait_until_angular_ready(self, timeout=None, error=None):
        """Waits until [https://goo.gl/Kzz8Y3|AngularJS] is ready to process the next request or
        ``timeout`` expires.

        You generally *do not* need to call this keyword directly,
        below is the list of keywords which already call this keyword internally:

        | `Click Button`                 |
        | `Click Element`                |
        | `Click Element At Coordinates` |
        | `Click Image`                  |
        | `Click Link`                   |
        | `Double Click Element`         |
        | `Input Password`               |
        | `Input Text`                   |
        | `Open Browser`                 |
        | `Select All From List`         |
        | `Select Checkbox`              |
        | `Select From List`             |
        | `Select From List By Index`    |
        | `Select From List By Label`    |
        | `Select From List By Value`    |
        | `Select Radio Button`          |
        | `Submit Form`                  |

        Arguments:
        - ``timeout``: The maximum value to wait for [https://goo.gl/Kzz8Y3|AngularJS]
                       to be ready to process the next request.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait For Condition`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait Until Element Is Visible`
        and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait Until Angular Ready | 15s |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._implicit_wait_in_secs)
        if not error:
            error = 'AngularJS is not ready in %s' % self._format_timeout(timeout)
        # we add more validation here to support transition
        # between AngularJs to non AngularJS page.
        # pylint: disable=no-member
        script = self.NG_WRAPPER % {'prefix': 'var cb=arguments[arguments.length-1];'
                                              'if(window.angular){',
                                    'handler': 'function(){cb(true)}',
                                    'suffix': '}else{cb(true)}'}
        # pylint: disable=no-member
        browser = self._current_browser()
        browser.set_script_timeout(timeout)
        # pylint: disable=bare-except
        try:
            WebDriverWait(browser, timeout, self._inputs['poll_frequency']).\
                until(lambda driver: driver.execute_async_script(script), error)
        except TimeoutException:
            # prevent double wait
            pass
        except:
            self._debug(exc_info()[0])
            # still inflight, second chance. let the browser take a deep breath...
            sleep(self._inputs['browser_breath_delay'])
            try:
                WebDriverWait(browser, timeout, self._inputs['poll_frequency']).\
                    until(lambda driver: driver.execute_async_script(script), error)
            except:
                # instead of halting the process because AngularJS is not ready
                # in <TIMEOUT>, we try our luck...
                self._debug(exc_info()[0])
            finally:
                browser.set_script_timeout(self._timeout_in_secs)
        finally:
            browser.set_script_timeout(self._timeout_in_secs)

    def wait_until_element_contains_attribute(self, attribute_locator, expected, timeout=None,
                                              error=None):
        """Waits until element attribute identified by ``attribute_locator``
        contains ``expected``.
        Fails if ``timeout`` expires before the ``expected`` element attribute
        presents on the page.

        Arguments:
        - ``attribute_locator``: The locator to find requested element attribute. It consists of
                                 element locator followed by an @ sign and attribute name,
                                 for example "element_id@class".
        - ``expected``: The expected element attribute value.
        - ``timeout``: The maximum value to wait for element attribute to contains ``expected``.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait Until Element Does Not Contain Attribute`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait Until Element Contains Attribute | css=div.class@class | value |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Element did not contain attribute '%s' after %s" %\
                    (expected, self._format_timeout(timeout))
        # pylint: disable=no-member
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until(lambda driver: expected in driver.get_element_attribute(attribute_locator),
                  error)

    def wait_until_element_does_not_contain_attribute(self, attribute_locator, unexpected,
                                                      timeout=None, error=None):
        """Waits until element attribute identified by ``attribute_locator``
        does not contain ``unexpected``.
        Fails if ``timeout`` expires before the ``unexpected`` element attribute
        goes away from the page.

        Arguments:
        - ``attribute_locator``: The locator to find requested element attribute. It consists of
                                 element locator followed by an @ sign and attribute name,
                                 for example "element_id@class".
        - ``unexpected``: The unexpected element attribute value.
        - ``timeout``: The maximum value to wait for ``unexpected`` element attribute to go away.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait Until Element Contains Attribute`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait Until Element Does Not Contain Attribute | css=div.class@class | value |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Element was still contain attribute '%s' after %s" %\
                    (unexpected, self._format_timeout(timeout))
        # pylint: disable=no-member
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until_not(lambda driver: unexpected in driver.get_element_attribute(attribute_locator),
                      error)

    # pylint: disable=missing-docstring
    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._implicit_wait_in_secs)
        if not error:
            error = 'Element \'%s\' was still visible after %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._inputs['poll_frequency']).\
            until_not(visibility_of(element), error)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._implicit_wait_in_secs)
        if not error:
            error = 'Element \'%s\' was not visible in %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._inputs['poll_frequency']).\
            until(visibility_of(element), error)

    def wait_until_location_contains(self, expected, timeout=None, error=None):
        """Waits until current URL contains ``expected``.
        Fails if ``timeout`` expires before the ``expected`` URL presents on the page.

        Arguments:
        - ``expected``: The expected URL value.
        - ``timeout``: The maximum value to wait for URL to contains ``expected``.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait Until Location Does Not Contain`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait Until Location Contains | www | 15s |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Location did not contain '%s' after %s" %\
                    (expected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until(lambda driver: expected in driver.get_location(), error)

    def wait_until_location_does_not_contain(self, unexpected, timeout=None, error=None):
        """Waits until current URL does not contain ``unexpected``.
        Fails if ``timeout`` expires before the ``unexpected`` URL goes away from the page.

        Arguments:
        - ``unexpected``: The unexpected URL value.
        - ``timeout``: The maximum value to wait for ``unexpected`` URL to go away.
                       See `introduction` for more information about ``timeout`` and
                       its default value.
        - ``error``: The value that would be use to override the default error message.

        See also `Wait Until Location Contains`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.

        Examples:
        | Wait Until Location Does Not Contain | www | 15s |
        """
        # pylint: disable=no-member
        timeout = self._get_timeout_value(timeout, self._timeout_in_secs)
        if not error:
            error = "Location was still contain '%s' after %s" %\
                    (unexpected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._inputs['poll_frequency']).\
            until_not(lambda driver: unexpected in driver.get_location(), error)

    @staticmethod
    def _get_timeout_value(timeout, default):
        """Returns default timeout when timeout is None."""
        return default if timeout is None else utils.timestr_to_secs(timeout)

    def _wait_until_html_ready(self, browser, timeout):
        """Wait until HTML is ready by using stale check."""
        # pylint: disable=no-member
        delay = self._inputs['browser_breath_delay']
        if delay < 1:
            delay *= 10
        # let the browser take a deep breath...
        sleep(delay)
        try:
            # pylint: disable=no-member
            WebDriverWait(None, timeout, self._inputs['poll_frequency']).\
                until_not(staleness_of(browser.find_element_by_tag_name('html')), '')
        # pylint: disable=bare-except
        except:
            # instead of halting the process because document is not ready
            # in <TIMEOUT>, we try our luck...
            # pylint: disable=no-member
            self._debug(exc_info()[0])

    def _wait_until_page_ready(self, *args, **kwargs):
        """Semi blocking API that incorporated different strategies for cross-browser support."""
        responses = {
            'page_ready_keywords': [],
            'response': kwargs.pop('default', None)
        }
        # pylint: disable=no-member
        if not self._inputs['block_until_page_ready']:
            return responses
        # pylint: disable=no-member
        browser = kwargs.pop('browser', self._current_browser())
        locator_position = int(kwargs.pop('locator_position', 0))
        prefix = kwargs.pop('prefix', 'var cb=arguments[arguments.length-1];if(window.angular){')
        skip_stale_check = bool(kwargs.pop('skip_stale_check', False))
        # pylint: disable=no-member
        if self._inputs['ensure_jq'] and not skip_stale_check:
            # only during possible page re-load/re-route
            jquery_bootstrap = self.JQUERY_BOOTSTRAP % {'jquery_url': self.JQUERY_URL}
            prefix = 'if(!window.jQuery){%(jquery_bootstrap)s}%(prefix)s' % \
                {'jquery_bootstrap': jquery_bootstrap, 'prefix': prefix}
        # pylint: disable=no-member
        script = self.NG_WRAPPER % {'prefix': prefix,
                                    'handler': kwargs.pop('handler', 'function(){cb(true)}'),
                                    'suffix': kwargs.pop('suffix', '}else{cb(false)}')}
        # pylint: disable=no-member
        default_timeout = self._implicit_wait_in_secs if skip_stale_check \
            else self._timeout_in_secs
        # pylint: disable=no-member
        timeout = self._get_timeout_value(kwargs.pop('timeout', None), default_timeout)
        if len(args) > locator_position and not isinstance(args[locator_position], WebElement):
            args = list(args)
            args[locator_position] = self._element_find(args[locator_position], True, True)
        if not skip_stale_check:
            self._wait_until_html_ready(browser, timeout)
        responses['response'] = self._wait_until_script_ready(browser, timeout, script, *args)
        # pylint: disable=no-member
        responses['page_ready_keywords'] = [self._builtin.run_keyword(keyword)
                                            for keyword in self._page_ready_keyword_list]
        return responses

    def _wait_until_script_ready(self, browser, timeout, script, *args):
        response = None
        # pylint: disable=no-member
        selenium_timeout = self._timeout_in_secs
        try:
            # pylint: disable=no-member
            if timeout != selenium_timeout:
                browser.set_script_timeout(timeout)
            response = browser.execute_async_script(script, *args)
        except TimeoutException:
            # instead of halting the process because document is not ready
            # in <TIMEOUT>, we try our luck...
            # pylint: disable=no-member
            self._debug(exc_info()[0])
        finally:
            if timeout != selenium_timeout:
                # pylint: disable=no-member
                browser.set_script_timeout(selenium_timeout)
        return response
