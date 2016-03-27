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
from ExtendedSelenium2Library.keywords import ExtendedElementKeywords
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.keywords import _ElementKeywords


class ExtendedElementTests(unittest.TestCase):
    """Extended element keyword test class."""

    def setUp(self):
        """Instantiate the extended element class."""
        self.driver = mock.Mock()
        self.driver.session_id = 'session'
        self.element = ExtendedElementKeywords()
        # pylint: disable=protected-access
        self.element._current_browser = mock.Mock()
        self.element._info = mock.Mock()
        self.element._wait_until_page_ready = mock.Mock()
        self.locator = 'css=.selector'
        self.locator_attribute = 'css=.selector@class'
        self.locator_class = 'selector'
        self.web_element = WebElement(self.driver, 'element', False)
        self.web_element.click = mock.Mock()

    def test_should_inherit_keywords(self):
        """Extended element instance should inherit Selenium2 element instances."""
        self.assertIsInstance(self.element, _ElementKeywords)

    def test_should_click_element(self):
        """Should click an element."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_element(self.locator)
        self.element._info.assert_called_with("Clicking element '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_element_and_skip_ready(self):
        """Should click an element with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_element(self.locator, True)
        self.element._info.assert_called_with("Clicking element '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement.ActionChains")
    def test_should_click_element_at_coordinates(self, mock_action_chains):
        """Should click an element at given coordinates."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_element_at_coordinates(self.locator, 0, 0)
        self.element._info.assert_called_with("Clicking element '%s' in coordinates '%s', '%s'." %
                                              (self.locator, 0, 0))
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        mock_action_chains.assert_called_with(self.element._current_browser())
        action_chains = mock_action_chains(self.element._current_browser())
        action_chains.move_to_element.assert_called_with(self.web_element)
        move_to_element = action_chains.move_to_element(self.web_element)
        move_to_element.move_by_offset.assert_called_with(0, 0)
        move_by_offset = move_to_element.move_by_offset(0, 0)
        move_by_offset.click.assert_called_with()
        click = move_by_offset.click()
        click.perform.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement.ActionChains")
    def test_should_click_el_at_coords_and_skip_ready(self, mock_action_chains):
        """Should click an element at given coordinates with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_element_at_coordinates(self.locator, 0, 0, True)
        self.element._info.assert_called_with("Clicking element '%s' in coordinates '%s', '%s'." %
                                              (self.locator, 0, 0))
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        mock_action_chains.assert_called_with(self.element._current_browser())
        action_chains = mock_action_chains(self.element._current_browser())
        action_chains.move_to_element.assert_called_with(self.web_element)
        move_to_element = action_chains.move_to_element(self.web_element)
        move_to_element.move_by_offset.assert_called_with(0, 0)
        move_by_offset = move_to_element.move_by_offset(0, 0)
        move_by_offset.click.assert_called_with()
        click = move_by_offset.click()
        click.perform.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_click_image(self):
        """Should click an image."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_image(self.locator)
        self.element._info.assert_called_with("Clicking image '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, False, 'image')
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_image_and_skip_ready(self):
        """Should click an image with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_image(self.locator, True)
        self.element._info.assert_called_with("Clicking image '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, False, 'image')
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_click_input_image(self):
        """Should click an input image."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.side_effect = \
            [None, self.web_element]
        self.element.click_image(self.locator)
        self.element._info.assert_called_with("Clicking image '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, True, 'input')
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_input_image_and_skip_ready(self):
        """Should click an input image with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.side_effect = \
            [None, self.web_element]
        self.element.click_image(self.locator, True)
        self.element._info.assert_called_with("Clicking image '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, True, 'input')
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    def test_should_click_link(self):
        """Should click a link."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_link(self.locator)
        self.element._info.assert_called_with("Clicking link '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, tag='a')
        self.web_element.click.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    def test_should_click_link_and_skip_ready(self):
        """Should click a link with skip_ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.click_link(self.locator, True)
        self.element._info.assert_called_with("Clicking link '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.\
            assert_called_with(self.locator, tag='a')
        self.web_element.click.assert_called_with()
        self.assertFalse(self.element._wait_until_page_ready.called)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement.ActionChains")
    def test_should_double_click_element(self, mock_action_chains):
        """Should double click an element."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.double_click_element(self.locator)
        self.element._info.assert_called_with("Double clicking element '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        mock_action_chains.assert_called_with(self.element._current_browser())
        action_chains = mock_action_chains(self.element._current_browser())
        action_chains.double_click.assert_called_with(self.web_element)
        double_click = action_chains.double_click(self.web_element)
        double_click.perform.assert_called_with()
        self.element._wait_until_page_ready.assert_called_with()

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement.ActionChains")
    def test_should_double_click_element_and_skip_ready(self, mock_action_chains):
        """Should double click an element with skip ready."""
        # pylint: disable=protected-access
        self.element._get_element_and_scroll_into_view_on_iexplore = mock.Mock()
        self.element._get_element_and_scroll_into_view_on_iexplore.return_value = self.web_element
        self.element.double_click_element(self.locator, True)
        self.element._info.assert_called_with("Double clicking element '%s'." % self.locator)
        self.element._get_element_and_scroll_into_view_on_iexplore.assert_called_with(self.locator)
        mock_action_chains.assert_called_with(self.element._current_browser())
        action_chains = mock_action_chains(self.element._current_browser())
        action_chains.double_click.assert_called_with(self.web_element)
        double_click = action_chains.double_click(self.web_element)
        double_click.perform.assert_called_with()
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

    def test_el_attr_should_raise_custom_msg_exception(self):
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

    def test_el_attr_not_contain_should_raise_exception(self):
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

    def test_el_attr_not_contain_raise_custom_msg_ex(self):
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
        # pylint: disable=protected-access
        self.element._is_visible = mock.Mock()
        self.element._is_visible.return_value = True
        self.assertTrue(self.element.is_element_visible(self.locator))
        self.element._is_visible.assert_called_with(self.locator)

    def test_is_element_not_visible(self):
        """Element should not be visible."""
        # pylint: disable=protected-access
        self.element._is_visible = mock.Mock()
        self.element._is_visible.return_value = False
        self.assertFalse(self.element.is_element_visible(self.locator))
        self.element._is_visible.assert_called_with(self.locator)

    @mock.patch("ExtendedSelenium2Library.keywords.extendedelement.logger")
    def test_scroll_element_into_view(self, mock_logger):
        """Scroll element into view."""
        # pylint: disable=protected-access
        self.element._current_browser().execute_script = mock.Mock()
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.assertEqual(self.element.scroll_element_into_view(self.locator),
                         self.web_element)
        mock_logger.info.assert_called_with("Scrolling element '%s' into view." % self.locator)
        self.element._element_find.assert_called_with(self.locator, True, True)
        self.element._current_browser().\
            execute_script.assert_called_with('arguments[0].scrollIntoView()',
                                              self.web_element)

    def test_scroll_element_into_view_with_web_element(self):
        """Scroll element into view with web element."""
        # pylint: disable=protected-access
        self.element._current_browser().execute_script = mock.Mock()
        self.element._element_find = mock.Mock()
        self.assertEqual(self.element.scroll_element_into_view(self.web_element),
                         self.web_element)
        self.assertFalse(self.element._info.called)
        self.assertFalse(self.element._element_find.called)
        self.element._current_browser().\
            execute_script.assert_called_with('arguments[0].scrollIntoView()',
                                              self.web_element)

    def test_get_browser_name(self):
        """Should return browser name."""
        # pylint: disable=protected-access
        self.element._current_browser().capabilities = {'browserName': 'chrome'}
        self.assertEqual(self.element._get_browser_name(), 'chrome')

    def test_get_element_and_scroll_into_view_on_iexplore(self):
        """Should scroll into view on internet explorer and returns the element."""
        # pylint: disable=protected-access
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._is_internet_explorer = mock.Mock()
        self.element._is_internet_explorer.return_value = True
        self.element.scroll_element_into_view = mock.Mock()
        self.assertEqual(self.element._get_element_and_scroll_into_view_on_iexplore(self.locator),
                         self.web_element)
        self.element._element_find.assert_called_with(self.locator, True, True, None)
        self.element._is_internet_explorer.assert_called_with()
        self.element.scroll_element_into_view.assert_called_with(self.web_element)

    def test_get_el_and_not_scroll_on_non_iexplore(self):
        """Should not scroll into view on non internet explorer and returns element."""
        # pylint: disable=protected-access
        self.element._element_find = mock.Mock()
        self.element._element_find.return_value = self.web_element
        self.element._is_internet_explorer = mock.Mock()
        self.element._is_internet_explorer.return_value = False
        self.element.scroll_element_into_view = mock.Mock()
        self.assertEqual(self.element._get_element_and_scroll_into_view_on_iexplore(self.locator),
                         self.web_element)
        self.element._element_find.assert_called_with(self.locator, True, True, None)
        self.element._is_internet_explorer.assert_called_with()
        self.assertFalse(self.element.scroll_element_into_view.called)

    def test_is_internet_explorer(self):
        """Browser name should be internet explorer."""
        # pylint: disable=protected-access
        self.element._get_browser_name = mock.Mock()
        self.element._get_browser_name.return_value = 'ie'
        self.assertTrue(self.element._is_internet_explorer())
        self.element._get_browser_name.assert_called_with()

    def test_is_not_internet_explorer(self):
        """Browser name should not be internet explorer."""
        # pylint: disable=protected-access
        self.element._get_browser_name = mock.Mock()
        self.assertFalse(self.element._is_internet_explorer('chrome'))
        self.assertFalse(self.element._get_browser_name.called)
