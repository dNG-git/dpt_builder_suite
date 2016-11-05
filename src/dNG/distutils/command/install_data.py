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

from distutils.command.install_data import install_data as _install_data
from os import path
from shutil import copyfile
import os

from dNG.distutils.temporary_directory import TemporaryDirectory
from .build_mixin import BuildMixin

class InstallData(_install_data, BuildMixin):
    """
python.org: Implements the Distutils 'install_data' command, for installing
platform-independent data files

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    _install_data_callback_definitions = [ ]
    """
Callbacks to call while executing "install_data".
    """

    def _extend_data_files(self, target_path):
        """
Extends the list of tuples for data files based on the content of the given
target directory.

:param target_path: Target directory for build

:since: v0.1.01
        """

        for dir_path, _, file_names in os.walk(target_path):
            files = [ ]
            for file_name in file_names: files.append(path.join(dir_path, file_name))
            if (len(files) > 0): self.data_files.append(( dir_path[len(target_path) + 1:], files ))
        #
    #

    def run(self):
        """
Build modules, packages, and copy data files to build directory

:since: v0.1.01
        """

        with TemporaryDirectory(dir = ".") as target_path:
            for callback_definition in InstallData._install_data_callback_definitions:
                for source_directory in callback_definition['source_directories']:
                    if (os.access(source_directory, os.R_OK | os.X_OK)):
                        callback_definition['callback'](source_directory,
                                                        target_path,
                                                        InstallData._build_target_parameters
                                                       )
                    #
                #
            #

            self._extend_data_files(target_path)

            _install_data.run(self)
        #
    #

    @staticmethod
    def add_install_data_callback(callback, source_directories):
        """
Adds a callback to be called while executing "install_data".

:param callback: Python callback
:param source_directories: Target directory for build

:since: v0.1.01
        """

        InstallData._install_data_callback_definitions.append({ "callback": callback,
                                                                "source_directories": source_directories
                                                              })
    #

    @staticmethod
    def plain_copy(source_dir_path, target_path, target_parameters):
        """
Callback to be used in "dNG.distutils.InstallData".

:param source_dir_path: Source directory to copy files in
:param target_path: Target directory for build
:param target_parameters: Target parameters

:since: v0.1.01
        """

        extensions = target_parameters.get("install_data_plain_copy_extensions", "").split(",")

        for dir_path, _, file_names in os.walk(source_dir_path):
            target_dir_path = path.join(target_path, dir_path)
            if (not os.access(target_dir_path, os.W_OK)): os.mkdir(target_dir_path, 0o755)

            for file_name in file_names:
                if (path.splitext(file_name)[1][1:] in extensions): copyfile(path.join(dir_path, file_name), path.join(target_dir_path, file_name))
            #
        #
    #
#
