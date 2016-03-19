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
from ExtendedSelenium2Library.keywords import ExtendedElementKeywords
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.keywords import _ElementKeywords
import mock
import unittest


class ExtendedElementTests(unittest.TestCase):
    """Extended element keyword test class."""

    def setUp(self):
        """Instantiate the extended element class."""
        self.element = ExtendedElementKeywords()
        self.element._current_browser = mock.Mock()
        self.element._wait_until_page_ready = mock.Mock()
        self.locator = 'css=.selector'
        self.locator_attribute = 'css=.selector@class'
        self.locator_class = 'selector'
        self.web_element = WebElement('element', False)

    def test_should_inherit_keywords(self):
        """Extended element instance should inherit Selenium2 element instances."""
        self.assertIsInstance(self.element, _ElementKeywords)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_element")
    def test_should_click_element(self, mock_click_element):
        """Should click an element."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_element(self.locator)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_element.assert_called_with(self.web_element)
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_element")
    def test_should_click_elementi_and_skip_ready(self, mock_click_element):
        """Should click an element with skip_ready."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_element(self.locator, True)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_element.assert_called_with(self.web_element)
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement."
                "_ElementKeywords.click_element_at_coordinates")
    def test_should_click_element_at_coordinates(self, mock_click_element_at_coordinates):
        """Should click an element at given coordinates."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_element_at_coordinates(self.locator, 0, 0)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_element_at_coordinates.assert_called_with(self.web_element, 0, 0)
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement."
                "_ElementKeywords.click_element_at_coordinates")
    def test_should_click_element_at_coordinates_and_skip_ready(self,
                                                                mock_click_element_at_coordinates):
        """Should click an element at given coordinates with skip_ready."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_element_at_coordinates(self.locator, 0, 0, True)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_element_at_coordinates.assert_called_with(self.web_element, 0, 0)
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_image")
    def test_should_click_image(self, mock_click_image):
        """Should click an image."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_image(self.locator)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_image.assert_called_with(self.web_element)
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_image")
    def test_should_click_image_and_skip_ready(self, mock_click_image):
        """Should click an image with skip_ready."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_image(self.locator, True)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_image.assert_called_with(self.web_element)
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_link")
    def test_should_click_link(self, mock_click_link):
        """Should click a link."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_link(self.locator)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_link.assert_called_with(self.web_element)
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement._ElementKeywords.click_link")
    def test_should_click_link_and_skip_ready(self, mock_click_link):
        """Should click a link with skip_ready."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.click_link(self.locator, True)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_click_link.assert_called_with(self.web_element)
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement."
                "_ElementKeywords.double_click_element")
    def test_should_double_click_element(self, mock_double_click_element):
        """Should double click an element."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.double_click_element(self.locator)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_double_click_element.assert_called_with(self.web_element)
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement."
                "_ElementKeywords.double_click_element")
    def test_should_double_click_element_and_skip_ready(self, mock_double_click_element):
        """Should double click an element."""
        self.element._scroll_into_view_on_internet_explorer = mock.Mock()
        self.element._scroll_into_view_on_internet_explorer.return_value = self.web_element
        self.element.double_click_element(self.locator, True)
        self.element._scroll_into_view_on_internet_explorer.assert_called_with(self.locator)
        mock_double_click_element.assert_called_with(self.web_element)
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_element_attribute_should_contain(self):
        """Element attribute should contain expected."""
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = self.locator_class
        self.element.element_attribute_should_contain(self.locator_attribute, self.locator_class)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)

    def test_element_attribute_should_raise_exception(self):
        """Element attribute should raise exception."""
        actual = 'nada'
        message = "Element attribute '%s' should have contained '%s' but its value was '%s'." %\
                  (self.locator_attribute, self.locator_class, actual)
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = actual
        with self.assertRaises(AssertionError) as context:
            self.element.element_attribute_should_contain(self.locator_attribute,
                                                          self.locator_class)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)
        self.assertEqual(' '.join(context.exception.args).strip(), message)

    def test_element_attribute_should_raise_custom_message_exception(self):
        """Element attribute should raise exception with custom message."""
        actual = 'nada'
        message = "Locator '%s' should have contained '%s' but it was '%s'." %\
                  (self.locator_attribute, self.locator_class, actual)
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = actual
        with self.assertRaises(AssertionError) as context:
            self.element.element_attribute_should_contain(self.locator_attribute,
                                                          self.locator_class,
                                                          message)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)
        self.assertEqual(' '.join(context.exception.args).strip(), message)

    def test_element_attribute_should_not_contain(self):
        """Element attribute should not contain unexpected."""
        actual = 'nada'
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = actual
        self.element.element_attribute_should_not_contain(self.locator_attribute,
                                                          self.locator_class)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)

    def test_element_attribute_not_contain_should_raise_exception(self):
        """Element attribute not contain should raise exception."""
        message = "Element attribute '%s' should not contain '%s' but it did." %\
                  (self.locator_attribute, self.locator_class)
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = self.locator_class
        with self.assertRaises(AssertionError) as context:
            self.element.element_attribute_should_not_contain(self.locator_attribute,
                                                              self.locator_class)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)
        self.assertEqual(' '.join(context.exception.args).strip(), message)

    def test_element_attribute_not_contain_should_raise_custom_message_exception(self):
        """Element attribute not contain should raise exception with custom message."""
        message = "Locator '%s' should not contain '%s' but it did." %\
                  (self.locator_attribute, self.locator_class)
        self.element.get_element_attribute = mock.Mock()
        self.element.get_element_attribute.return_value = self.locator_class
        with self.assertRaises(AssertionError) as context:
            self.element.element_attribute_should_not_contain(self.locator_attribute,
                                                              self.locator_class,
                                                              message)
        self.element.get_element_attribute.assert_called_with(self.locator_attribute)
        self.assertEqual(' '.join(context.exception.args).strip(), message)

    def test_is_element_visible(self):
        """Element should be visible."""
        self.element._is_visible = mock.Mock()
        self.element._is_visible.return_value = True
        self.assertTrue(self.element.is_element_visible(self.locator))
        self.element._is_visible.assert_called_with(self.locator)

    def test_is_element_not_visible(self):
        """Element should not be visible."""
        self.element._is_visible = mock.Mock()
        self.element._is_visible.return_value = False
        self.assertFalse(self.element.is_element_visible(self.locator))
        self.element._is_visible.assert_called_with(self.locator)

    def test_scroll_element_into_view(self):
        """Scroll element into view."""
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._current_browser().execute_script = mock.Mock()
        self.assertEqual(self.element.scroll_element_into_view(self.locator),
                         self.web_element)
        self.element._element_find.assert_called_with(self.locator, True, True)
        self.element._current_browser().\
            execute_script.assert_called_with('arguments[0].scrollIntoView()',
                                              self.web_element)

    def test_scroll_element_into_view_raise_exception(self):
        """Scroll element into view raise exception."""
        message = "Element '%s' not found." % self.locator
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = None
        with self.assertRaises(AssertionError) as context:
            self.assertIsNone(self.element.scroll_element_into_view(self.locator))
        self.assertEqual(' '.join(context.exception.args).strip(), message)
        self.element._element_find.assert_called_with(self.locator, True, True)
        self.assertFalse(self.element._current_browser().execute_script.called)

    def test_get_browser_name(self):
        """Should return browser name."""
        self.element._current_browser().capabilities = {'browserName': 'chrome'}
        self.assertEqual(self.element._get_browser_name(), 'chrome')

    def test_is_internet_explorer(self):
        """Browser name should be internet explorer."""
        self.element._get_browser_name = mock.Mock()
        self.element._get_browser_name.return_value = 'ie'
        self.assertTrue(self.element._is_internet_explorer())
        self.element._get_browser_name.assert_called_with()

    def test_is_not_internet_explorer(self):
        """Browser name should not be internet explorer."""
        self.element._get_browser_name = mock.Mock()
        self.assertFalse(self.element._is_internet_explorer('chrome'))
        self.assertFalse(self.element._get_browser_name.called)

    def test_scroll_into_view_on_internet_explorer(self):
        """Should scroll into view on internet explorer."""
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._is_internet_explorer = mock.Mock()
        self.element._is_internet_explorer.return_value = True
        self.element.scroll_element_into_view = mock.Mock()
        self.assertEqual(self.element._scroll_into_view_on_internet_explorer(self.locator),
                         self.web_element)
        self.element._element_find.assert_called_with(self.locator, True, True)
        self.element._is_internet_explorer.assert_called_with()
        self.element.scroll_element_into_view.assert_called_with(self.web_element)

    def test_not_scroll_into_view_on_non_internet_explorer(self):
        """Should not scroll into view on non internet explorer."""
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._is_internet_explorer = mock.Mock()
        self.element._is_internet_explorer.return_value = False
        self.element.scroll_element_into_view = mock.Mock()
        self.assertEqual(self.element._scroll_into_view_on_internet_explorer(self.locator),
                         self.web_element)
        self.element._element_find.assert_called_with(self.locator, True, True)
        self.element._is_internet_explorer.assert_called_with()
        self.assertFalse(self.element.scroll_element_into_view.called)
