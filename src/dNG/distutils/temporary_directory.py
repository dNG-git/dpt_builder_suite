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

from shutil import rmtree

try: from tempfile import TemporaryDirectory
except ImportError:
#
	from tempfile import mkdtemp

	class TemporaryDirectory(object):
	#
		"""
python.org: Create and return a temporary directory.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSkel
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
		"""

		def __init__(self, suffix = "", prefix = "tmp", dir = None):
		#
			"""
Constructor __init__(TemporaryDirectory)
			"""

			self.dir = dir
			self.name = None
			self.prefix = prefix
			self.suffix = suffix
		#

		def __enter__(self):
		#
			"""
python.org: Enter the runtime context related to this object.
			"""

			self.name = mkdtemp(self.suffix, self.prefix, self.dir)
			return self.name
		#

		def __exit__(self, exc, value, tb):
		#
			"""
python.org: Exit the runtime context related to this object.
			"""

			self.cleanup()
		#

		def cleanup(self, _warn = False):
		#
			"""
python.org: The directory can be explicitly cleaned up by calling the cleanup() method.
			"""

			rmtree(self.name)
		#
	#
#

##j## EOF