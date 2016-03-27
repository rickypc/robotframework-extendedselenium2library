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
from ExtendedSelenium2Library.keywords import ExtendedSelectElementKeywords
from Selenium2Library.keywords import _SelectElementKeywords


class ExtendedSelectElementTests(unittest.TestCase):
    """Extended select element keyword test class."""

    def setUp(self):
        """Instantiate the extended select element class."""
        self.element = ExtendedSelectElementKeywords()
        self.indexes = (1, 2, 3, 4, 5)
        self.items = ('1', '2', '3', '4', '5')
        self.labels = ('1', '2', '3', '4', '5')
        self.locator = 'css=.selector'
        self.values = ('1', '2', '3', '4', '5')

    def test_should_inherit_keywords(self):
        """Extended select element instance should inherit Selenium2 select element instances."""
        self.assertIsInstance(self.element, _SelectElementKeywords)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedselectelement."
                "_SelectElementKeywords.select_all_from_list")
    def test_should_select_all_from_list(self, mock_select_all_from_list):
        """Should select all option items from list."""
        # pylint: disable=protected-access
        self.element._element_trigger_change = mock.Mock()
        self.element.select_all_from_list(self.locator)
        mock_select_all_from_list.assert_called_with(self.locator)
        self.element._element_trigger_change.assert_called_with(self.locator)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedselectelement."
                "_SelectElementKeywords.select_from_list")
    def test_should_select_from_list(self, mock_select_from_list):
        """Should select option items from list by item."""
        # pylint: disable=protected-access
        self.element._element_trigger_change = mock.Mock()
        self.element.select_from_list(self.locator, self.items)
        mock_select_from_list.assert_called_with(self.locator, self.items)
        self.element._element_trigger_change.assert_called_with(self.locator)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedselectelement."
                "_SelectElementKeywords.select_from_list_by_index")
    def test_should_select_from_list_by_index(self, mock_select_from_list_by_index):
        """Should select option items from list by index."""
        # pylint: disable=protected-access
        self.element._element_trigger_change = mock.Mock()
        self.element.select_from_list_by_index(self.locator, self.indexes)
        mock_select_from_list_by_index.assert_called_with(self.locator, self.indexes)
        self.element._element_trigger_change.assert_called_with(self.locator)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedselectelement."
                "_SelectElementKeywords.select_from_list_by_label")
    def test_should_select_from_list_by_label(self, mock_select_from_list_by_label):
        """Should select option items from list by label."""
        # pylint: disable=protected-access
        self.element._element_trigger_change = mock.Mock()
        self.element.select_from_list_by_label(self.locator, self.labels)
        mock_select_from_list_by_label.assert_called_with(self.locator, self.labels)
        self.element._element_trigger_change.assert_called_with(self.locator)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedselectelement."
                "_SelectElementKeywords.select_from_list_by_value")
    def test_should_select_from_list_by_value(self, mock_select_from_list_by_value):
        """Should select option items from list by value."""
        # pylint: disable=protected-access
        self.element._element_trigger_change = mock.Mock()
        self.element.select_from_list_by_value(self.locator, self.values)
        mock_select_from_list_by_value.assert_called_with(self.locator, self.values)
        self.element._element_trigger_change.assert_called_with(self.locator)

    def test_should_trigger_change(self):
        """Should trigger change event."""
        # pylint: disable=protected-access
        self.element._wait_until_page_ready = mock.Mock()
        self.element._element_trigger_change(self.locator)
        self.element._wait_until_page_ready.\
            assert_called_with(self.locator, skip_stale_check=True,
                               prefix='var cb=arguments[arguments.length-1];'
                                      'var el=arguments[0];if(window.angular){',
                               handler='function(){$(el).trigger(\'change\').'
                                       'trigger(\'focusout\');cb(true)}')
