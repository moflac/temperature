#! /usr/bin/env python
#
# setup.py
#
# py-rrdtool distutil setup
#
# Author  : Hye-Shik Chang <perky@FreeBSD.org>
# Date    : $Date: 2006/09/13 09:51:53 $
# Created : 24 May 2002
#
# $Revision: 1.8 $
#
#  ==========================================================================
#  This file is part of py-rrdtool.
#
#  py-rrdtool is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  py-rrdtool is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Foobar; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from distutils.core import setup, Extension
import sys, os

RRDBASE = os.environ.get('LOCALBASE', '/usr/local')
library_dir = os.environ.get('LIBDIR', os.path.join(RRDBASE, 'lib'))
include_dir = os.environ.get('INCDIR', os.path.join(RRDBASE, 'include'))

setup(name = "py-rrdtool",
      version = "1.0b1",
      description = "Python Interface to RRDTool",
      author = "Hye-Shik Chang",
      author_email = "perky@FreeBSD.org",
      license = "LGPL",
      url = "http://sourceforge.net/projects/py-rrdtool/",
      py_modules = ['rrdtool'],
      ext_modules = [
          Extension(
            "_rrdtool",
            ["src/_rrdtoolmodule.c"],
            libraries=['rrd'],
            library_dirs=[library_dir],
            include_dirs=[include_dir],
          )
      ]
)
