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

from os import path

class BuildMixin(object):
#
	"""
This mixin is used to map Distutils methods with a build directory.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSkel
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	_build_target_path = None
	"""
Target directory for build
	"""
	_build_target_parameters = { }
	"""
Target parameters
	"""

	@staticmethod
	def set_build_target_path(target_path):
	#
		"""
Sets the target directory used during build.

:param target_path: Target directory for build

:since: v0.1.01
		"""

		BuildMixin._build_target_path = path.normpath(target_path)
	#

	@staticmethod
	def set_build_target_parameters(parameters):
	#
		"""
Sets the target parameters.

:param parameters: Target parameters

:since: v0.1.01
		"""

		BuildMixin._build_target_parameters = parameters
	#
#

##j## EOF