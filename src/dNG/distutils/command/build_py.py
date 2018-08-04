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
:since:     v0.1.1
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def __init__(self, *args, **kwargs):
        _build_py.__init__(self, *args, **kwargs)

        self.is_built = False
    #

    def _build_source(self):
        """
Builds the preprocessed source and adds it's packages for processing.

:since: v1.0.0
        """

        if ((not self.is_built) and os.access("src", (os.R_OK | os.X_OK))):
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

            for dir_path, subdir_names, _ in os.walk(target_path):
                dir_path = dir_path[len(target_path) + 1:]

                if (dir_path == ""):
                    if ('' not in self.package_dir):
                        self.package_dir[''] = target_path
                    #

                    for dir_name in subdir_names:
                        self.package_dir[dir_name] = path.join(target_path, dir_name)
                    #
                else:
                    package = dir_path.replace(path.sep, ".")

                    if (package not in self.packages): self.packages.append(package)
                #
            #

            self.is_built = True
        #
    #

    def build_packages(self):
        """
Builds the packages defined in the 'setup.py' packages list.

:since: v1.0.0
        """

        self._build_source()
        _build_py.build_packages(self)
    #

    def find_all_modules(self):
        """
python.org: Compute the list of all modules that will be built, whether
they are specified one-module-at-a-time ('self.py_modules') or by whole
packages ('self.packages').

:return: List of tuples
:since:  v1.0.0
        """

        self._build_source()
        return _build_py.find_all_modules(self)
    #
#
