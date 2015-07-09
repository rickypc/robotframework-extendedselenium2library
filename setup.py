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

import shutil
import sys
# To use a consistent encoding
from codecs import open
from os.path import abspath, dirname, join
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

cwd = abspath(dirname(__file__))
execfile(join(cwd, 'src', 'ExtendedSelenium2Library', 'version.py'))

with open(join(cwd, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='robotframework-extendedselenium2library',
    version=VERSION,
    description='Web testing library for Robot Framework that support AngularJS',
    long_description=long_description,
    url='https://github.com/rickypc/robotframework-extendedselenium2library',
    author='Richard Huang',
    author_email='rickypc@users.noreply.github.com',
    license='AGPL 3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='robot framework testing automation selenium selenium2 webdriver web angular angularjs ng',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['robotframework-selenium2library>=1.7.0']
)
