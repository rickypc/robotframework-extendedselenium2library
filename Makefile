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

.PHONY: help

help:
	@echo targets: clean, version, documentation, documentation_on_github, testpypi_upload, pypi_upload

clean:
	python setup.py clean --all
	rm -rf src/*.egg-info
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" | xargs rm -rf {} \;

version:
	grep "VERSION = '*'" src/ExtendedSelenium2Library/version.py	

documentation:clean
	python -m robot.libdoc src/ExtendedSelenium2Library doc/ExtendedSelenium2Library.html
	python -m analytics doc/ExtendedSelenium2Library.html

documentation_on_github:clean
	git checkout gh-pages
	git merge master
	git push origin gh-pages
	git checkout master	

testpypi_upload:documentation
	python setup.py register -r test
	python setup.py sdist upload -r test --sign
	@echo https://testpypi.python.org/pypi/robotframework-extendedselenium2library/

pypi_upload:documentation
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi --sign
	@echo https://pypi.python.org/pypi/robotframework-extendedselenium2library/
