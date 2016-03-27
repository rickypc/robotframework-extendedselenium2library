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
from ExtendedSelenium2Library.keywords import ExtendedFormElementKeywords
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.keywords import _FormElementKeywords


class ExtendedFormElementTests(unittest.TestCase):
    """Extended form element keyword test class."""

    def setUp(self):
        """Instantiate the extended form element class."""
        self.driver = mock.Mock()
        self.driver.session_id = 'session'
        self.element = ExtendedFormElementKeywords()
        # pylint: disable=protected-access
        self.element._info = mock.Mock()
        self.element._wait_until_page_ready = mock.Mock()
        self.group_name = 'group'
        self.locator = 'css=.selector'
        self.value = 'value'
        self.web_element = WebElement(self.driver, 'element', False)
        self.web_element.click = mock.Mock()

    def test_should_inherit_keywords(self):
        """Extended form element instance should inherit Selenium2 form element instances."""
        self.assertIsInstance(self.element, _FormElementKeywords)

    def test_should_click_input_button(self):
        """Should click an input button."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_button(self.locator)
        self.element._info.assert_called_with("Clicking button '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, False, 'input')
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_input_button_and_skip_ready(self):
        """Should click an input button with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_button(self.locator, True)
        self.element._info.assert_called_with("Clicking button '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, False, 'input')
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_click_button(self):
        """Should click a button."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            side_effect = [None, self.web_element]
        self.element.click_button(self.locator)
        self.element._info.assert_called_with("Clicking button '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, True, 'button')
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_button_and_skip_ready(self):
        """Should click a button with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            side_effect = [None, self.web_element]
        self.element.click_button(self.locator, True)
        self.element._info.assert_called_with("Clicking button '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, True, 'button')
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_select_checkbox(self):
        """Should select a checkbox."""
        # pylint: disable=protected-access
        self.element._get_checkbox = mock.Mock()
        self.element._get_checkbox.return_value = self.web_element
        self.element._select_checkbox_or_radio_button = mock.Mock()
        self.web_element.is_selected = mock.Mock()
        self.web_element.is_selected.return_value = False
        self.element.select_checkbox(self.locator)
        self.element._info.assert_called_with("Selecting checkbox '%s'." % self.locator)
        self.element._get_checkbox.assert_called_with(self.locator)
        self.web_element.is_selected.assert_called_with()
        self.element._select_checkbox_or_radio_button.assert_called_with(self.locator)

    def test_should_ignore_selected_checkbox(self):
        """Should ignore selected checkbox."""
        # pylint: disable=protected-access
        self.element._get_checkbox = mock.Mock()
        self.element._get_checkbox.return_value = self.web_element
        self.element._select_checkbox_or_radio_button = mock.Mock()
        self.web_element.is_selected = mock.Mock()
        self.web_element.is_selected.return_value = True
        self.element.select_checkbox(self.locator)
        self.element._info.assert_called_with("Selecting checkbox '%s'." % self.locator)
        self.element._get_checkbox.assert_called_with(self.locator)
        self.web_element.is_selected.assert_called_with()
        self.assertFalse(self.element._select_checkbox_or_radio_button.called)

    def test_should_select_radio_button(self):
        """Should select a radio button."""
        # pylint: disable=protected-access
        self.element._get_radio_button_with_value = mock.Mock()
        self.element._get_radio_button_with_value.return_value = self.web_element
        self.element._select_checkbox_or_radio_button = mock.Mock()
        self.web_element.is_selected = mock.Mock()
        self.web_element.is_selected.return_value = False
        self.element.select_radio_button(self.group_name, self.value)
        self.element._info.assert_called_with("Selecting '%s' from radio button '%s'." %
                                              (self.value, self.group_name))
        self.element._get_radio_button_with_value.assert_called_with(self.group_name, self.value)
        self.web_element.is_selected.assert_called_with()
        self.element._select_checkbox_or_radio_button.\
            assert_called_with('css=input[name="%s"][value="%s"]' % (self.group_name, self.value))

    def test_should_ignore_selected_radio_button(self):
        """Should ignore selected radio button."""
        # pylint: disable=protected-access
        self.element._get_radio_button_with_value = mock.Mock()
        self.element._get_radio_button_with_value.return_value = self.web_element
        self.element._select_checkbox_or_radio_button = mock.Mock()
        self.web_element.is_selected = mock.Mock()
        self.web_element.is_selected.return_value = True
        self.element.select_radio_button(self.group_name, self.value)
        self.element._info.assert_called_with("Selecting '%s' from radio button '%s'." %
                                              (self.value, self.group_name))
        self.element._get_radio_button_with_value.assert_called_with(self.group_name, self.value)
        self.web_element.is_selected.assert_called_with()
        self.assertFalse(self.element._select_checkbox_or_radio_button.called)

    def test_should_submit_form(self):
        """Should submit form."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.web_element.submit = mock.Mock()
        self.element.submit_form(self.locator)
        self.element._info.assert_called_with("Submitting form '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore(self.locator, tag='form')
        self.web_element.submit.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_submit_form_and_skip_ready(self):
        """Should submit form with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.web_element.submit = mock.Mock()
        self.element.submit_form(self.locator, skip_ready=True)
        self.element._info.assert_called_with("Submitting form '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore(self.locator, tag='form')
        self.web_element.submit.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_submit_form_without_locator(self):
        """Should submit form without locator."""
        locator = 'xpath=//form'
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.web_element.submit = mock.Mock()
        self.element.submit_form()
        self.element._info.assert_called_with("Submitting form '%s'." % locator)
        self.element._get_element_and_scroll_into_view_on_iexplore(locator, tag='form')
        self.web_element.submit.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_submit_form_no_locator_and_skip_ready(self):
        """Should submit form without locator with skip_ready."""
        locator = 'xpath=//form'
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.web_element.submit = mock.Mock()
        self.element.submit_form(skip_ready=True)
        self.element._info.assert_called_with("Submitting form '%s'." % locator)
        self.element._get_element_and_scroll_into_view_on_iexplore(locator, tag='form')
        self.web_element.submit.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_fill_text_field(self):
        """Should fill text field."""
        # pylint: disable=protected-access
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._element_trigger_change = mock.Mock()
        self.web_element.clear = mock.Mock()
        self.web_element.send_keys = mock.Mock()
        self.element._input_text_into_text_field(self.locator, self.value)
        self.element._element_find(self.locator, True, True)
        self.web_element.clear.assert_called_with()
        self.web_element.send_keys.assert_called_with(self.value)
        self.element._element_trigger_change.assert_called_with(self.locator)

    def test_should_fill_text_field_and_skip_ready(self):
        """Should fill text field with skip_ready."""
        # pylint: disable=protected-access
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._element_trigger_change = mock.Mock()
        self.web_element.clear = mock.Mock()
        self.web_element.send_keys = mock.Mock()
        self.element._input_text_into_text_field(self.locator, self.value, True)
        self.element._element_find(self.locator, True, True)
        self.web_element.clear.assert_called_with()
        self.web_element.send_keys.assert_called_with(self.value)
        self.assertFalse(self.element._element_trigger_change.called)

    def test_should_select_checkbox_or_radio_button(self):
        """Should select checkbox or radio button."""
        # pylint: disable=protected-access
        self.element._wait_until_page_ready = mock.Mock()
        self.element._select_checkbox_or_radio_button(self.locator)
        self.element._wait_until_page_ready.\
            assert_called_with(self.locator, skip_stale_check=True,
                               prefix='var cb=arguments[arguments.length-1];'
                                      'var el=arguments[0];if(window.angular){',
                               handler='function(){angular.element(el).'
                                       'prop(\'checked\',true).triggerHandler(\'click\');'
                                       'cb(true)}',
                               suffix='}else{el.click();cb(false)}')
