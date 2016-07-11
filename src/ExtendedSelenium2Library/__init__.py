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

from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import Selenium2Library
from ExtendedSelenium2Library.decorators import inherit_docs
from ExtendedSelenium2Library.keywords import ExtendedElementKeywords
from ExtendedSelenium2Library.keywords import ExtendedFormElementKeywords
from ExtendedSelenium2Library.keywords import ExtendedJavascriptKeywords
from ExtendedSelenium2Library.keywords import ExtendedSelectElementKeywords
from ExtendedSelenium2Library.keywords import ExtendedWaitingKeywords
from ExtendedSelenium2Library.version import get_version

__version__ = get_version()


# pylint: disable=too-many-ancestors
@inherit_docs
class ExtendedSelenium2Library(Selenium2Library, ExtendedElementKeywords,
                               ExtendedFormElementKeywords, ExtendedJavascriptKeywords,
                               ExtendedSelectElementKeywords, ExtendedWaitingKeywords):
    # pylint: disable=line-too-long
    """ExtendedSelenium2Library is a [http://goo.gl/boVQia|Selenium2 (WebDriver)]
    web testing library with [https://goo.gl/Kzz8Y3|AngularJS] support and
    custom improvement for [http://goo.gl/lES6WM|Robot Framework].

    ExtendedSelenium2Library strives to make the transition from
    [https://goo.gl/1VXDSI|Selenium2Library] as seamless as possible.
    It uses [http://goo.gl/boVQia|Selenium2 (WebDriver)] libraries
    and [https://goo.gl/Kzz8Y3|AngularJS] synchronization internally to control a web browser
    and ensure all the keywords stay in sync with [https://goo.gl/Kzz8Y3|AngularJS] process.

    See `Wait Until Angular Ready` keyword for a list of all other keywords that is already
    calling `Wait Until Angular Ready` from within.
    See [http://goo.gl/boVQia|Selenium2 and WebDriver] for more information.

    ExtendedSelenium2Library runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    Non-inherited Keywords:
    | `Element Attribute Should Contain`                 |
    | `Element Attribute Should Not Contain`             |
    | `Execute Async Javascript With Replaced Variables` |
    | `Execute Javascript With Replaced Variables`       |
    | `Fast Wait Until Page Contains`                    |
    | `Get Browser Logs`                                 |
    | `Get Screen Size`                                  |
    | `Is Element Visible`                               |
    | `Register Page Ready Keyword`                      |
    | `Remove Page Ready Keyword`                        |
    | `Scroll Element Into View`                         |
    | `Wait For Async Condition`                         |
    | `Wait For Condition With Replaced Variables`       |
    | `Wait Until Angular Ready`                         |
    | `Wait Until Element Contains Attribute`            |
    | `Wait Until Element Does Not Contain Attribute`    |
    | `Wait Until Location Contains`                     |
    | `Wait Until Location Does Not Contain`             |
    | `Warn Any Javascript Errors`                       |

    AngularJS Locators Support:
    | *AngularJS Strategy* | *Example*                                         | *Description*                                        |
    | model                | Click Element   `|` model=model_name              | Matches by AngularJS model name                      |
    | binding              | Click Element   `|` binding=binding_name          | Matches by AngularJS binding name                    |
    | partial binding      | Click Element   `|` partial binding=binding_name  | Matches by partial AngularJS binding name            |
    | button               | Click Element   `|` button=My Button              | Matches button elements by their button text         |
    | partial button       | Click Element   `|` partial button=y But          | Matches button elements by their partial button text |
    | options              | Get WebElements `|` options=options_descriptor    | Matches by AngularJS options descriptor              |

    = Before running tests =

    Prior to running test cases using ExtendedSelenium2Library, ExtendedSelenium2Library must be
    imported into your Robot test suite (see `importing` section), and the
    `Open Browser` keyword must be used to open a browser to the desired location.
    """
    # pylint: disable=line-too-long

    # let's not confuse people with different name and version
    __doc__ += Selenium2Library.__doc__.split('desired location.', 1)[-1]. \
        replace('Selenium2Library', 'ExtendedSelenium2Library'). \
        replace('version 1.7', 'version 0.4.9'). \
        replace('Version 1.7.0', 'version 0.4.9')

    JQUERY_URL = '//code.jquery.com/jquery-1.11.3.min.js'
    JQUERY_BOOTSTRAP = 'var a=document.getElementsByTagName(\'head\')[0];' \
                       'var b=document.createElement(\'script\');' \
                       'b.type=\'text/javascript\';b.src=document.location.' \
                       'protocol+\'%(jquery_url)s\';a.appendChild(b);'
    NG_WRAPPER = '%(prefix)s' \
                 'var $inj;try{$inj=angular.element(document.querySelector(' \
                 '\'[data-ng-app],[ng-app],.ng-scope\')||document).injector()||' \
                 'angular.injector([\'ng\'])}catch(ex){' \
                 '$inj=angular.injector([\'ng\'])};$inj.get=$inj.get||$inj;' \
                 '$inj.get(\'$browser\').notifyWhenNoOutstandingRequests(%(handler)s)' \
                 '%(suffix)s'
    PAGE_READY_WRAPPER = 'var cb=arguments[arguments.length-1];if(window.jQuery){' \
                         '$(document).ready(function(){cb(true)})}else{'\
                         '%(jquery_bootstrap)s' \
                         'cb(document.readyState===\'complete\' && document.body && ' \
                         'document.body.childNodes.length)}'
    ROBOT_EXIT_ON_FAILURE = True
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, implicit_wait=15.0, **kwargs):
        # pylint: disable=line-too-long
        """ExtendedSelenium2Library can be imported with optional arguments.

        Arguments:
        - ``timeout``: The maximum value to wait for all waiting actions. (Default 5.0)
                       It can be set later with `Set Selenium Timeout`.
                       See `introduction` for more information about ``timeout``.
        - ``implicit_wait``: The maximum implicit timeout value to wait when looking
                             for elements. (Default 15.0)
                             It can be later set with `Set Selenium Implicit Wait`.
                             See [http://goo.gl/8ePMo6|WebDriver: Advanced Usage]
                             section of the SeleniumHQ documentation for more information about
                             WebDriver's implicit wait functionality.
        - ``run_on_failure``: The name of a keyword (from any available libraries) to execute
                              when a ExtendedSelenium2Library keyword fails. By default
                              `Capture Page Screenshot` will be used to take a screenshot of
                              the current page.
                              Using the value "Nothing" will disable this feature altogether.
                              See `Register Keyword To Run On Failure` keyword for
                              more information about this functionality.
        - ``screenshot_root_directory``: The default root directory that screenshots should be
                                         stored in. If not provided, the default directory will be
                                         where [http://goo.gl/lES6WM|Robot Framework] places its
                                         logfile.
        - ``block_until_page_ready``: A boolean flag to block the execution until
                                      the page is ready. (Default True)
        - ``browser_breath_delay``: The delay value in seconds to give the browser enough time to
                                    complete current execution. (Default 0.05)
        - ``ensure_jq``: A boolean flag to ensure jQuery library is loaded on the page.
                         ``sizzle`` locator strategy will depend on this flag. (Default True)
        - ``poll_frequency``: The delay value in seconds to retry the next step. (Default 0.2)

        Examples:
        | Library `|` ExtendedSelenium2Library `|` 15                                            | # Sets default timeout to 15 seconds                                       |
        | Library `|` ExtendedSelenium2Library `|` 0 `|` 5                                       | # Sets default timeout to 0 seconds and default implicit_wait to 5 seconds |
        | Library `|` ExtendedSelenium2Library `|` 5 `|` run_on_failure=Log Source               | # Sets default timeout to 5 seconds and runs `Log Source` on failure       |
        | Library `|` ExtendedSelenium2Library `|` implicit_wait=5 `|` run_on_failure=Log Source | # Sets default implicit_wait to 5 seconds and runs `Log Source` on failure |
        | Library `|` ExtendedSelenium2Library `|` timeout=10      `|` run_on_failure=Nothing    | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        # pylint: disable=line-too-long
        self._inputs = {
            'block_until_page_ready': bool(kwargs.pop('block_until_page_ready', True)),
            'browser_breath_delay': float(kwargs.pop('browser_breath_delay', 0.05)),
            'ensure_jq': bool(kwargs.pop('ensure_jq', True)),
            'poll_frequency': float(kwargs.pop('poll_frequency', 0.2)),
        }
        self._builtin = BuiltIn()
        Selenium2Library.__init__(self, implicit_wait=implicit_wait, **kwargs)
        ExtendedElementKeywords.__init__(self)
        ExtendedFormElementKeywords.__init__(self)
        ExtendedJavascriptKeywords.__init__(self)
        ExtendedSelectElementKeywords.__init__(self)
        ExtendedWaitingKeywords.__init__(self)
        self._implicit_wait_in_secs = float(implicit_wait) if implicit_wait is not None else 15.0
        self._page_ready_keyword_list = []
        # pylint: disable=protected-access
        self._table_element_finder._element_finder = self._element_finder

    def get_browser_logs(self):
        """Returns the Javascript console logs from the browser. (Non Internet Explorer only).

        Please see [https://goo.gl/S7yvqR|Logging Preferences JSON object] to set
        how verbose the logging should be. (Default 'SEVERE')

        Examples:
        | Get Browser Logs |
        """
        # IEDriverServer doesn't have log implementation yet
        return [] if self._is_internet_explorer() else self._current_browser().get_log('browser')

    def get_location(self):
        # AngularJS support
        response = self._wait_until_page_ready(handler='function(){cb(location.href)}',
                                               suffix='}else{cb(location.href)}',
                                               timeout=self._implicit_wait_in_secs)['response']
        # retry with sync approach
        if response is None:
            response = self._current_browser().execute_script('return location.href')
        # fallback
        if response is None:
            response = self._current_browser().get_current_url()
        return response

    # pylint: disable=arguments-differ
    # pylint: disable=too-many-arguments
    def open_browser(self, url, browser='firefox', alias=None, remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None, skip_ready=False):
        index = super(ExtendedSelenium2Library, self).\
            open_browser(url, browser, alias, remote_url, desired_capabilities, ff_profile_dir)
        if not skip_ready:
            self._wait_until_page_ready()
        return index

    def register_page_ready_keyword(self, keyword_name):
        """Adds a keyword to be run at the end of the wait until page ready keyword.

        Arguments:
        - ``keyword_name``: Adds existing keyword name to be run when the page is ready.

        Examples:
        | Register Page Ready Keyword | My Keyword |
        """
        self._page_ready_keyword_list.append(keyword_name)

    def remove_page_ready_keyword(self, keyword_name):
        """Removes a keyword to be run at the end of the wait until page ready keyword.

        Arguments:
        - ``keyword_name``: Removes existing keyword name from running when the page is ready.

        Examples:
        | Remove Page Ready Keyword | My Keyword |
        """
        self._page_ready_keyword_list.remove(keyword_name)
