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

from Selenium2Library.keywords import _FormElementKeywords


class ExtendedFormElementKeywords(_FormElementKeywords):
    """ExtendedFormElementKeywords are form element execution in the requested browser."""

    def __init__(self):
        super(ExtendedFormElementKeywords, self).__init__()

    # pylint: disable=arguments-differ
    def click_button(self, locator, skip_ready=False):
        """Clicks a button identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested button. Key attributes for
                       arbitrary buttons are ``id``, ``name``, and ``value``.
                       See `introduction` for details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Button | css=button.class |
        | Click Button | css=button.class | True |
        """
        # pylint: disable=no-member
        self._info("Clicking button '%s'." % locator)
        # pylint: disable=no-member
        element = self._get_element_and_scroll_into_view_on_iexplore(locator, False, 'input')
        if element is None:
            # pylint: disable=no-member
            element = self._get_element_and_scroll_into_view_on_iexplore(locator, True, 'button')
        element.click()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def select_checkbox(self, locator):
        """Selects checkbox identified by ``locator``.
        Does nothing if checkbox is already selected.

        Arguments:
        - ``locator``: The locator to find requested checkbox. Key attributes for
                       arbitrary checkboxes are ``id``, and ``name``.
                       See `introduction` for details about locating elements.

        Examples:
        | Select Checkbox | css=input[type="checkbox"] |
        """
        # pylint: disable=no-member
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            self._select_checkbox_or_radio_button(locator)

    def select_radio_button(self, group_name, value):
        """Sets selection of radio button group identified by ``group_name`` to ``value``.
        The XPath used to locate the correct radio button and it looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        Arguments:
        - ``group_name``: The name of the radio input
        - ``value``: The value attribute or the id attribute

        Examples:
        | # Matches HTML like <input type="radio" name="size" value="XL">XL</input> |
        | Select Radio Button | size | XL |
        | # Matches HTML like <input type="radio" name="size" value="XL" id="sizeXL">XL</input> |
        | Select Radio Button | size | sizeXL |
        """
        # pylint: disable=no-member
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            self._select_checkbox_or_radio_button('css=input[name="%s"][value="%s"]' %
                                                  (group_name, value))

    # pylint: disable=arguments-differ
    def submit_form(self, locator=None, skip_ready=False):
        """Submits a form identified by `locator`.

        Arguments:
        - ``locator``: The locator to find requested form. If ``locator`` is empty,
                       first form in the page will be submitted. Key attributes for
                       arbitrary forms are ``id``, and ``name``.
                       See `introduction` for details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Submit Form | css=form.class |
        | Submit Form | css=form.class | True |
        """
        if not locator:
            locator = 'xpath=//form'
        # pylint: disable=no-member
        self._info("Submitting form '%s'." % locator)
        # pylint: disable=no-member
        self._get_element_and_scroll_into_view_on_iexplore(locator, tag='form').submit()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    # pylint: disable=arguments-differ
    def _input_text_into_text_field(self, locator, text, skip_ready=False):
        """Send keys to text field with AngularJS synchronization."""
        # pylint: disable=no-member
        element = self._element_find(locator, True, True)
        element.clear()
        element.send_keys(text)
        if not skip_ready:
            # pylint: disable=no-member
            self._element_trigger_change(locator)

    def _select_checkbox_or_radio_button(self, locator):
        """Select checkbox or radio button with AngularJS support."""
        # pylint: disable=no-member
        self._wait_until_page_ready(locator,
                                    skip_stale_check=True,
                                    prefix='var cb=arguments[arguments.length-1];'
                                           'var el=arguments[0];if(window.angular){',
                                    handler='function(){angular.element(el).'
                                            'prop(\'checked\',true).triggerHandler(\'click\');'
                                            'cb(true)}',
                                    suffix='}else{el.click();cb(false)}')
