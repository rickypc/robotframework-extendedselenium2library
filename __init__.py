#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Richard Huang <rickypc@users.noreply.github.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import Selenium2Library
#from ExtendedSelenium2Library.locators import ExtendedElementFinder

current_dir = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(current_dir, 'version.py'))
__version__ = VERSION


class ExtendedSelenium2Library(Selenium2Library.Selenium2Library):
    """Extended Selenium2 library to support AngularJS and custom improvement to be used with
    Robot Framework's test library.
    """

    NG_READY = '__RFNGREADY'
    NG_WRAPPER = '%(prefix)s' \
                 'angular.element(document.querySelector(\'[data-ng-app]\')||document).injector().' \
                 'get(\'$browser\').notifyWhenNoOutstandingRequests(%(handler)s)'

    ROBOT_EXIT_ON_FAILURE = True
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, timeout=5.0, implicit_wait=0.0, run_on_failure='Capture Page Screenshot'):
        Selenium2Library.Selenium2Library.__init__(self, timeout, implicit_wait, run_on_failure)
        #self._element_finder = ExtendedElementFinder()

    def click_button(self, locator):
        super(ExtendedSelenium2Library, self).click_button(locator)
        self.wait_until_angular_ready()

    def click_element(self, locator):
        super(ExtendedSelenium2Library, self).click_element(locator)
        self.wait_until_angular_ready()

    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        super(ExtendedSelenium2Library, self).click_element_at_coordinates(locator, xoffset, yoffset)
        self.wait_until_angular_ready()

    def click_image(self, locator):
        super(ExtendedSelenium2Library, self).click_image(locator)
        self.wait_until_angular_ready()

    def click_link(self, locator):
        super(ExtendedSelenium2Library, self).click_link(locator)
        self.wait_until_angular_ready()

    def double_click_element(self, locator):
        super(ExtendedSelenium2Library, self).double_click_element(locator)
        self.wait_until_angular_ready()

    def open_browser(self, url, browser='firefox', alias=None,remote_url=False,
                     desired_capabilities=None,ff_profile_dir=None):
        index = super(ExtendedSelenium2Library, self).open_browser(url, browser,
                                                                   alias, remote_url,
                                                                   desired_capabilities,
                                                                   ff_profile_dir)
        self.wait_until_angular_ready()
        return index

    def select_all_from_list(self, locator):
        super(ExtendedSelenium2Library, self).select_all_from_list(locator)
        self._angular_element_trigger_change(locator)

    def select_checkbox(self, locator):
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)

        if self._is_angular_control(element):
            self._angular_select_checkbox_or_radio_button(element)
        else:
            if not element.is_selected():
                element.click()

    def select_from_list(self, locator, *items):
        super(ExtendedSelenium2Library, self).select_from_list(locator, *items)
        self._angular_element_trigger_change(locator)

    def select_from_list_by_index(self, locator, *indexes):
        super(ExtendedSelenium2Library, self).select_from_list_by_index(locator, *indexes)
        self._angular_element_trigger_change(locator)

    def select_from_list_by_label(self, locator, *labels):
        super(ExtendedSelenium2Library, self).select_from_list_by_label(locator, *labels)
        self._angular_element_trigger_change(locator)

    def select_from_list_by_value(self, locator, *values):
        super(ExtendedSelenium2Library, self).select_from_list_by_value(locator, *values)
        self._angular_element_trigger_change(locator)

    def select_radio_button(self, group_name, value):
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)

        if self._is_angular_control(element):
            self._angular_select_checkbox_or_radio_button(element)
        else:
            if not element.is_selected():
                element.click()

    def submit_form(self, locator):
        super(ExtendedSelenium2Library, self).submit_form(locator)
        self.wait_until_angular_ready()

    def wait_until_angular_ready(self, timeout=None, error=None):
        if self._is_angular_page():
            if not timeout:
                timeout = self._timeout_in_secs

            if not error:
                error = 'AngularJS is not ready in %ss.' % timeout

            js = self.NG_WRAPPER % {'prefix': 'document.%s=false;' % self.NG_READY,
                                    'handler': 'function(){document.%s=true}' % self.NG_READY}

            self._debug("Executing JavaScript:\n%s" % js)
            self._current_browser().execute_script(js)
            self.wait_for_condition('return document.%s' % self.NG_READY, timeout, error)

    def _angular_element_trigger_change(self, locator):
        element = self._element_find(locator, True, True)

        if element is None:
            raise ValueError("Element '%s' not found." % locator)

        if self._is_angular_control(element):
            # you will operating in different scope
            js = self.NG_WRAPPER % {'prefix': 'var obj=arguments[0];',
                                    'handler': 'function(){angular.element(obj).triggerHandler(\'change\')}'}

            self._debug("Executing JavaScript:\n%s" % js)
            self._current_browser().execute_script(js, element)
            self.wait_until_angular_ready()

    def _angular_select_checkbox_or_radio_button(self, element):
        if element is None:
            raise ValueError("Element not found.")

        if self._is_angular_control(element):
            # you will operating in different scope
            js = self.NG_WRAPPER % {'prefix': 'var obj=arguments[0];',
                                    'handler': 'function(){angular.element(obj).prop(\'checked\',true).'
                                    'triggerHandler(\'click\')}'}

            self._debug("Executing JavaScript:\n%s" % js)
            self._current_browser().execute_script(js, element)
            self.wait_until_angular_ready()

    def _is_angular_control(self, element):
        self._debug('Validating Angular control: %s' % element.get_attribute('outerHTML'))
        return element.get_attribute('ng-model') != '' or element.get_attribute('data-ng-model') != ''

    def _is_angular_page(self):
        js = 'return !!(window.angular && window.angular.version)'
        self._debug("Executing JavaScript:\n%s" % js)
        return self._current_browser().execute_script(js)