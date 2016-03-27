0.9.0 (2016.03.26)
==================

* Bugfixes on issue #9 and issue #11
* Refactors form and select elements into its own module
* Fix and add more unit tests
* Add acceptance tests for fixed issues

0.8.3 (2016.03.18)
==================

* Bugfixes on issue #8
* Fix unit test to support Python 3.x

0.8.2 (2016.03.06)
==================

* Bugfixes on issue #5

0.8.1 (2016.02.23)
==================

* Fix typos
* Add new strategies for ``Get Location``

0.8.0 (2016.02.14)
==================

* Refactor element related operation into its own module
* Using type check to validate the value instead of locator position
* Add unit tests

0.7.2 (2016.02.07)
==================

* Add ``Scroll Element Into View`` keyword
* Using locator instead of element to prevent stale exception in ``_wait_until_page_ready``
* Using locator position to indicate the argument type
* Add new classifier Framework :: Robot Framework

0.7.1 (2016.02.03)
==================

* Add default timeout for ``_wait_until_page_ready``
* Refactor ``_wait_until_page_ready`` to reduce its complexity
* Include page ready keywords return values as part of ``_wait_until_page_ready`` return value
* Follow lint suggestion

0.7.0 (2016.01.31)
==================

* Different approach of waiting to bring speed improvement

0.6.2 (2016.01.10)
==================

* Add `skip_ready` argument to skip page ready check.
* Add ``get_screen_size`` keyword.
* Add Python 3.x support.
* Follow lint suggestion.

0.6.1 (2015.10.22)
==================

* Bugfixes

0.6.0 (2015.10.15)
==================

* Add ``Execute Async Javascript With Replaced Variables`` keyword.
* Add ``Execute Javascript With Replaced Variables`` keyword.
* Add ``Wait For Condition With Replaced Variables`` keyword.
* Add ``Warn Any Javascript Errors`` keyword.
* Major restructure on existing keywords for better maintainability.

0.5.7 (2015.10.04)
==================

* Add ``wait_until_element_contains_attribute`` and ``wait_until_element_does_not_contain_attribute`` keywords.

0.5.6 (2015.09.26)
==================

* Add ``get_browser_logs`` keyword.
* Refactor library parameters.

0.5.5 (2015.09.22)
==================

* Add frames support
* Add ``register_page_ready_keyword`` and ``remove_page_ready_keyword`` keywords
* Bugfixes

0.5.4 (2015.09.06)
==================

* Add Angular strategies support

0.4.13 (2015.07.24)
===================

* Adjust selenium and S2L requirements
* Register the main window as the first window handle in the list during open browser
* Use docstring decorator to inherit method docs from parent class

0.4.12 (2015.07.22)
===================

* Update documentation
* selenium package hard requirement

0.4.11 (2015.07.22)
===================

* Fixes ``wait_for_async_condition`` typos
* Follow flake8 and pylint recommendation

0.4.10 (2015.07.09)
==================

* Fixes ``get_location`` to consider AngularJS synchronization, this is specially apparent on IE
* Adds ``element_attribute_should_contain`` and ``element_attribute_should_not_contain`` keywords to support element attribute verification
* Adds ``wait_until_location_contains`` and ``wait_until_location_does_not_contain`` to support current URL verification
* Adds more documentation
* Adds package registration as part of make task

0.4.9 (2015.07.08)
==================

* Removes part of ``_input_text_into_text_field`` method and inherits directly from Selenium2Library
* Overrides ``get_location`` method with cross browser support
* Removes ``location_should_be`` method
* Removes ``_is_firefox`` method
* Inherits class documentation from Selenium2Library with minor adjustments
* Adds documentation and licensing information
* Removes unneeded exclude in manifest file
* Minor syntax adjustments

0.4.8 (2015.06.27)
==================

* Initial library launch
