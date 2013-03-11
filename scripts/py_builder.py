# -*- coding: utf-8 -*-
##j## BOF

"""
This is the main Python "make" worker class file.
"""
"""n// NOTE
----------------------------------------------------------------------------
pyBuilder
Build Python code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?py;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pyBuilderVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import re

from builder_skel import direct_builder_skel

class direct_py_builder(direct_builder_skel):
#
	"""
Provides a Python "make" environment object.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    ext_core
:subpackage: pyBuilder
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	dir_exclude_list = [ "__pycache__" ]
	"""
Directories to be excluded
	"""

	def data_parse(self, data, file_pathname, file_name):
	#
		"""
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:access: protected
:return: (mixed) Line based array; False on error
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -pyBuilder.data_parse(data)- (#echo(__LINE__)#)")
		data = self.parser('"""#', direct_builder_skel.data_parse(self, data, file_pathname, file_name))

		if (self.get_variable("dev_comments") == None): return self.data_remove_dev_comments(data)
		else: return data
	#

	def data_remove_dev_comments(self, data):
	#
		"""
Remove all development comments from the content.

:param data: Data to be parsed

:access: protected
:return: (str) Filtered data
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -pyBuilder.data_remove_dev_comments(data)- (#echo(__LINE__)#)")
		return re.sub('(\n[ \t]*"""\n---.+?---\n[ \t]*"""\n)|("""\w//.+?//\w"""\n)', "", data, 0, re.S)
	#

	def parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:access: protected
:return: (str) Converted data
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -pyBuilder.parser_change(tag_definition, data, {0:d}, {1:d}, {2:d})- (#echo(__LINE__)#)".format(tag_position, data_position, tag_end_position))
		var_return = data[:tag_position]

		data_closed = data[self.parser_tag_find_end_position(data, tag_end_position, "*/"):]

		if (tag_definition[0] == '"""#ifdef'):
		#
			variable = re.match('^"""#ifdef\((\w+)\)', data[tag_position:data_position]).group(1)
			tag_end = data[tag_end_position:self.parser_tag_find_end_position(data, tag_end_position, '"""')]

			if (self.get_variable(variable) != None):
			#
				if (data[data_position:data_position + 1] == "\n"): var_return += data[data_position + 1:tag_end_position].replace('"\\"', '"""')
				else: var_return += data[data_position:tag_end_position].replace('"\\"', '"""')
			#

			if ((tag_end == '#\\n"""') or (tag_end == ':#\\n"""')): data_closed = re.sub("^\n", "", data_closed)
			var_return += data_closed
		#
		elif (tag_definition[0] == '"""#ifndef'):
		#
			variable = re.match('^"""#ifndef\((\w+)\)', data[tag_position:data_position]).group(1)
			tag_end = data[tag_end_position:self.parser_tag_find_end_position(data, tag_end_position, '"""')]

			if (self.get_variable(variable) == None):
			#
				if (data[data_position:data_position + 1] == "\n"): var_return += data[data_position + 1:tag_end_position].replace('"\\"', '"""')
				else: var_return += data[data_position:tag_end_position].replace('"\\"', '"""')
			#

			if ((tag_end == '#\\n"""') or (tag_end == ':#\\n"""')): data_closed = re.sub("^\n", "", data_closed)
			var_return += data_closed
		#
		else: var_return += data_closed

		return var_return
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:access: protected
:return: (mixed) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -pyBuilder.parser_check(data)- (#echo(__LINE__)#)")
		var_return = None

		if (data[:9] == '"""#ifdef'):
		#
			re_object = re.match('^"""#ifdef\((\w+)\) """\n', data)

			if (re_object == None):
			#
				re_object = re.match('^"""#ifdef\((\w+)\):\n', data)

				if (re_object == None): var_return = None
				else: var_return = ( '"""#ifdef', ":", ( ':#\\n"""', ':#"""' ) )
			#
			else: var_return = ( '"""#ifdef', '"""', ( '#\\n"""', '#"""' ) )
		#
		elif (data[:10] == '"""#ifndef'):
		#
			re_object = re.match('^"""#ifndef\((\w+)\) """\n', data)

			if (re_object == None):
			#
				re_object = re.match('^"""#ifndef\((\w+)\):\n', data)

				if (re_object == None): var_return = None
				else: var_return = ( '"""#ifndef', ":", ( ':#\\n"""', ':#"""' ) )
			#
			else: var_return = ( '"""#ifndef', '"""', ( '#\\n"""', '#"""' ) )
		#

		return var_return
	#
#

##j## EOF