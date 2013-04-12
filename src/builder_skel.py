# -*- coding: utf-8 -*-
##j## BOF

"""
The builder skeleton combines common methods to interate directories and
parse files.
"""
"""n// NOTE
----------------------------------------------------------------------------
builderSkel
Common skeleton for builder tools
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?builderSkel

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(builderSkelVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
from time import time
import os, re, sys

try: import hashlib
except ImportError: import md5 as hashlib

try: import cPickle as pickle
except ImportError: import pickle

from file import direct_file

try: _unicode_object = { "type": unicode, "str": unicode.encode, "unicode": str.decode }
except: _unicode_object = { "type": bytes, "str": bytes.decode, "unicode": str.encode }

class direct_builder_skel(object):
#
	"""
Provides a Python "make" environment skeleton.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    ext_core
:subpackage: builderSkel
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, parameters, include, output_path, filetype, default_umask = None, default_chmod_files = None, default_chmod_dirs = None, timeout_retries = 5, event_handler = None):
	#
		"""
Constructor __init__(direct_builder_skel)

:param parameters: DEFINE statements
:param include: String (delimiter is ",") with directory or file names to
                be included.
:param output_path: Output path
:param filetype: String (delimiter is ",") with extensions of files to be
                 parsed.
:param default_umask umask: to set before creating new directories or files
:param default_chmod_files: chmod to set when creating a new file
:param default_chmod_dirs: chmod to set when creating a new directory
:param timeout_retries: Retries before timing out
:param event_handler: EventHandler to use

:since: v0.1.00
		"""

		if (event_handler != None): event_handler.debug("#echo(__FILEPATH__)# -builderSkel.__init__()- (#echo(__LINE__)#)")

		self.chmod_dirs = (0o750 if (default_chmod_dirs == None) else int(default_chmod_dirs, 8))
		"""
chmod to set when creating a new directory
		"""
		self.chmod_files = default_chmod_files
		"""
chmod to set when creating a new file
		"""
		self.dir_list = [ ]
		"""
Directories to be scanned
		"""
		self.dir_exclude_list = [ ]
		"""
Directories to be ignored while scanning
		"""
		self.event_handler = event_handler
		"""
The EventHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.file_dict = { }
		"""
Files to be parsed
		"""
		self.file_exclude_list = [ ]
		"""
Files to be ignored while scanning
		"""
		self.filetype_list = [ ]
		"""
Filetype extensions to be parsed
		"""
		self.filetype_ascii_list = [ "txt", "js", "php", "py", "xml" ]
		"""
Filetype extensions to be parsed
		"""
		self.output_path = ""
		"""
Path to generate the output files
		"""
		self.output_strip_prefix = ""
		"""
Prefix to be stripped from output paths
		"""
		self.parameters = { }
		"""
DEFINE values
		"""
		self.parser_list = None
		"""
Tags to be scanned for
		"""
		self.parser_pickle = { }
		"""
md5 strings of parsed files
		"""
		self.parser_tag = None
		"""
Tag identifier
		"""
		self.timeout_retries = timeout_retries
		"""
Retries before timing out
		"""
		self.umask = default_umask
		"""
umask to set before creating a new file
		"""
		self.workdir_rescan = True
		"""
umask to set before creating a new file
		"""

		self.set_new_target(parameters, include, output_path, filetype)
	#

	def add_filetype_ascii(self, extension):
	#
		"""
Adds an extension to the list of ASCII file types.

:param extension: File type extension to add
		"""

		global _unicode_object
		if (type(extension) == _unicode_object['type']): extension = _unicode_object['str'](extension, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.add_filetype_ascii({0})- (#echo(__LINE__)#)".format(extension))
		self.filetype_ascii_list.append(extension)
	#

	def data_parse(self, data, file_pathname, file_name):
	#
		"""
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:access: protected
:return: (str) Filtered data
:since:  v0.1.00
		"""

		global _unicode_object
		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.data_parse(data)- (#echo(__LINE__)#)")

		var_return = data.replace("#" + "echo(__FILE__)#", file_name)
		var_return = var_return.replace("#" + "echo(__FILEPATH__)#", file_pathname)

		if (var_return.find("#" + "echo(__LINE__)#") > -1):
		#
			data = re.split("\r\n|\r|\n", var_return)
			line = 0

			for result in data:
			#
				data[line] = result.replace("#" + "echo(__LINE__)#", str(line + 1))
				line += 1
			#

			var_return = "\n".join(data)
		#

		result_list = re.findall("#" + "echo\(((?!_)\w+)\)#", var_return)

		if (len(result_list)):
		#
			matched_list = [ ]

			for result in result_list:
			#
				if (result not in matched_list):
				#
					if (type(result) == _unicode_object['type']): result = _unicode_object['str'](result, "utf-8")
					value = self.get_variable(result)

					if (value == None): var_return = var_return.replace("#" + "echo({0})#".format(result), result)
					else: var_return = var_return.replace("#" + "echo({0})#".format(result), value)

					matched_list.append(result)
				#
			#
		#

		return var_return
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

		return data
	#

	def dir_create(self, dir_path, timeout = -1):
	#
		"""
Creates a directory (or returns the status of is_writable if it exists).
Use slashes - even on Microsoft(R) Windows(R) machines.

:param dir_path: Path to the new directory.
:param timeout: Timeout to use

:access: protected
:return: (bool) True on success
:since:  v0.1.00
		"""

		global _unicode_object
		if (type(dir_path) == _unicode_object['type']): dir_path = _unicode_object['str'](dir_path, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.dir_create({0}, {1:d})- (#echo(__LINE__)#)".format(dir_path, timeout))

		dir_path = re.sub("\/$", "", dir_path)
		dir_path_os = path.normpath(dir_path)

		if (len(dir_path) == 0 or dir_path == "."): var_return = False
		elif (path.isdir(dir_path_os) and os.access(dir_path_os, os.W_OK)): var_return = True
		elif (path.exists(dir_path_os)): var_return = False
		else:
		#
			is_writable = True
			dir_list = dir_path.split("/")
			dir_count = len(dir_list)
			var_return = False

			if (timeout < 0): timeout_time = time() + self.timeout_retries
			else: timeout_time = time() + timeout

			if (dir_count > 1):
			#
				dir_list.pop()
				dir_basepath = "/".join(dir_list)
				is_writable = self.dir_create(dir_basepath)
			#

			if (is_writable and time() < timeout_time):
			#
				if (self.umask != None): os.umask(int(self.umask, 8))

				try:
				#
					os.mkdir(dir_path_os, self.chmod_dirs)
					var_return = os.access(dir_path_os, os.W_OK)
				#
				except: pass
			#
		#

		return var_return
	#

	def file_parse(self, file_pathname):
	#
		"""
Handle the given file and call the content parse method.

:param file_pathname: Path to the requested file

:access: protected
:return: (bool) True on success
:since:  v0.1.00
		"""

		global _unicode_object
		if (type(file_pathname) == _unicode_object['type']): file_pathname = _unicode_object['str'](file_pathname, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.file_parse({0})- (#echo(__LINE__)#)".format(file_pathname))

		var_return = True

		( file_basename, file_ext ) = path.splitext(file_pathname)
		file_basename = path.basename(file_pathname)
		file_ext = file_ext[1:]
		file_object = direct_file(self.umask, self.chmod_files, self.timeout_retries, self.event_handler)
		file_text_mode = False

		if (len(file_ext) > 0 and file_ext in self.filetype_ascii_list): file_text_mode = True
		elif (len(file_basename) > 0): file_text_mode = file_basename in self.filetype_ascii_list

		if ((file_text_mode and file_object.open(file_pathname, True, "r")) or file_object.open(file_pathname, True, "rb")):
		#
			file_content = file_object.read()
			file_object.close()
		#
		else: file_content = None

		file_pathname = re.sub("^{0}".format(re.escape(self.output_strip_prefix)), "", file_pathname)

		if (file_pathname in self.parser_pickle):
		#
			if ((file_text_mode and file_object.open(self.output_path + file_pathname, True, "r")) or file_object.open(self.output_path + file_pathname, True, "rb")):
			#
				file_old_content = file_object.read()
				file_object.close()

				if (type(file_old_content) != _unicode_object['type']): file_old_content = _unicode_object['unicode'](file_old_content, "utf-8")
				file_old_content_md5 = hashlib.md5(file_old_content).hexdigest()
			#
			else: file_old_content_md5 = None

			if (file_old_content_md5 != None and file_old_content_md5 != self.parser_pickle[file_pathname]):
			#
				var_return = False
				sys.stdout.write("has been changed ... ")
			#
		#

		if (var_return):
		#
			if (file_content == None):
			#
				file_content = ""
				var_return = self.file_write("", self.output_path + file_pathname)
			#
			elif (file_text_mode):
			#
				file_content = self.data_parse(file_content, file_pathname, file_basename)
				var_return = self.file_write(file_content, self.output_path + file_pathname, "w+")
			#
			else: var_return = self.file_write(file_content, self.output_path + file_pathname)

			if (type(file_content) != _unicode_object['type']): file_content = _unicode_object['unicode'](file_content, "utf-8")
			if (var_return): self.parser_pickle[file_pathname] = hashlib.md5(file_content).hexdigest()
		#

		return var_return
	#

	def file_write(self, file_content, file_pathname, file_mode = "w+b"):
	#
		"""
Write the given file to the defined location. Create subdirectories if
needed.

:param file_content: Parsed content
:param file_pathname: Path to the output file
:param file_mode: Filemode to use

:access: protected
:return: (bool) True on success
:since:  v0.1.00
		"""

		global _unicode_object
		if (type(file_pathname) == _unicode_object['type']): file_pathname = _unicode_object['str'](file_pathname, "utf-8")
		if (type(file_mode) == _unicode_object['type']): file_mode = _unicode_object['str'](file_mode, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.file_write(file_content, {0}, {1})- (#echo(__LINE__)#)".format(file_pathname, file_mode))

		dir_path = path.dirname(file_pathname)
		var_return = False

		if (len(dir_path) < 1 or self.dir_create(dir_path)):
		#
			file_object = direct_file(self.umask, self.chmod_files, self.timeout_retries, self.event_handler)

			if (file_object.open(file_pathname, False, file_mode)):
			#
				var_return = file_object.write(file_content)
				file_object.close()
			#
		#

		return var_return
	#

	def get_variable(self, name):
	#
		"""
Gets the variable content with the given name.

:param name: Variable name

:access: protected
:return: (mixed) Variable content; None if undefined
:since:  v0.1.00
		"""

		global _unicode_object
		if (type(name) == _unicode_object['type']): name = _unicode_object['str'](name, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.get_variable({0})- (#echo(__LINE__)#)".format(name))
		return self.parameters.get(name, None)
	#

	def make_all(self):
	#
		"""
Parse and rewrite all directories and files given as include definitions.

:return: (bool) True on success
:since:  v0.1.00
		"""

		global _unicode_object
		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.make_all()- (#echo(__LINE__)#)")

		var_return = False

		if ((self.workdir_rescan) and len(self.dir_list) > 0 and len(self.filetype_list) > 0):
		#
			self.workdir_scan()
			self.workdir_rescan = False
		#

		if (len(self.file_dict) < 1):
		#
			if (self.event_handler != None): self.event_handler.error("#echo(__FILEPATH__)# -builderSkel.make_all()- (#echo(__LINE__)#) reports: No valid files found for parsing")
		#
		else:
		#
			for file_id in self.file_dict:
			#
				var_file = self.file_dict[file_id]
				if (type(var_file) == _unicode_object['type']): var_file = _unicode_object['str'](var_file, "utf-8")

				sys.stdout.write(">>> Processing {0} ... ".format(var_file))

				if (self.file_parse(var_file)): sys.stdout.write("done\n")
				else: sys.stdout.write("failed\n")
			#
		#

		if (len(self.parser_pickle) > 0):
		#
			sys.stdout.write(">> Writing make.py.pickle\n")

			var_file = open("{0}/make.py.pickle".format(self.output_path), "wb")
			pickle.dump(self.parser_pickle, var_file, pickle.HIGHEST_PROTOCOL)
			var_file.close()
		#

		return var_return
	#

	def parser(self, parser_tag, data, data_position = 0, nested_tag_end_position = None):
	#
		"""
Parser for "make" tags.

:param parser_tag: Starting tag to be searched for
:param data: Data to be parsed
:param data_position: Current parser position
:param nested_tag_end_position: End position for nested tags 

:access: protected
:return: (str) Converted data; None for nested parsing results without a match
:since:  v0.1.00
		"""

		global _unicode_object
		if (type(parser_tag) == _unicode_object['type']): parser_tag = _unicode_object['str'](parser_tag, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.parser({0}, data, {1:d}, nested_tag_end_position)- (#echo(__LINE__)#)".format(parser_tag, data_position))

		if (nested_tag_end_position == None):
		#
			data_position = data.find(parser_tag, data_position)
			nested_check = False
		#
		else:
		#
			data_position = data.find(parser_tag, data_position)
			if (data_position >= nested_tag_end_position): data_position = -1

			nested_check = True
			tag_end_position = -1
		#

		while (data_position > -1):
		#
			tag_definition = self.parser_check(data[data_position:])

			if (tag_definition == None): data_position += len(parser_tag)
			else:
			#
				tag_length = len(tag_definition[0])
				tag_start_end_position = self.parser_tag_find_end_position(data, data_position + tag_length, tag_definition[1])
				tag_end_position = -1

				if (tag_start_end_position > -1):
				#
					tag_end_position = self.parser_tag_end_find_position(data, tag_start_end_position, tag_definition[2])

					if (tag_end_position < 0): nested_data = None
					else: nested_data = self.parser(parser_tag, data, data_position + 1, tag_end_position)

					while (nested_data != None):
					#
						data = nested_data
						tag_start_end_position = self.parser_tag_find_end_position(data, data_position + 1, tag_definition[1])
						if (tag_start_end_position > -1): tag_end_position = self.parser_tag_end_find_position(data, tag_start_end_position, tag_definition[2])

						nested_data = self.parser(parser_tag, data, data_position + 1, tag_end_position)
					#
				#

				if (tag_end_position > -1): data = self.parser_change(tag_definition, data, data_position, tag_start_end_position, tag_end_position)
				else: data_position += tag_length
			#

			if (nested_check): data_position = -1
			else: data_position = data.find(parser_tag, data_position)
		#

		if (nested_check and tag_end_position < 0): data = None
		return data
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

		raise RuntimeError("Not implemented")
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:access: protected
:return: (tuple) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		return None
	#

	def parser_tag_end_find_position(self, data, data_position, tag_end_list):
	#
		"""
Find the starting position of the closing tag.

:param data: String that contains convertable data
:param data_position: Current parser position
:param tag_end_list: List of possible closing tags to be searched for

:access: protected
:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.parser_tag_end_find_position(data, data_position, tag_end_list)- (#echo(__LINE__)#)")
		var_return = None

		is_valid = True
		result = -1

		while ((var_return == None or var_return > -1) and is_valid):
		#
			for tag_end in tag_end_list:
			#
				result = data.find(tag_end, data_position)
				if (result > -1 and (var_return == None or result < var_return)): var_return = result
			#

			if (var_return == None): var_return = -1
			elif (var_return > -1):
			#
				data_position = var_return
				if (data[var_return - 1:var_return] != "\\"): is_valid = False
			#
		#

		return var_return
	#

	def parser_tag_find_end_position(self, data, data_position, tag_end):
	#
		"""
Find the starting position of the enclosing content.

:param data: String that contains convertable data
:param data_position: Current parser position
:param tag_end: Tag end definition

:access: protected
:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.parser_tag_find_end_position(data, data_position, tag_end)- (#echo(__LINE__)#)")
		var_return = None

		is_valid = True

		while ((var_return == None or var_return > -1) and is_valid):
		#
			var_return = data.find(tag_end, data_position)

			if (var_return > -1):
			#
				data_position = var_return
				if (data[var_return - 1:var_return] != "\\"): is_valid = False
			#
		#

		if (var_return > -1): var_return += len(tag_end)
		return var_return
	#

	def set_event_handler(self, event_handler = None):
	#
		"""
Sets the EventHandler.

:param event_handler: EventHandler to use

:since: v0.1.00
		"""

		if (event_handler != None): event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_event_handler(event_handler)- (#echo(__LINE__)#)")
		self.event_handler = event_handler
	#

	def set_exclude(self, exclude):
	#
		"""
Add "exclude" definitions for directories and files.

:param exclude: String (delimiter is ",") with exclude names or paths

:since: v0.1.00
		"""

		global _unicode_object
		if (type(exclude) == _unicode_object['type']): exclude = _unicode_object['str'](exclude, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_exclude({0})- (#echo(__LINE__)#)".format(exclude))

		if (type(exclude) == str):
		#
			exclude_list = exclude.split(",")

			for exclude in exclude_list:
			#
				self.dir_exclude_list.append(exclude)
				self.file_exclude_list.append(exclude)
			#
		#
		elif (self.event_handler != None): self.event_handler.warn("#echo(__FILEPATH__)# -builderSkel.set_exclude()- (#echo(__LINE__)#) reports: Given parameter is not a string")
	#

	def set_exclude_dirs(self, exclude):
	#
		"""
Add "exclude" definitions for directories.

:param exclude: String (delimiter is ",") with exclude names or paths

:since: v0.1.00
		"""

		global _unicode_object
		if (type(exclude) == _unicode_object['type']): exclude = _unicode_object['str'](exclude, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_exclude_dirs({0})- (#echo(__LINE__)#)".format(exclude))

		if (type(exclude) == str):
		#
			exclude_list = exclude.split(",")
			for exclude in exclude_list: self.dir_exclude_list.append(exclude)
		#
		elif (self.event_handler != None): self.event_handler.warn("#echo(__FILEPATH__)# -builderSkel.set_exclude_dirs()- (#echo(__LINE__)#) reports: Given parameter is not a string")
	#

	def set_exclude_files(self, exclude):
	#
		"""
Add "exclude" definitions for files.

:param exclude: String (delimiter is ",") with exclude names or paths

:since: v0.1.00
		"""

		global _unicode_object
		if (type(exclude) == _unicode_object['type']): exclude = _unicode_object['str'](exclude, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_exclude_files({0})- (#echo(__LINE__)#)".format(exclude))

		if (type(exclude) == str):
		#
			exclude_list = exclude.split(",")
			for exclude in exclude_list: self.file_exclude_list.append(exclude)
		#
		elif (self.event_handler != None): self.event_handler.warn("#echo(__FILEPATH__)# -builderSkel.set_exclude_files()- (#echo(__LINE__)#) reports: Given parameter is not a string")
	#

	def set_new_target(self, parameters, include, output_path, filetype):
	#
		"""
Sets a new target for processing.

:param parameters: DEFINE statements
:param include: String (delimiter is ",") with directory or file names to
                be included.
:param output_path: Output path
:param filetype: String (delimiter is ",") with extensions of files to be
                 parsed.

:since: v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_new_target(parameters, include, output_path, filetype)- (#echo(__LINE__)#)")

		self.dir_exclude_list = [ ]
		self.file_exclude_list = [ ]
		self.filetype_list = filetype.split(",")

		if (len(output_path) and (not output_path.endswith("/")) and (not output_path.endswith("\\"))): output_path += path.sep
		self.output_path = output_path
		sys.stdout.write("> New output target {0}\n".format(output_path))

		if (os.access(path.normpath("{0}/make.py.pickle".format(output_path)), os.W_OK)):
		#
			sys.stdout.write(">> Reading make.py.pickle\n")

			var_file = open("{0}/make.py.pickle".format(output_path), "rb")
			self.parser_pickle = pickle.load(var_file)
			var_file.close()
		#
		else: self.parser_pickle = { }

		if (type(self.parser_pickle) != dict): self.parser_pickle = { }
		self.output_strip_prefix = "";

		if (type(parameters) == dict): self.parameters = parameters
		else: self.parameters = { }

		data_list = include.split(",")

		for data in data_list:
		#
			if (path.isdir(data)):
			#
				if (self.workdir_rescan == False and (data not in self.dir_list)):
				#
					self.dir_list = [ ]
					self.file_dict = { }
					self.workdir_rescan = True
				#

				self.dir_list.append(data)
			#
			elif (path.isfile(data)):
			#
				if (type(data) != _unicode_object['type']): data = _unicode_object['unicode'](data, "utf-8")
				file_id = hashlib.md5(data).hexdigest()

				if (self.workdir_rescan == False and (file_id not in self.file_dict)):
				#
					self.dir_list = [ ]
					self.file_dict = { }
					self.workdir_rescan = True
				#

				self.file_dict[file_id] = data
			#
		#
	#

	def set_strip_prefix(self, strip_prefix):
	#
		"""
Define a prefix to be stripped from output paths.

:param strip_prefix: Prefix definition

:since: v0.1.00
		"""

		global _unicode_object
		if (type(strip_prefix) == _unicode_object['type']): strip_prefix = _unicode_object['str'](strip_prefix, "utf-8")

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.set_strip_prefix({0})- (#echo(__LINE__)#)".format(strip_prefix))

		if (type(strip_prefix) == str): self.output_strip_prefix = strip_prefix
		elif (self.event_handler != None): self.event_handler.warn("#echo(__FILEPATH__)# -builderSkel.set_strip_prefix()- (#echo(__LINE__)#) reports: Given parameter is not a string")
	#

	def workdir_scan(self):
	#
		"""
Scan given directories for files to be parsed.

:access: protected
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -builderSkel.workdir_scan()- (#echo(__LINE__)#)")

		"""
Create a list of files - we need to scan directories recursively ...
		"""

		re_content_estripped = re.compile("^{0}".format(re.escape(self.output_strip_prefix)))
		sys.stdout.write(">> Ready to build file index\n")
		dir_counter = 0

		while (len(self.dir_list) > dir_counter):
		#
			sys.stdout.write(">>> Scanning {0} ... ".format(self.dir_list[dir_counter]))
			dir_path_os = path.normpath(self.dir_list[dir_counter])

			if (path.isdir(dir_path_os) and os.access(dir_path_os, os.R_OK)):
			#
				content_list = os.listdir(dir_path_os)

				for content in content_list:
				#
					if (content[0] != "."):
					#
						if (self.dir_list[dir_counter].endswith("/")): content_extended = self.dir_list[dir_counter] + content
						else: content_extended = "{0}/{1}".format(self.dir_list[dir_counter], content)

						content_extended_os = path.normpath(content_extended)
						content_estripped = re_content_estripped.sub("", content_extended)
						if (type(content_estripped) == _unicode_object['type']): content_estripped = _unicode_object['str'](content_estripped, "utf-8")

						if (path.isdir(content_extended_os)):
						#
							if ((content not in self.dir_exclude_list) and (content_estripped not in self.dir_exclude_list)): self.dir_list.append(content_extended)
						#
						elif (path.isfile(content_extended_os)):
						#
							( content_basename, content_ext ) = path.splitext(content)
							content_ext = content_ext[1:]
							content_id = content_estripped

							if (type(content_id) != _unicode_object['type']): content_id = _unicode_object['unicode'](content_id, "utf-8")
							content_id = hashlib.md5(content_id).hexdigest()

							if (len(content_ext) > 0 and content_ext in self.filetype_list and (content not in self.file_exclude_list) and (content_estripped not in self.file_exclude_list)): self.file_dict[content_id] = content_extended
						#
					#
				#

				sys.stdout.write("done\n")
			#
			else: sys.stdout.write("failed\n")

			dir_counter += 1
		#
	#
#

##j## EOF