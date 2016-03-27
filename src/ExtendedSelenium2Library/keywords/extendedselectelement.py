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

from Selenium2Library.keywords import _SelectElementKeywords


class ExtendedSelectElementKeywords(_SelectElementKeywords):
    """ExtendedSelectElementKeywords are select element execution in the requested browser."""

    def __init__(self):
        super(ExtendedSelectElementKeywords, self).__init__()

    def select_all_from_list(self, locator):
        """Selects all values from multi-select list identified by ``locator``.

        Arguments:
        - ``locator``: The locator to find requested select list. Key attributes for
                       select lists are ``id`` and ``name``. See `introduction` for
                       details about locating elements.

        Examples:
        | Select All From List | css=select.class |
        """
        super(ExtendedSelectElementKeywords, self).select_all_from_list(locator)
        self._element_trigger_change(locator)

    def select_from_list(self, locator, *items):
        """Selects ``*items`` from list identified by ``locator``

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and ``*items`` is an empty list, all values of the list will be selected.

        It's faster to use 'by index/value/label' keywords.

        An exception is raised for a single-selection list if the last
        value does not exist in the list and a warning for all other non-
        existing items. For a multi-selection list, an exception is raised
        for any and all non-existing values.

        Select list keywords work on both lists and combo boxes.

        Arguments:
        - ``locator``: The locator to find requested select list. Key attributes for
                       select lists are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``*items``: A list of items where it will be use to try to select
                      by value then by label.

        Examples:
        | Select From List | css=select.class | item |
        """
        super(ExtendedSelectElementKeywords, self).select_from_list(locator, *items)
        self._element_trigger_change(locator)

    def select_from_list_by_index(self, locator, *indexes):
        """Selects ``*indexes`` from list identified by ``locator``.
        Select list keywords work on both lists and combo boxes.

        Arguments:
        - ``locator``: The locator to find requested select list. Key attributes for
                       select lists are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``*indexes``: A list of indexes to be selected.

        Examples:
        | Select From List By Index | css=select.class | index |
        """
        super(ExtendedSelectElementKeywords, self).select_from_list_by_index(locator, *indexes)
        self._element_trigger_change(locator)

    def select_from_list_by_label(self, locator, *labels):
        """Selects ``*labels`` from list identified by ``locator``.
        Select list keywords work on both lists and combo boxes.

        Arguments:
        - ``locator``: The locator to find requested select list. Key attributes for
                       select lists are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``*labels``: A list of labels to be selected.

        Examples:
        | Select From List By Label | css=select.class | label |
        """
        super(ExtendedSelectElementKeywords, self).select_from_list_by_label(locator, *labels)
        self._element_trigger_change(locator)

    def select_from_list_by_value(self, locator, *values):
        """Selects ``*values`` from list identified by ``locator``.
        Select list keywords work on both lists and combo boxes.

        Arguments:
        - ``locator``: The locator to find requested select list. Key attributes for
                       select lists are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        - ``*values``: A list of values to be selected.

        Examples:
        | Select From List By Value | css=select.class | value |
        """
        super(ExtendedSelectElementKeywords, self).select_from_list_by_value(locator, *values)
        self._element_trigger_change(locator)

    def _element_trigger_change(self, locator):
        """Trigger change event on target element when AngularJS is ready."""
        # pylint: disable=no-member
        self._wait_until_page_ready(locator,
                                    skip_stale_check=True,
                                    prefix='var cb=arguments[arguments.length-1];'
                                           'var el=arguments[0];if(window.angular){',
                                    handler='function(){$(el).trigger(\'change\').'
                                            'trigger(\'focusout\');cb(true)}')
