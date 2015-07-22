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

from ExtendedSelenium2Library.version import get_version
# from locators import ExtendedElementFinder
from robot import utils
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, visibility_of
from Selenium2Library import Selenium2Library
from sys import exc_info
from time import sleep

__version__ = get_version()


class ExtendedSelenium2Library(Selenium2Library):
    """ExtendedSelenium2Library is a web testing library with AngularJS support and
    custom improvement for Robot Framework.

    ExtendedSelenium2Library strives to make the transition from Selenium2Library
    as seamless as possible.
    It uses Selenium 2 (WebDriver) libraries and AngularJS synchronization internally
    to control a web browser and ensure all the keywords stay in sync with AngularJS process.

    See `Wait Until Angular Ready` keyword for a list of all other keywords that is already
    calling `Wait Until Angular Ready` from within.
    See http://seleniumhq.org/docs/03_webdriver.html for more information on Selenium 2
    and WebDriver.

    ExtendedSelenium2Library runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    = Non-inherited Keywords =

    | `Element Attribute Should Contain`     |
    | `Element Attribute Should Not Contain` |
    | `Wait For Async Condition`             |
    | `Wait Until Angular Ready`             |
    | `Wait Until Location Contains`         |
    | `Wait Until Location Does Not Contain` |

    = AngularJS Locators Support =

    Coming Soon...

    = Before running tests =

    Prior to running test cases using ExtendedSelenium2Library, ExtendedSelenium2Library must be
    imported into your Robot test suite (see `importing` section), and the
    `Open Browser` keyword must be used to open a browser to the desired location.
    """

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

    def __init__(self, timeout=90.0, implicit_wait=15.0, run_on_failure='Capture Page Screenshot',
                 block_until_page_ready=True, browser_breath_delay=0.05, ensure_jq=True,
                 poll_frequency=0.2):
        # pylint: disable=line-too-long
        """ExtendedSelenium2Library can be imported with optional arguments.

        `timeout` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Selenium Timeout`.

        'implicit_wait' is the implicit timeout that Selenium waits when
        looking for elements.
        It can be later set with `Set Selenium Implicit Wait`.
        See `WebDriver: Advanced Usage`__ section of the SeleniumHQ documentation
        for more information about WebDriver's implicit wait functionality.

        __ http://seleniumhq.org/docs/04_webdriver_advanced.html#explicit-and-implicit-waits

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a ExtendedSelenium2Library keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value "Nothing" will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        `block_until_page_ready` if it's true, will block the execution until the page ready.

        `browser_breath_delay` is the delay in seconds to give the browser enough time
        to execute the next step.

        `ensure_jq` if it's true, will ensure jQuery loaded on the page.

        `poll_frequency` is the number in seconds to retry the next step.

        Examples:
        | Library `|` ExtendedSelenium2Library `|` 15                                            | # Sets default timeout to 15 seconds                                       |
        | Library `|` ExtendedSelenium2Library `|` 0 `|` 5                                       | # Sets default timeout to 0 seconds and default implicit_wait to 5 seconds |
        | Library `|` ExtendedSelenium2Library `|` 5 `|` run_on_failure=Log Source               | # Sets default timeout to 5 seconds and runs `Log Source` on failure       |
        | Library `|` ExtendedSelenium2Library `|` implicit_wait=5 `|` run_on_failure=Log Source | # Sets default implicit_wait to 5 seconds and runs `Log Source` on failure |
        | Library `|` ExtendedSelenium2Library `|` timeout=10      `|` run_on_failure=Nothing    | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        # pylint: disable=line-too-long
        Selenium2Library.__init__(self, timeout, implicit_wait, run_on_failure)
        self._block_until_page_ready = block_until_page_ready
        self._browser_breath_delay = 0.05 \
            if browser_breath_delay is None else float(browser_breath_delay)
        self._ensure_jq = True if ensure_jq else False
        self._implicit_wait_in_secs = 15.0 \
            if implicit_wait is None else float(implicit_wait)
        jquery_bootstrap = self.JQUERY_BOOTSTRAP % \
            {'jquery_url': self.JQUERY_URL} if self._ensure_jq else ''
        self._page_ready_bootstrap = self.PAGE_READY_WRAPPER % \
            {'jquery_bootstrap': jquery_bootstrap}
        self._poll_frequency = 0.2 if poll_frequency is None else float(poll_frequency)
        # self._element_finder = ExtendedElementFinder()

    def click_button(self, locator):
        """Clicks a button identified by `locator`.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_button(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_element(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        """Click element identified by `locator` at x/y coordinates of the element.
        Cursor is moved and the center of the element and x/y coordinates are
        calculted from that point.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self). \
            click_element_at_coordinates(locator, xoffset, yoffset)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_image(self, locator):
        """Clicks an image found by `locator`.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_image(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def click_link(self, locator):
        """Clicks a link identified by locator.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).click_link(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).double_click_element(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def element_attribute_should_contain(self, attribute_locator, expected, message=''):
        """Verifies element attribute identified by `attribute_locator` contains `expected`.

        `attribute_locator` consists of element locator followed by an @ sign and attribute name,
        for example "element_id@class".

        `message` can be used to override the default error message.
        """
        actual = self.get_element_attribute(attribute_locator)
        if expected not in actual:
            if not message:
                message = "Element attribute '%s' should have contained '%s'" \
                          " but its value was '%s'." % (attribute_locator, expected, actual)
            raise AssertionError(message)

    def element_attribute_should_not_contain(self, attribute_locator, expected, message=''):
        """Verifies element attribute identified by `attribute_locator`
        does not contain `expected`.

        `attribute_locator` consists of element locator followed by an @ sign and attribute name,
        for example "element_id@class".

        `message` can be used to override the default error message.
        """
        actual = self.get_element_attribute(attribute_locator)
        if expected in actual:
            if not message:
                message = "Element attribute '%s' should not contain '%s'" \
                          " but it did." % (attribute_locator, expected)
            raise AssertionError(message)

    def get_location(self):
        """Returns the current location."""
        # AngularJS support
        script = self.NG_WRAPPER % {'prefix': 'var cb=arguments[arguments.length-1];'
                                              'if(window.angular){',
                                    'handler': 'function(){cb(document.location.href)}',
                                    'suffix': '}else{cb(document.location.href)}'}
        return self._current_browser().execute_async_script(script)

    def is_element_visible(self, locator):
        """Returns element visibility identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        return self._is_visible(locator)

    def open_browser(self, url, browser='firefox', alias=None, remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None):
        """Opens a new browser instance to given URL.

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        Optional alias is an alias for the browser instance and it can be used
        for switching between browsers (just as index can be used). See `Switch
        Browser` for more details.

        Possible values for `browser` are as follows:

        | firefox          | FireFox                         |
        | ff               | FireFox                         |
        | internetexplorer | Internet Explorer               |
        | ie               | Internet Explorer               |
        | googlechrome     | Google Chrome                   |
        | gc               | Google Chrome                   |
        | chrome           | Google Chrome                   |
        | opera            | Opera                           |
        | phantomjs        | PhantomJS                       |
        | htmlunit         | HTMLUnit                        |
        | htmlunitwithjs   | HTMLUnit with Javascipt support |
        | android          | Android                         |
        | iphone           | Iphone                          |
        | safari           | Safari                          |

        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine

        Optional 'remote_url' is the url for a remote selenium server for example
        http://127.0.0.1/wd/hub.  If you specify a value for remote you can
        also specify 'desired_capabilities' which is a string in the form
        key1:val1,key2:val2 that will be used to specify desired_capabilities
        to the remote server. This is useful for doing things like specify a
        proxy server for internet explorer or for specify browser and os if your
        using saucelabs.com. 'desired_capabilities' can also be a dictonary
        (created with 'Create Dictionary') to allow for more complex configurations.

        Optional 'ff_profile_dir' is the path to the firefox profile dir if you
        wish to overwrite the default.
        """
        index = super(ExtendedSelenium2Library, self).open_browser(url, browser, alias, remote_url,
                                                                   desired_capabilities,
                                                                   ff_profile_dir)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()
        return index

    def select_all_from_list(self, locator):
        """Selects all values from multi-select list identified by `id`.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        super(ExtendedSelenium2Library, self).select_all_from_list(locator)
        self._element_trigger_change(locator)

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            self._select_checkbox_or_radio_button(element)

    def select_from_list(self, locator, *items):
        """Selects `*items` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*items` is an empty list, all values of the list will be selected.

        *items try to select by value then by label.

        It's faster to use 'by index/value/label' functions.

        An exception is raised for a single-selection list if the last
        value does not exist in the list and a warning for all other non-
        existing items. For a multi-selection list, an exception is raised
        for any and all non-existing values.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        super(ExtendedSelenium2Library, self).select_from_list(locator, *items)
        self._element_trigger_change(locator)

    def select_from_list_by_index(self, locator, *indexes):
        """Selects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        super(ExtendedSelenium2Library, self).select_from_list_by_index(locator, *indexes)
        self._element_trigger_change(locator)

    def select_from_list_by_label(self, locator, *labels):
        """Selects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        super(ExtendedSelenium2Library, self).select_from_list_by_label(locator, *labels)
        self._element_trigger_change(locator)

    def select_from_list_by_value(self, locator, *values):
        """Selects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        super(ExtendedSelenium2Library, self).select_from_list_by_value(locator, *values)
        self._element_trigger_change(locator)

    def select_radio_button(self, group_name, value):
        # pylint: disable=line-too-long
        """Sets selection of radio button group identified by `group_name` to `value`.

        The radio button to be selected is located by two arguments:
        - `group_name` is used as the name of the radio input
        - `value` is used for the value attribute or for the id attribute

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        Examples:
        | Select Radio Button | size | XL | # Matches HTML like <input type="radio" name="size" value="XL">XL</input> |
        | Select Radio Button | size | sizeXL | # Matches HTML like <input type="radio" name="size" value="XL" id="sizeXL">XL</input> |
        """
        # pylint: disable=line-too-long
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            self._select_checkbox_or_radio_button(element)

    def submit_form(self, locator=None):
        """Submits a form identified by `locator`.

        If `locator` is empty, first form in the page will be submitted.
        Key attributes for forms are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._scroll_into_view(locator)
        super(ExtendedSelenium2Library, self).submit_form(locator)
        self._wait_until_page_ready()
        self.wait_until_angular_ready()

    def wait_for_async_condition(self, condition, timeout=None, error=None):
        """Waits until the given asynchronous `condition` is true or `timeout` expires.

        The `condition` can be arbitrary JavaScript expression but must explicitly signal
        they are finished by invoking the provided callback at the end.
        See `Execute Async Javascript` for information about executing asynchronous JavaScript.

        `error` can be used to override the default error message.

        See `introduction` for more information about `timeout` and its default value.

        See also `Wait For Condition`, `Wait Until Page Contains`, `Wait Until Page Contains
        Element`, `Wait Until Element Is Visible` and BuiltIn keyword
        `Wait Until Keyword Succeeds`.
        """
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Condition '%s' did not become true in %s" % \
                (condition, self._format_timeout(timeout))
        WebDriverWait(self._current_browser(), timeout, self._poll_frequency).\
            until(lambda driver: driver.execute_async_script(condition), error)

    def wait_until_angular_ready(self, timeout=None, error=None):
        """Waits until AngularJS is ready to process next request or `timeout` expires.

        You do not need to call this keyword directly,
        below is the list of keywords which already call this keyword:

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

        `error` can be used to override the default error message.

        See `introduction` for more information about `timeout` and its
        default value.

        See also `Wait For Condition`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait Until Element Is Visible`
        and BuiltIn keyword `Wait Until Keyword Succeeds`.
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
        """Waits until element specified with `locator` is not visible.

        Fails if `timeout` expires before the element is not visible. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Element Is Visible`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        timeout = self._implicit_wait_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = 'Element \'%s\' was still visible after %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._poll_frequency).until_not(visibility_of(element), error)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` is visible.

        Fails if `timeout` expires before the element is visible. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Element Is Not Visible`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        timeout = self._implicit_wait_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = 'Element \'%s\' was not visible in %s' % \
                (locator, self._format_timeout(timeout))
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        WebDriverWait(None, timeout, self._poll_frequency).until(visibility_of(element), error)

    def wait_until_location_contains(self, expected, timeout=None, error=None):
        """Waits until current URL contains `expected`.

        Fails if `timeout` expires before the expected URL presents on the page. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Location Does Not Contain`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Location did not contain '%s' after %s" %\
                    (expected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._poll_frequency).\
            until(lambda driver: expected in driver.get_location(), error)

    def wait_until_location_does_not_contain(self, expected, timeout=None, error=None):
        """Waits until current URL does not contain `expected`.

        Fails if `timeout` expires before the expected URL goes away from the page. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Location Contains`, `Wait Until Page Contains`,
        `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        timeout = self._timeout_in_secs if timeout is None else utils.timestr_to_secs(timeout)
        if not error:
            error = "Location was still contain '%s' after %s" %\
                    (expected, self._format_timeout(timeout))
        WebDriverWait(self, timeout, self._poll_frequency).\
            until_not(lambda driver: expected in driver.get_location(), error)

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
                    until_not(staleness_of(browser.find_element_by_tag_name('body')), '')
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
