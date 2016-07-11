Extended Selenium 2 (WebDriver) web testing library for Robot Framework
=======================================================================

|Docs| |Version| |Status| |Python| |Download| |License|

Introduction
------------

ExtendedSelenium2Library is web testing library for `Robot Framework`_
that uses the `Selenium 2 (WebDriver)`_ libraries from the Selenium_ project,
to control the web browser with AngularJS_ support.

It leverages Selenium2Library_ internally to provide AngularJS_ synchronization support,
to provide AngularJS_ locators support, to deliver keywords enhancement,
and strive for a seamless migration from Selenium2Library_.

ExtendedSelenium2Library runs tests in a real browser instance. It should work in
most modern browsers and can be used with both Python and Jython interpreters.

More information about this library can be found in the `Keyword Documentation`_.

Robot Framework and Cucumber Similarities
-----------------------------------------

|Similarity|

|Onion|

|Actual|

Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using pip_:

.. code:: console

    pip install robotframework-extendedselenium2library

The main benefit of using ``pip`` is that it automatically installs all
dependencies needed by the library. Other nice features are easy upgrading
and support for un-installation:

.. code:: console

    pip install --upgrade robotframework-extendedselenium2library
    pip uninstall robotframework-extendedselenium2library

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the Selenium tool used by the library:

.. code:: console

    pip install robotframework-extendedselenium2library==x.x.x
    pip install --upgrade selenium
    pip install selenium==x.xx

Proxy configuration
'''''''''''''''''''

If you are behind a proxy, you can use ``--proxy`` command line option
or set ``http_proxy`` and/or ``https_proxy`` environment variables to
configure ``pip`` to use it. If you are behind an authenticating NTLM proxy,
you may want to consider installing CNTML_ to handle communicating with it.

For more information about ``--proxy`` option and using pip with proxies
in general see:

- http://pip-installer.org/en/latest/usage.html
- http://stackoverflow.com/questions/9698557/how-to-use-pip-on-windows-behind-an-authenticating-proxy
- http://stackoverflow.com/questions/14149422/using-pip-behind-a-proxy

Manual installation
'''''''''''''''''''

If you do not have network connection or cannot make proxy to work, you need
to resort to manual installation. This requires installing both the library
and its dependencies yourself.

- Make sure you have `Robot Framework installed`_.

- Download source distributions (``*.tar.gz``) for the library and its dependencies:

  - https://pypi.python.org/pypi/robotframework-extendedselenium2library
  - https://pypi.python.org/pypi/robotframework-selenium2library
  - https://pypi.python.org/pypi/selenium
  - https://pypi.python.org/pypi/decorator

- Download PGP signatures (``*.tar.gz.asc``) for signed packages.

- Find each public key used to sign the package:

.. code:: console

    gpg --keyserver pgp.mit.edu --search-keys D1406DE7

- Select the number from the list to import the public key

- Verify the package against its PGP signature:

.. code:: console

    gpg --verify robotframework-extendedselenium2library-x.x.x.tar.gz.asc robotframework-extendedselenium2library-x.x.x.tar.gz

- Extract each source distribution to a temporary location.

- Go to each created directory from the command line and install each project using:

.. code:: console

       python setup.py install

If you are on Windows, and there are Windows installers available for
certain projects, you can use them instead of source distributions.
Just download 32bit or 64bit installer depending on your system,
double-click it, and follow the instructions.

Directory Layout
----------------

doc/
    `Keyword documentation`_

src/
    Python source code

test/
     Test files

     utest/
           Python unit test

Usage
-----

To write tests with Robot Framework and ExtendedSelenium2Library,
ExtendedSelenium2Library must be imported into your Robot test suite.

.. code:: robotframework

    *** Settings ***
    Library    ExtendedSelenium2Library

See `Robot Framework User Guide`_ for more information.

More information about Robot Framework standard libraries and built-in tools
can be found in the `Robot Framework Documentation`_.

Building Keyword Documentation
------------------------------

The `Keyword Documentation`_ can be found online, if you need to generate the keyword documentation, run:

.. code:: console

    make doc

Run Unit Tests, and Test Coverage Report
----------------------------------------

Test the testing library, talking about dogfooding, let's run:

.. code:: console

    make test

Contributing
------------

If you would like to contribute code to Extended Selenium2 Library project you can do so through GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible. Please also include appropriate test cases.

Before your code can be accepted into the project you must also sign the `Extended Selenium2 Library CLA`_ (Individual Contributor License Agreement).

That's it! Thank you for your contribution!

License
-------

Copyright (c) 2015, 2016 Richard Huang.

This library is free software, licensed under: `GNU Affero General Public License (AGPL-3.0)`_.

Documentation and other similar content are provided under `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License`_.

.. _AngularJS: https://goo.gl/Kzz8Y3
.. _CNTML: http://goo.gl/ukiwSO
.. _Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License: http://goo.gl/SNw73V
.. _Extended Selenium2 Library CLA: https://goo.gl/forms/1pkl9YfWpA
.. _GNU Affero General Public License (AGPL-3.0): http://goo.gl/LOMJeU
.. _Keyword Documentation: https://goo.gl/9z5Xj9
.. _pip: http://goo.gl/jlJCPE
.. _Robot Framework: http://goo.gl/lES6WM
.. _Robot Framework Documentation: http://goo.gl/zy53tf
.. _Robot Framework installed: https://goo.gl/PFbWqM
.. _Robot Framework User Guide: http://goo.gl/Q7dfPB
.. _Selenium: http://goo.gl/fbso3g
.. _Selenium2Library: https://goo.gl/1VXDSI
.. _Selenium 2 (WebDriver): http://goo.gl/boVQia
.. |Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://goo.gl/9z5Xj9
    :alt: Keyword Documentation
.. |Version| image:: https://img.shields.io/pypi/v/robotframework-extendedselenium2library.svg
    :target: https://goo.gl/wHr4ni
    :alt: Package Version
.. |Status| image:: https://img.shields.io/pypi/status/robotframework-extendedselenium2library.svg
    :target: https://goo.gl/wHr4ni
    :alt: Development Status
.. |Python| image:: https://img.shields.io/pypi/pyversions/robotframework-extendedselenium2library.svg
    :target: https://goo.gl/sXzgao
    :alt: Python Version
.. |Download| image:: https://img.shields.io/pypi/dm/robotframework-extendedselenium2library.svg
    :target: https://goo.gl/wHr4ni
    :alt: Monthly Download
.. |License| image:: https://img.shields.io/pypi/l/robotframework-extendedselenium2library.svg
    :target: http://goo.gl/LOMJeU
    :alt: License
.. |Similarity| image:: https://raw.githubusercontent.com/rickypc/robotframework-extendedselenium2library/master/assets/RF-Cucumber-01.jpg
    :alt: Framework Similarities
.. |Onion| image:: https://raw.githubusercontent.com/rickypc/robotframework-extendedselenium2library/master/assets/RF-Cucumber-02.jpg
    :alt: Onion Diagram
.. |Actual| image:: https://raw.githubusercontent.com/rickypc/robotframework-extendedselenium2library/master/assets/RF-Cucumber-03.jpg
    :alt: Actual Implementation
