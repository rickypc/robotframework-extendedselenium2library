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

from ExtendedSelenium2Library.decorators import inherit_docs
from ExtendedSelenium2Library.locators import ExtendedElementFinder
from ExtendedSelenium2Library.version import get_version
from robot import utils
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, visibility_of
from Selenium2Library import Selenium2Library
from sys import exc_info
from time import sleep
from robot.libraries.BuiltIn import BuiltIn

__version__ = get_version()


# pylint: disable=too-many-ancestors
@inherit_docs
class ExtendedSelenium2Library(Selenium2Library):
    # pylint: disable=line-too-long
    """ExtendedSelenium2Library is a [http://goo.gl/boVQia|Selenium2 (WebDriver)]
    web testing library with [https://goo.gl/Kzz8Y3|AngularJS] support and
    custom improvement for [http://goo.gl/lES6WM|Robot Framework].

    ExtendedSelenium2Library strives to make the transition from
    [https://goo.gl/1VXDSI|Selenium2Library] as seamless as possible.
    It uses [http://goo.gl/boVQia|Selenium2 (WebDriver)] libraries
    and [https://goo.gl/Kzz8Y3|AngularJS] synchronization internally to control a web browser
    and ensure all the keywords stay in sync with [https://goo.gl/Kzz8Y3|AngularJS] process.

    See `Wait Until Angular Ready` keyword for a list of all other keywords that is already
    calling `Wait Until Angular Ready` from within.
    See [http://goo.gl/boVQia|Selenium2 and WebDriver] for more information.

    ExtendedSelenium2Library runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    Non-inherited Keywords:
    | `Element Attribute Should Contain`     |
    | `Element Attribute Should Not Contain` |
    | `Get Browser Logs`                     |
    | `Is Element Visible`                   |
    | `Register Page Ready Keyword`          |
    | `Remove Page Ready Keyword`            |
    | `Wait For Async Condition`             |
    | `Wait Until Angular Ready`             |
    | `Wait Until Location Contains`         |
    | `Wait Until Location Does Not Contain` |

    AngularJS Locators Support:
    | *AngularJS Strategy* | *Example*                                         | *Description*                                        |
    | model                | Click Element   `|` model=model_name              | Matches by AngularJS model name                      |
    | binding              | Click Element   `|` binding=binding_name          | Matches by AngularJS binding name                    |
    | partial binding      | Click Element   `|` partial binding=binding_name  | Matches by partial AngularJS binding name            |
    | button               | Click Element   `|` button=My Button              | Matches button elements by their button text         |
    | partial button       | Click Element   `|` partial button=y But          | Matches button elements by their partial button text |
    | options              | Get WebElements `|` options=options_descriptor    | Matches by AngularJS options descriptor              |

    = Before running tests =

    Prior to running test cases using ExtendedSelenium2Library, ExtendedSelenium2Library must be
    imported into your Robot test suite (see `importing` section), and the
    `Open Browser` keyword must be used to open a browser to the desired location.
    """
    # pylint: disable=line-too-long

    # let's not confuse people with different name and version
    __doc__ += Selenium2Library.__doc__.split('desired location.', 1)[-1]. \
        replace('Selenium2Library', 'ExtendedSelenium2Library'). \
        replace('version 1.7', 'version 0.4.9'). \
        replace('Version 1.7.0', 'version 0.4.9')

    JQUERY_URL = '//code.jquery.com/jquery-1.11.3.min.js'
    JQUERY_BOOTSTRAP = 'var a=document.getElementsByTagName(\'head\')[0];' \
                       'var b=document.createElement(\'script\');' \
                       'b.type=\'text/javascript\';b.src=document.location.' \
                       'protocol+\'%(jquery_url)s\';a.appendChild(b);'
    NG_WRAPPER = '%(prefix)s' \
                 'angular.element(document.querySelector(\'[data-ng-app]\')||document).' \
                 'injector().get(\'$browser\').notifyWhenNoOutstandingRequests(%(handler)s)' \
                 '%(suffix)s'
    PAGE_READY_WRAPPER = 'var cb=arguments[arguments.length-1];if(window.jQuery){' \
                         '$(document).ready(function(){cb(true)})}else{'\
                         '%(jquery_bootstrap)s' \
                         'cb(document.readyState===\'complete\' && document.body && ' \
                         'document.body.childNodes.length)}'
    ROBOT_EXIT_ON_FAILURE = True
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, implicit_wait=15.0, **kwargs):
        # pylint: disable=line-too-long
        """ExtendedSelenium2Library can be imported with optional arguments.

        Arguments:
        - ``timeout``: The maximum value to wait for all waiting actions. (Default 5.0)
                       It can be set later with `Set Selenium Timeout`.
                       See `introduction` for more information about ``timeout``.
        - ``implicit_wait``: The maximum implicit timeout value to wait when looking
                             for elements. (Default 15.0)
                             It can be later set with `Set Selenium Implicit Wait`.
                             See [http://goo.gl/8ePMo6|WebDriver: Advanced Usage]
                             section of the SeleniumHQ documentation for more information about
                             WebDriver's implicit wait functionality.
        - ``run_on_failure``: The name of a keyword (from any available libraries) to execute
                              when a ExtendedSelenium2Library keyword fails. By default
                              `Capture Page Screenshot` will be used to take a screenshot of
                              the current page.
                              Using the value "Nothing" will disable this feature altogether.
                              See `Register Keyword To Run On Failure` keyword for
                              more information about this functionality.
        - ``screenshot_root_directory``: The default root directory that screenshots should be
                                         stored in. If not provided, the default directory will be
                                         where [http://goo.gl/lES6WM|Robot Framework] places its
                                         logfile.
        - ``block_until_page_ready``: A boolean flag to block the execution until
                                      the page is ready. (Default True)
        - ``browser_breath_delay``: The delay value in seconds to give the browser enough time to
                                    complete current execution. (Default 0.05)
        - ``ensure_jq``: A boolean flag to ensure jQuery library is loaded on the page.
                         ``sizzle`` locator strategy will depend on this flag. (Default True)
        - ``poll_frequency``: The delay value in seconds to retry the next step. (Default 0.2)

        Examples:
        | Library `|` ExtendedSelenium2Library `|` 15                                            | # Sets default timeout to 15 seconds                                       |
        | Library `|` ExtendedSelenium2Library `|` 0 `|` 5                                       | # Sets default timeout to 0 seconds and default implicit_wait to 5 seconds |
        | Library `|` ExtendedSelenium2Library `|` 5 `|` run_on_failure=Log Source               | # Sets default timeout to 5 seconds and runs `Log Source` on failure       |
        | Library `|` ExtendedSelenium2Library `|` implicit_wait=5 `|` run_on_failure=Log Source | # Sets default implicit_wait to 5 seconds and runs `Log Source` on failure |
        | Library `|` ExtendedSelenium2Library `|` timeout=10      `|` run_on_failure=Nothing    | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        # pylint: disable=line-too-long
        self._block_until_page_ready = kwargs.pop('block_until_page_ready', True)
        self._browser_breath_delay = float(kwargs.pop('browser_breath_delay', 0.05))
        self._ensure_jq = kwargs.pop('ensure_jq', True)
        self._poll_frequency = float(kwargs.pop('poll_frequency', 0.2))
        Selenium2Library.__init__(self, implicit_wait=implicit_wait, **kwargs)
        self._element_finder = ExtendedElementFinder()
        self._implicit_wait_in_secs = float(implicit_wait) if implicit_wait is not None else 15.0
        jquery_bootstrap = self.JQUERY_BOOTSTRAP % \
            {'jquery_url': self.JQUERY_URL} if self._ensure_jq else ''
        self._page_ready_bootstrap = self.PAGE_READY_WRAPPER % \
            {'jquery_bootstrap': jquery_bootstrap}
        self._table_element_finder._element_finder = self._element_finder  # pylint: disable=protected-access
        self._page_ready_keyword_list = []
        self._builtin = BuiltIn()

    def click_button(self, locator):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_button(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_element(self, locator):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_element(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self). \
            click_element_at_coordinates(locator, xoffset, yoffset)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_image(self, locator):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_image(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_link(self, locator):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_link(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def double_click_element(self, locator):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).double_click_element(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def element_attribute_should_contain(self, attribute_locator, expected, message=''):
        """Verifies element attribute identified by ``attribute_locator`` contains ``expected``.

        Arguments:
        - ``attribute_locator``: The locator to find requested element attribute. It consists of
                                 element locator followed by an @ sign and attribute name,
                                 for example "element_id@class".
        - ``expected``: The expected attribute value.
        - ``message``: The value that would be use to override the default error message.

        Examples:
        | Element Attribute Should Contain | css=div.class@class | value |
        """
        actual = self.get_element_attribute(attribute_locator)
        if expected not in actual:
            if not message:
                message = "Element attribute '%s' should have contained '%s'" \
                          " but its value was '%s'." % (attribute_locator, expected, actual)
            raise AssertionError(message)

    def element_attribute_should_not_contain(self, attribute_locator, unexpected, message=''):
        """Verifies element attribute identified by ``attribute_locator``
        does not contain ``unexpected``.

        Arguments:
        - ``attribute_locator``: The locator to find requested element attribute. It consists of
                                 element locator followed by an @ sign and attribute name,
                                 for example "element_id@class".
        - ``unexpected``: The unexpected attribute value.
        - ``message``: The value that would be use to override the default error message.

        Examples:
        | Element Attribute Should Not Contain | css=div.class@class | value |
        """
        actual = self.get_element_attribute(attribute_locator)
        if unexpected in actual:
            if not message:
                message = "Element attribute '%s' should not contain '%s'" \
                          " but it did." % (attribute_locator, unexpected)
            raise AssertionError(message)

    def get_browser_logs(self):
        """Returns the Javascript console logs from the browser.

        Please see [https://goo.gl/S7yvqR|Logging Preferences JSON object] to set
        how verbose the logging should be. (Default 'SEVERE')

        Examples:
        | Get Browser Logs |
        """
        return self._current_browser().get_log('browser')

    def get_location(self):
        # AngularJS support
        script = self.NG_WRAPPER % {'prefix': 'var cb=arguments[arguments.length-1];'
                                              'if(window.angular){',
                                    'handler': 'function(){cb(document.location.href)}',
                                    'suffix': '}else{cb(document.location.href)}'}
        return self._current_browser().execute_async_script(script)

    def is_element_visible(self, locator):
        """Returns element visibility identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.

        Examples:
        | Is Element Visible | css=div.class |
        """
        return self._is_visible(locator)

    # pylint: disable=too-many-arguments
    def open_browser(self, url, browser='firefox', alias=None, remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None):
        index = super(ExtendedSelenium2Library, self).\
            open_browser(url, browser, alias, remote_url, desired_capabilities, ff_profile_dir)
        # register the main window as the first window handle in the list
        self.select_window()
        self._wait_until_page_ready()
        self.wait_until_angular_ready()
        return index

    def register_page_ready_keyword(self, keyword_name):
        """Adds a keyword to be run at the end of the wait until page ready keyword.

        Arguments:
        - ``keyword_name``: Adds existing keyword name to be run when the page is ready.

        Examples:
        | Register Page Ready Keyword | My Keyword |
        """
        self._page_ready_keyword_list.append(keyword_name)

    def remove_page_ready_keyword(self, keyword_name):
        """Removes a keyword to be run at the end of the wait until page ready keyword.

        Arguments:
        - ``keyword_name``: Removes existing keyword name from running when the page is ready.

        Examples:
        | Remove Page Ready Keyword | My Keyword |
        """
        self._page_ready_keyword_list.remove(keyword_name)

    def select_all_from_list(self, locator):
        super(ExtendedSelenium2Library, self).select_all_from_list(locator)
        self._element_trigger_change(locator)

    def select_checkbox(self, locator):
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            self._select_checkbox_or_radio_button(element)

    def select_from_list(self, locator, *items):
        super(ExtendedSelenium2Library, self).select_from_list(locator, *items)
        self._element_trigger_change(locator)

    def select_from_list_by_index(self, locator, *indexes):
        super(ExtendedSelenium2Library, self).select_from_list_by_index(locator, *indexes)
        self._element_trigger_change(locator)

    def select_from_list_by_label(self, locator, *labels):
        super(ExtendedSelenium2Library, self).select_from_list_by_label(locator, *labels)
        self._element_trigger_change(locator)

    def select_from_list_by_value(self, locator, *values):
        super(ExtendedSelenium2Library, self).select_from_list_by_value(locator, *values)
        self._element_trigger_change(locator)

    def select_radio_button(self, group_name, value):
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            self._select_checkbox_or_radio_button(element)

    def submit_form(self, locator=None):
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).submit_form(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

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
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Condition '%s' did not become true in %s" % \
                (condition, self._format_timeout(timeout))
        WebDriverWait(self._current_browser(), timeout, self._poll_frequency).\
            until(lambda driver: driver.execute_async_script(condition), error)

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
        timeout = self._implicit_wait_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = 'AngularJS is not ready in %s' % self._format_timeout(timeout)
        # we add more validation here to support transition between AngularJs to non AngularJS page.
        script = self.NG_WRAPPER % {'prefix': 'var cb=arguments[arguments.length-1];'
                                              'if(window.angular){',
                                    'handler': 'function(){cb(true)}',
                                    'suffix': '}else{cb(true)}'}
        browser = self._current_browser()
        browser.set_script_timeout(timeout)
        try:
            WebDriverWait(browser, timeout, self._poll_frequency).\
                until(lambda driver: driver.execute_async_script(script), error)
        except TimeoutException:
            # prevent double wait
            pass
        except:
            self._debug(exc_info()[0])
            # still inflight, second chance. let the browser take a deep breath...
            sleep(self._browser_breath_delay)
            try:
                WebDriverWait(browser, timeout, self._poll_frequency).\
                    until(lambda driver: driver.execute_async_script(script), error)
            except:
                # instead of halting the process because AngularJS is not ready
                # in <TIMEOUT>, we try our luck...
                self._debug(exc_info()[0])
            finally:
                browser.set_script_timeout(self._timeout_in_secs)
        finally:
            browser.set_script_timeout(self._timeout_in_secs)

    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        timeout = self._implicit_wait_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = 'Element \'%s\' was still visible after %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._poll_frequency).until_not(visibility_of(element), error)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        timeout = self._implicit_wait_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = 'Element \'%s\' was not visible in %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._poll_frequency).until(visibility_of(element), error)

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
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Location did not contain '%s' after %s" %\
                    (expected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._poll_frequency).\
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
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Location was still contain '%s' after %s" %\
                    (unexpected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._poll_frequency).\
            until_not(lambda driver: unexpected in driver.get_location(), error)

    def _angular_select_checkbox_or_radio_button(self, element):
        """Select checkbox or radio button when AngularJS is ready."""
        if element is None:
            raise AssertionError("Element not found.")
        # you will operating in different scope
        script = self.NG_WRAPPER % {'prefix': 'var obj=arguments[0];',
                                    'handler': 'function(){angular.element(obj).'
                                               'prop(\'checked\',true).triggerHandler(\'click\')}',
                                    'suffix': ''}
        self._current_browser().execute_script(script, element)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def _element_trigger_change(self, locator):
        """Trigger change event on target element when AngularJS is ready."""
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        if self._is_angular_control(element):
            # you will operating in different scope
            script = self.NG_WRAPPER % {'prefix': 'var obj=arguments[0];',
                                        'handler': 'function(){$(obj).trigger(\'change\').'
                                                   'trigger(\'focusout\')}',
                                        'suffix': ''}
            self._current_browser().execute_script(script, element)
            self._wait_until_page_ready()
            self.wait_until_angular_ready()
        else:
            self._wait_until_page_ready()

    def _get_browser_name(self):
        """Returns current browser name."""
        return self._current_browser().capabilities['browserName'].strip().lower()

    def _input_text_into_text_field(self, locator, text):
        """Send keys to text field with AngularJS synchronization."""
        super(ExtendedSelenium2Library, self)._input_text_into_text_field(locator, text)
        element = self._element_find(locator, True, True)
        if self._is_angular_control(element):
            self._wait_until_page_ready()
            self.wait_until_angular_ready()

    def _is_angular_control(self, element):
        """Returns true if target element is an AngularJS control, otherwise false."""
        if self._is_angular_page():
            return element.get_attribute('data-ng-model') != '' \
                or element.get_attribute('ng-model') != ''
        else:
            return False

    def _is_angular_page(self):
        """Returns true if current page is an AngularJS page, otherwise false."""
        script = 'return !!window.angular'
        try:
            return self._current_browser().execute_script(script)
        except:
            self._debug(exc_info()[0])
            return False

    def _is_internet_explorer(self, browser_name=None):
        """Returns true if current browser is Internet Explorer."""
        if not browser_name:
            browser_name = self._get_browser_name()
        return browser_name == 'internetexplorer' or browser_name == 'ie'

    def _scroll_into_view(self, locator):
        """Scroll target element into view. (Internet Explorer only)."""
        if self._is_internet_explorer():
            element = self._element_find(locator, True, True)
            if element is None:
                raise AssertionError("Element '%s' not found." % locator)
            script = 'arguments[0].scrollIntoView(false)'
            self._current_browser().execute_script(script, element)

    def _select_checkbox_or_radio_button(self, element):
        """Select checkbox or radio button with AngularJS support."""
        if self._is_angular_control(element):
            self._angular_select_checkbox_or_radio_button(element)
        else:
            element.click()
            self._wait_until_page_ready()

    def _wait_until_page_ready(self, timeout=None):
        """Semi blocking API that incorporated different strategies for cross-browser support."""
        if self._block_until_page_ready:
            delay = self._browser_breath_delay
            if delay < 1:
                delay *= 10
            # let the browser take a deep breath...
            sleep(delay)
            timeout = self._implicit_wait_in_secs \
                if timeout is None else utils.timestr_to_secs(timeout)
            browser = self._current_browser()
            try:
                WebDriverWait(None, timeout, self._poll_frequency).\
                    until_not(staleness_of(browser.find_element_by_tag_name('html')), '')
            except:
                # instead of halting the process because document is not ready
                # in <TIMEOUT>, we try our luck...
                self._debug(exc_info()[0])
            try:
                WebDriverWait(browser, timeout, self._poll_frequency).\
                    until(lambda driver: driver.
                          execute_async_script(self._page_ready_bootstrap), '')
            except:
                # instead of halting the process because document is not ready
                # in <TIMEOUT>, we try our luck...
                self._debug(exc_info()[0])
            for keyword in self._page_ready_keyword_list:
                self._builtin.run_keyword(keyword)
