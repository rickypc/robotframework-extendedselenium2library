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

from os.path import split
from re import sub
import sys


def main(argv):
    """Adds analytics code into auto generated documentation."""
    try:
        path = argv[0]
    except IndexError:
        print("analytics.py <file_path>")
        sys.exit(1)

    with open(path) as reader:
        content = reader.read()

    analytics = """<script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create','UA-325170-8','auto');ga('set','checkProtocolTask',null);
    ga('send','pageview','%s');
</script>""" % (split(path)[1])

    content = sub(r"</body>", analytics + "\n</body>", content)

    with open(path, "w") as writer:
        writer.write(content)

if __name__ == "__main__":
    main(sys.argv[1:])
