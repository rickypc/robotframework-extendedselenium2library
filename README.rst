Extended Selenium 2 (WebDriver) library for Robot Framework
===========================================================

Introduction
------------

ExtendedSelenium2Library is a web testing library for `Robot Framework`_
that uses the `Selenium 2 (WebDriver)`_ libraries from the Selenium_ project,
to control the web browser with AngularJS_ support.

It leverages Selenium2Library_ internally to provide AngularJS_ synchronization support,
deliver keywords enhancement, and strive for a seamless migration from Selenium2Library_.

ExtendedSelenium2Library runs tests in a real browser instance. It should work in
most modern browsers and can be used with both Python and Jython interpreters.

More information about this library can be found in the `Keyword Documentation`_.

Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using `pip <http://pip-installer.org>`__:

.. code:: bash

    pip install robotframework-extendedselenium2library

The main benefit of using ``pip`` is that it automatically installs all
dependencies needed by the library. Other nice features are easy upgrading
and support for un-installation:

.. code:: bash

    pip install --upgrade robotframework-extendedselenium2library
    pip uninstall robotframework-extendedselenium2library

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the Selenium tool used by the library:

.. code:: bash

    pip install robotframework-extendedselenium2library==x.x.x
    pip install --upgrade selenium
    pip install selenium==2.46

Proxy configuration
'''''''''''''''''''

If you are behind a proxy, you can use ``--proxy`` command line option
or set ``http_proxy`` and/or ``https_proxy`` environment variables to
configure ``pip`` to use it. If you are behind an authenticating NTLM proxy,
you may want to consider installing `CNTML <http://cntlm.sourceforge.net>`__
to handle communicating with it.

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

- Make sure you have `Robot Framework installed <http://code.google.com/p/robotframework/wiki/Installation>`__.

- Download source distributions (``*.tar.gz``) for the library and its dependencies:

  - https://pypi.python.org/pypi/robotframework-extendedselenium2library
  - https://pypi.python.org/pypi/robotframework-selenium2library
  - https://pypi.python.org/pypi/selenium
  - https://pypi.python.org/pypi/decorator

- Download PGP signatures (``*.tar.gz.asc``) for signed packages.

- Find each public key used to sign the package:

.. code:: bash

    gpg --keyserver pgp.mit.edu --search-keys D1406DE7

- Select the number from the list to import the public key

- Verify the package against its PGP signature:

.. code:: bash

    gpg --verify robotframework-extendedselenium2library-x.x.x.tar.gz.asc robotframework-extendedselenium2library-x.x.x.tar.gz

- Extract each source distribution to a temporary location.

- Go to each created directory from the command line and install each project using:

.. code:: bash

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

Usage
-----

To write tests with Robot Framework and ExtendedSelenium2Library,
ExtendedSelenium2Library must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.

Building Keyword Documentation
------------------------------

The `Keyword Documentation`_ can be found online, if you need to generate the keyword documentation, run:

.. code:: bash

    make documentation

License
-------

Copyright (c) 2015 Richard Huang.

This library is free software, licensed under: `GNU Affero General Public License (AGPL-3.0) <http://www.gnu.org/licenses/agpl-3.0.en.html>`_.

Documentation and other similar content are provided under `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License <http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.

.. _AngularJS: https://angularjs.org
.. _Keyword Documentation: https://rickypc.github.io/robotframework-extendedselenium2library/doc/ExtendedSelenium2Library.html
.. _Robot Framework: http://robotframework.org
.. _Selenium: http://selenium.openqa.org
.. _Selenium2Library: https://github.com/rtomac/robotframework-selenium2library/wiki
.. _Selenium 2 (WebDriver): http://seleniumhq.org/docs/03_webdriver.html
.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuide
