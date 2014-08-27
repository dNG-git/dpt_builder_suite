# -*- coding: utf-8 -*-
##j## BOF

"""
builderSkel
Common skeleton for builder tools
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?py;builder_skel

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(builderSkelVersion)#
#echo(__FILEPATH__)#
"""

from distutils.command.install_data import install_data as _install_data
from os import path
from shutil import copyfile
import os

from .build_mixin import BuildMixin

class InstallData(_install_data, BuildMixin):
#
	"""
python.org: Implements the Distutils 'install_data' command, for installing
platform-independent data files

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSkel
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	_install_data_callback_definitions = [ ]
	"""
Callbacks to call while executing "install_data".
	"""

	def _extend_data_files(self, target_path, target_directory):
	#
		"""
Extends the list of tuples for data files based on the content of the given
target directory.

:param target_path: Target directory for build

:since: v0.1.01
		"""

		for dirpath, _, filenames in os.walk(path.join(target_path, target_directory)):
		#
			files = [ ]
			for filename in filenames: files.append(path.join(dirpath, filename))
			if (len(files) > 0): self.data_files.append(( dirpath[len(target_path) + 1:], files ))
		#
	#

	def run(self):
	#
		"""
Build modules, packages, and copy data files to build directory

:since: v0.1.01
		"""

		target_directories = [ ]

		for callback_definition in InstallData._install_data_callback_definitions:
		#
			for source_directory in callback_definition['source_directories']:
			#
				if (os.access(source_directory, os.R_OK | os.X_OK)):
				#
					callback_definition['callback'](source_directory, InstallData._build_target_path, InstallData._build_target_parameters)
					if (source_directory not in target_directories): target_directories.append(source_directory)
				#
			#
		#

		for target_directory in target_directories:
		#
			self._extend_data_files(InstallData._build_target_path, target_directory)
		#

		_install_data.run(self)
	#

	@staticmethod
	def add_install_data_callback(callback, source_directories):
	#
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
	def plain_copy(source_dirpath, target_path, target_parameters):
	#
		"""
Callback to be used in "dNG.distutils.InstallData".

:param source_dirpath: Source directory to copy files in
:param target_path: Target directory for build
:param target_parameters: Target parameters

:since: v0.1.01
		"""

		extensions = target_parameters.get("install_data_plain_copy_extensions", "").split(",")

		for dirpath, _, filenames in os.walk(source_dirpath):
		#
			target_dirpath = path.join(target_path, dirpath)
			if (not os.access(target_dirpath, os.W_OK)): os.mkdir(target_dirpath, 0o755)

			for filename in filenames:
			#
				if (path.splitext(filename)[1][1:] in extensions): copyfile(path.join(dirpath, filename), path.join(target_dirpath, filename))
			#
		#
	#
#

##j## EOF