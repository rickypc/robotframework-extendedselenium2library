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

LIBRARY_NAME = ExtendedSelenium2Library

lc = $(subst A,a,$(subst B,b,$(subst C,c,$(subst D,d,$(subst E,e,$(subst F,f,$(subst G,g,$(subst H,h,$(subst I,i,$(subst J,j,$(subst K,k,$(subst L,l,$(subst M,m,$(subst N,n,$(subst O,o,$(subst P,p,$(subst Q,q,$(subst R,r,$(subst S,s,$(subst T,t,$(subst U,u,$(subst V,v,$(subst W,w,$(subst X,x,$(subst Y,y,$(subst Z,z,$1))))))))))))))))))))))))))

.PHONY: help

help:
	@echo targets: clean, clean_dist, version, lint, test, doc, github_doc, testpypi, pypi

clean:
	python setup.py clean --all
	rm -rf .coverage htmlcov src/*.egg-info
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" | xargs rm -rf {} \;

clean_dist:
	rm -rf dist

version:
	python -m robot.libdoc src/$(LIBRARY_NAME) version

lint:clean
	flake8 --max-complexity 10 src/$(LIBRARY_NAME)/*.py\
 		src/$(LIBRARY_NAME)/decorators/*.py\
		src/$(LIBRARY_NAME)/keywords/*.py\
 		src/$(LIBRARY_NAME)/locators/*.py
	pylint --rcfile=setup.cfg src/$(LIBRARY_NAME)/*.py\
 		src/$(LIBRARY_NAME)/decorators/*.py\
		src/$(LIBRARY_NAME)/keywords/*.py\
 		src/$(LIBRARY_NAME)/locators/*.py

test:test_unit

test_unit:
	PYTHONPATH=./src: coverage run --source=src -m unittest discover test/utest
	coverage report

doc:clean
	python -m robot.libdoc src/$(LIBRARY_NAME) doc/$(LIBRARY_NAME).html
	python -m analytics doc/$(LIBRARY_NAME).html

github_doc:clean
	git checkout gh-pages
	git merge master
	git push origin gh-pages
	git checkout master

testpypi:clean_dist doc
	python setup.py sdist --formats=gztar upload -r test --sign
	@echo https://test.pypi.org/project/robotframework-$(call lc,$(LIBRARY_NAME))/

pypi:clean_dist doc
	python setup.py sdist --formats=gztar upload -r pypi --sign
	@echo https://pypi.org/project/robotframework-$(call lc,$(LIBRARY_NAME))/
