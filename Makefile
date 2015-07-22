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

LIBRARY_NAME = ExtendedSelenium2Library

lc = $(subst A,a,$(subst B,b,$(subst C,c,$(subst D,d,$(subst E,e,$(subst F,f,$(subst G,g,$(subst H,h,$(subst I,i,$(subst J,j,$(subst K,k,$(subst L,l,$(subst M,m,$(subst N,n,$(subst O,o,$(subst P,p,$(subst Q,q,$(subst R,r,$(subst S,s,$(subst T,t,$(subst U,u,$(subst V,v,$(subst W,w,$(subst X,x,$(subst Y,y,$(subst Z,z,$1))))))))))))))))))))))))))

.PHONY: help

help:
	@echo targets: clean, version, lint, doc, github_doc, testpypi, pypi

clean:
	python setup.py clean --all
	rm -rf .coverage htmlcov src/*.egg-info
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" | xargs rm -rf {} \;

version:
	grep "VERSION = '*'" src/$(LIBRARY_NAME)/version.py

lint:clean
	flake8 --max-complexity 10
	pylint --rcfile=setup.cfg src/$(LIBRARY_NAME)/*.py src/$(LIBRARY_NAME)/locators/*.py

doc:clean
	python -m robot.libdoc src/$(LIBRARY_NAME) doc/$(LIBRARY_NAME).html
	python -m analytics doc/$(LIBRARY_NAME).html

github_doc:clean
	git checkout gh-pages
	git merge master
	git push origin gh-pages
	git checkout master

testpypi:doc
	python setup.py register -r test
	python setup.py sdist upload -r test --sign
	@echo https://testpypi.python.org/pypi/robotframework-$(call lc,$(LIBRARY_NAME))/

pypi:doc
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi --sign
	@echo https://pypi.python.org/pypi/robotframework-$(call lc,$(LIBRARY_NAME))/
