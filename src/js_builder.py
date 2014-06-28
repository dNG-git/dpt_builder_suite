# -*- coding: utf-8 -*-
##j## BOF

"""
jsBuilder
Build JavaScript code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?js;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(jsBuilderVersion)#
#echo(__FILEPATH__)#
"""

from os import path
from slimit.minifier import minify

from builder_skel import BuilderSkel

class JsBuilder(BuilderSkel):
#
	"""
Provides a Javascript "make" environment object.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    ext_core
:subpackage: jsBuilder
:since:      v1.0.0
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _parse_data(self, data, file_pathname, file_name):
	#
		"""
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:return: (str) Filtered data
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -JsBuilder._parse_data(data)- (#echo(__LINE__)#)")

		if (self._get_variable("js_min_filenames") != None
		    and file_pathname[-7:].lower() != ".min.js"
		    and self._get_variable("debug") == None
		   ): data = minify(data, True)

		if (self._get_variable("js_header") != None): data = "// {0}\n{1}".format(self._get_variable("js_header"), data)
		return BuilderSkel._parse_data(self, data, file_pathname, file_name)
	#

	def _write_file(self, file_content, file_pathname, file_mode = "w+b"):
	#
		"""
Write the given file to the defined location. Create subdirectories if
needed.

:param file_content: Parsed content
:param file_pathname: Path to the output file
:param file_mode: Filemode to use

:return: (bool) True on success
:since:  v0.1.00
		"""

		if (self._get_variable("js_min_filenames") != None
		    and file_pathname[-7:].lower() != ".min.js"
		    and self._get_variable("debug") == None
		   ):
		#
			( file_pathname, file_ext ) = path.splitext(file_pathname)
			if (len(file_ext) > 0): file_pathname = "{0}.min{1}".format(file_pathname, file_ext)
		#

		return BuilderSkel._write_file(self, file_content, file_pathname, file_mode)
	#
#

##j## EOF