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

from Selenium2Library.locators import ElementFinder


class ExtendedElementFinder(ElementFinder):
    """ExtendedElementFinder is a web element finder with
    [https://goo.gl/00Q8qX|Protractor locators] support."""

    BUTTON_TEXT_WRAPPER = "return [].filter.call(document.querySelectorAll('button," \
                          "input[type=\"button\"],input[type=\"submit\"]')," \
                          "function(item){var text=(item.nodeName.toLowerCase()==='button')?" \
                          "(item.textContent||item.innerText||''):item.value;%(handler)s})"

    NG_BINDING_WRAPPER = "return [].filter.call(document.getElementsByClassName('ng-binding')," \
                         "function(item){var binding=angular.element(item).data('$binding');" \
                         "if(binding){var name=binding.exp||binding[0].exp||binding;%(handler)s}})"

    def __init__(self):
        ElementFinder.__init__(self)
        strategies = {
            'binding': self._find_by_ng_binding,
            'button': self._find_by_button_text,
            'model': self._find_by_ng_model,
            'options': self._find_by_ng_options,
            'partial binding': self._find_by_ng_binding_partial,
            'partial button': self._find_by_button_text_partial
        }
        self._strategies.update(strategies)
        self._default_strategies = list(self._strategies.keys())
        self._ng_prefixes = ['ng-', 'data-ng-', 'ng_', 'x-ng-', 'ng\\:']

    def _find_by_button_text(self, browser, button_text, tag, constraints):
        """Find button matches by exact text."""
        # pylint: disable=anomalous-backslash-in-string
        script = self.BUTTON_TEXT_WRAPPER \
            % {'handler': "return text.replace(/^\s+|\s+$/g,'')==='%s'" % button_text}
        return self._filter_elements(browser.execute_script(script), tag, constraints)

    def _find_by_button_text_partial(self, browser, button_text, tag, constraints):
        """Find button matches by partial text."""
        script = self.BUTTON_TEXT_WRAPPER % \
            {'handler': "return text.indexOf('%s')>-1" % button_text}
        return self._filter_elements(browser.execute_script(script), tag, constraints)

    def _find_by_ng_binding(self, browser, binding_name, tag, constraints):
        """Find element matches by exact binding name."""
        # pylint: disable=anomalous-backslash-in-string
        script = self.NG_BINDING_WRAPPER % \
            {'handler': ("var matcher=new RegExp('({|\\s|^|\\|)'+'%s'."
                         # See http://stackoverflow.com/q/3561711
                         "replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g,'\\$&')"
                         "+'(}|\\s|$|\\|)');return matcher.test(name)") % binding_name}
        return self._filter_elements(browser.execute_script(script), tag, constraints)

    def _find_by_ng_binding_partial(self, browser, binding_name, tag, constraints):
        """Find element matches by partial binding name."""
        script = self.NG_BINDING_WRAPPER % \
            {'handler': "return name.indexOf('%s')>-1" % binding_name}
        return self._filter_elements(browser.execute_script(script), tag, constraints)

    def _find_by_ng_model(self, browser, model_name, tag, constraints):
        """Find element matches by exact model name."""
        stem = 'model="%s"' % model_name
        joiner = '%s],[' % stem
        criteria = '[' + joiner.join(self._ng_prefixes) + stem + ']'
        return self._find_by_css_selector(browser, criteria, tag, constraints)

    def _find_by_ng_options(self, browser, descriptor, tag, constraints):
        """Find options matches by exact descriptor."""
        stem = 'options="%s"' % descriptor
        joiner = '%s] option,[' % stem
        criteria = '[' + joiner.join(self._ng_prefixes) + stem + '] option'
        return self._find_by_css_selector(browser, criteria, tag, constraints)
