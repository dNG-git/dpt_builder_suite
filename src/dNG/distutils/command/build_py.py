# -*- coding: utf-8 -*-

"""
builderSuite
Build code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?py;builder_suite

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(builderSuiteVersion)#
#echo(__FILEPATH__)#
"""

from distutils.command.build_py import build_py as _build_py
from os import path
import os

from dNG.distutils.py_builder import PyBuilder
from .build_mixin import BuildMixin

class BuildPy(_build_py, BuildMixin):
    """
python.org: Build the .py/.pyc files of a package

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def _extend_packages(self, target_path):
        """
Extends the list of packages based on the content of the given target
directory.

:param target_path: Target directory for build

:since: v0.1.01
        """

        for dir_path, _, _ in os.walk(target_path):
            package = dir_path[len(target_path) + 1:].replace(path.sep, ".")
            if (package not in self.packages): self.packages.append(package)
        #
    #

    def run(self):
        """
Build modules, packages, and copy data files to build directory

:since: v0.1.01
        """

        if (os.access("src", (os.R_OK | os.X_OK))):
            target_path = path.join(BuildPy._build_target_path, "src")

            py_builder = PyBuilder(BuildPy._build_target_parameters,
                                   "src",
                                   target_path,
                                   "py",
                                   default_chmod_files = "0644",
                                   default_chmod_dirs = "0755"
                                  )

            py_builder.set_strip_prefix("src" + path.sep)

            py_builder.make_all()

            self._extend_packages(target_path)
        #

        _build_py.run(self)
    #
#
