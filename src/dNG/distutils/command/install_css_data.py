# -*- coding: utf-8 -*-
##j## BOF

"""
cssBuilder
Build minimized CSS code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?css;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(cssBuilderVersion)#
#echo(__FILEPATH__)#
"""

from os import path

from dNG.distutils.css_builder import CssBuilder

class InstallCssData(object):
#
	"""
python.org: Create and return a temporary directory.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   cssBuilder
:since:     v0.1.01
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def callback(source_path, target_path, target_parameters):
	#
		"""
Callback to be used in "dNG.distutils.InstallData".

:param source_path: Source directory to work in
:param target_path: Target directory for build
:param target_parameters: Target parameters

:since: v0.1.01
		"""

		css_builder = CssBuilder(target_parameters,
		                         source_path,
		                         target_path,
		                         "css,scss",
		                         default_chmod_files = "0644",
		                         default_chmod_dirs = "0755"
		                        )

		css_builder.set_strip_prefix(target_path + path.sep)

		css_builder.make_all()
	#
#

##j## EOF