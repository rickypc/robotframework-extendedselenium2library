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

from Selenium2Library.keywords import _ElementKeywords
from ExtendedSelenium2Library.locators import ExtendedElementFinder


class ExtendedElementKeywords(_ElementKeywords):
    """ExtendedElementKeywords are web element related execution in the requested browser."""
    def __init__(self):
        super(ExtendedElementKeywords, self).__init__()
        self._element_finder = ExtendedElementFinder()

    # pylint: disable=arguments-differ
    def click_element(self, locator, skip_ready=False):
        """Click element identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Element | css=div.class |
        | Click Element | css=div.class | True |
        """
        element = self._scroll_into_view_on_internet_explorer(locator)
        super(ExtendedElementKeywords, self).click_element(element)
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_element_at_coordinates(self, locator, xoffset, yoffset, skip_ready=False):
        """Click element identified by ``locator`` at x/y coordinates of the element.
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
        element = self._scroll_into_view_on_internet_explorer(locator)
        super(ExtendedElementKeywords, self). \
            click_element_at_coordinates(element, xoffset, yoffset)
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_image(self, locator, skip_ready=False):
        """Click an image identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested image. Key attributes for
                       arbitrary images are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Image | css=div.class |
        | Click Image | css=div.class | True |
        """
        element = self._scroll_into_view_on_internet_explorer(locator)
        super(ExtendedElementKeywords, self).click_image(element)
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def click_link(self, locator, skip_ready=False):
        """Click a link identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested link. Key attributes for
                       arbitrary links are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Click Link | css=div.class |
        | Click Link | css=div.class | True |
        """
        element = self._scroll_into_view_on_internet_explorer(locator)
        super(ExtendedElementKeywords, self).click_link(element)
        if not skip_ready:
            # pylint: disable=no-member
            self._wait_until_page_ready()

    def double_click_element(self, locator, skip_ready=False):
        """Double click element identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``skip_ready``: A boolean flag to skip the wait for page ready. (Default False)

        Examples:
        | Double Click Element | css=div.class |
        | Double Click Element | css=div.class | True |
        """
        element = self._scroll_into_view_on_internet_explorer(locator)
        super(ExtendedElementKeywords, self).double_click_element(element)
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
        """Scroll element from given ``locator`` into view.

        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.

        Examples:
        | Scroll Element Into View | css=div.class |
        """
        element = self._element_find(locator, True, True)
        if element is None:
            raise AssertionError("Element '%s' not found." % locator)
        script = 'arguments[0].scrollIntoView()'
        # pylint: disable=no-member
        self._current_browser().execute_script(script, element)
        return element

    def _get_browser_name(self):
        """Returns current browser name."""
        # pylint: disable=no-member
        return self._current_browser().capabilities['browserName'].strip().lower()

    def _is_internet_explorer(self, browser_name=None):
        """Returns true if current browser is Internet Explorer."""
        if not browser_name:
            browser_name = self._get_browser_name()
        return browser_name == 'internetexplorer' or browser_name == 'ie'

    def _scroll_into_view_on_internet_explorer(self, locator):
        """Scroll target element into view. (Internet Explorer only)."""
        element = self._element_find(locator, True, True)
        if self._is_internet_explorer():
            self.scroll_element_into_view(element)
        return element
