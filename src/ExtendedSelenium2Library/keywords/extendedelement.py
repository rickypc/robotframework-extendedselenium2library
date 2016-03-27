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

from robot.api import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.keywords import _ElementKeywords
from ExtendedSelenium2Library.locators import ExtendedElementFinder


class ExtendedElementKeywords(_ElementKeywords):
    """ExtendedElementKeywords are web element execution in the requested browser."""

    def __init__(self):
        super(ExtendedElementKeywords, self).__init__()
        self._element_finder = ExtendedElementFinder()

    # pylint: disable=arguments-differ
    def click_element(self, locator, skip_ready=False):
        """Clicks an element identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Element | css=div.class |
        | Click Element | css=div.class | True |
        """
        # pylint: disable=no-member
        self._info("Clicking element '%s'." % locator)
        self._get_element_and_scroll_into_view_on_iexplore(locator).click()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_element_at_coordinates(self, locator, xoffset, yoffset, skip_ready=False):
        """Clicks an element identified by ``locator`` at x/y coordinates of the element.
        Cursor is moved at the center of the element and x/y coordinates are
        calculated from that point.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``xoffset``: The x offset value from the center of the element.
        - ``yoffset``: The y offset value from the center of the element.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Element At Coordinates | css=div.class | 0 | 0 |
        | Click Element At Coordinates | css=div.class | 0 | 0 | True |
        """
        # pylint: disable=no-member
        self._info("Clicking element '%s' in coordinates '%s', '%s'." %
                   (locator, xoffset, yoffset))
        element = self._get_element_and_scroll_into_view_on_iexplore(locator)
        # pylint: disable=no-member
        ActionChains(self._current_browser()).move_to_element(element). \
            move_by_offset(xoffset, yoffset).click().perform()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_image(self, locator, skip_ready=False):
        """Clicks an image identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested image. Key attributes for
                       arbitrary images are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Image | css=img.class |
        | Click Image | css=img.class | True |
        """
        # pylint: disable=no-member
        self._info("Clicking image '%s'." % locator)
        element = self._get_element_and_scroll_into_view_on_iexplore(locator, False, 'image')
        if element is None:
            # A form may have an image as it's submit trigger.
            element = self._get_element_and_scroll_into_view_on_iexplore(locator, True, 'input')
        element.click()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_link(self, locator, skip_ready=False):
        """Clicks a link identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested link. Key attributes for
                       arbitrary links are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Link | css=a.class |
        | Click Link | css=a.class | True |
        """
        # pylint: disable=no-member
        self._info("Clicking link '%s'." % locator)
        self._get_element_and_scroll_into_view_on_iexplore(locator, tag='a').click()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def double_click_element(self, locator, skip_ready=False):
        """Double clicks an element identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Double Click Element | css=div.class |
        | Double Click Element | css=div.class | True |
        """
        # pylint: disable=no-member
        self._info("Double clicking element '%s'." % locator)
        element = self._get_element_and_scroll_into_view_on_iexplore(locator)
        # pylint: disable=no-member
        ActionChains(self._current_browser()).double_click(element).perform()
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def element_attribute_should_contain(self, attribute_locator, expected, message=''):
        """Verifies element attribute identified by ``attribute_locator`` contains ``expected``.

        Arguments:
        - ``attribute_locator``: The locator to find requested element attribute. It consists of
                                 element locator followed by an @ sign and attribute name,
                                 for example "element_id@class".
        - ``expected``: The expected element attribute value.
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
        - ``unexpected``: The unexpected element attribute value.
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

    def scroll_element_into_view(self, locator):
        """Scrolls an element from given ``locator`` into view.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.

        Examples:
        | Scroll Element Into View | css=div.class |
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            logger.info("Scrolling element '%s' into view." % locator)
            element = self._element_find(locator, True, True)
        script = 'arguments[0].scrollIntoView()'
        # pylint: disable=no-member
        self._current_browser().execute_script(script, element)
        return element

    def _get_browser_name(self):
        """Returns current browser name."""
        # pylint: disable=no-member
        return self._current_browser().capabilities['browserName'].strip().lower()

    def _get_element_and_scroll_into_view_on_iexplore(self, locator, required=True, tag=None):
        """Scrolls a target element into view. (Internet Explorer only)."""
        element = self._element_find(locator, True, required, tag)
        if element and self._is_internet_explorer():
            self.scroll_element_into_view(element)
        return element

    def _is_internet_explorer(self, browser_name=None):
        """Returns true if current browser is Internet Explorer."""
        if not browser_name:
            browser_name = self._get_browser_name()
        browser_name = browser_name.replace(' ', '')
        return browser_name == 'internetexplorer' or browser_name == 'ie'
