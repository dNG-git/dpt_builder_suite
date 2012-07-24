# -*- coding: utf-8 -*-
##j## BOF

"""
This is the skeleton Python "make" worker class file.

@internal   We are using epydoc (JavaDoc style) to automate the
            documentation process for creating the Developer's Manual.
            Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage builderSkel
@since      v0.1.00
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
builderSkel
Common skeleton for builder tools
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?builderSkel

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(builderSkelVersion)#
builderSkel/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
from time import time
import os,re,sys

try: import hashlib
except ImportError: import md5 as hashlib

from file import direct_file

try: _unicode_object = { "type": unicode,"str": unicode.encode,"unicode": str.decode }
except: _unicode_object = { "type": bytes,"str": bytes.decode,"unicode": str.encode }

class direct_builder_skel (object):
#
	"""
Provides a Python "make" environment object.

@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage builderSkel
@since      v1.0.0
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
	"""

	E_NOTICE = 1
	"""
Error notice: It is save to ignore it
	"""
	E_WARNING = 2
	"""
Warning type: Could create trouble if ignored
	"""
	E_ERROR = 4
	"""
Error type: An error occured and was handled
	"""

	chmod_dirs = None
	"""
chmod to set when creating a new directory
	"""
	chmod_files = None
	"""
chmod to set when creating a new file
	"""
	debug = None
	"""
Debug message container
	"""
	dir_list = [ ]
	"""
Directories to be scanned
	"""
	dir_exclude_list = [ ]
	"""
Directories to be ignored while scanning
	"""
	error_callback = None
	"""
Function to be called for logging exceptions and other errors
	"""
	file_dict = { }
	"""
Files to be parsed
	"""
	file_exclude_list = [ ]
	"""
Files to be ignored while scanning
	"""
	filetype_list = [ ]
	"""
Filetype extensions to be parsed
	"""
	filetype_ascii_list = [ ]
	"""
Filetype extensions to be parsed
	"""
	output_path = ""
	"""
Path to generate the output files
	"""
	output_strip_prefix = ""
	"""
Prefix to be stripped from output pathes
	"""
	parameters = { }
	"""
DEFINE values
	"""
	parser_list = None
	"""
Tags to be scanned for
	"""
	parser_tag = None
	"""
Tags to be scanned for
	"""
	time = -1
	"""
Current UNIX timestamp
	"""
	timeout_count = 5
	"""
Retries before timing out
	"""
	umask = None
	"""
umask to set before creating a new file
	"""

	"""
----------------------------------------------------------------------------
Construct the class
----------------------------------------------------------------------------
	"""

	def __init__ (self,parameters,include,output_path,filetype,default_umask = None,default_chmod_files = None,default_chmod_dirs = None,current_time = -1,timeout_count = 5,debug = False):
	#
		"""
Constructor __init__ (direct_py_builder)

@param parameters DEFINE statements
@param include String (delimiter is ",") with directory or file names to
       be included.
@param output_path Output path
@param filetype String (delimiter is ",") with extensions of files to be
       parsed.
@param default_umask umask to set before creating new directories or files
@param default_chmod_files chmod to set when creating a new file
@param default_chmod_dirs chmod to set when creating a new directory
@param current_time Current UNIX timestamp
@param timeout_count Retries before timing out
@since v0.1.00
		"""

		if (debug): self.debug = [ "builderSkel/#echo(__FILEPATH__)# -builderSkel->__init__ (direct_py_builder)- (#echo(__LINE__)#)" ]
		else: self.debug = None

		if (default_chmod_dirs == None): self.chmod_dirs = 0o750
		else: self.chmod_dirs = int (default_chmod_dirs,8)

		self.chmod_files = default_chmod_files
		self.dir_exclude_list = [ ]
		self.error_callback = None
		self.file_exclude_list = [ ]
		self.filetype_list = filetype.split (",")
		self.filetype_ascii_list = [ "txt","js","php","py","xml" ]

		if ((len (output_path)) and (not output_path.endswith ("/")) and (not output_path.endswith ("\\"))): output_path += path.sep
		self.output_path = output_path

		self.output_strip_prefix = "";

		if (type (parameters) == dict): self.parameters = parameters
		else: self.parameters = { }

		if (current_time < 0): self.time = time ()
		else: self.time = current_time

		self.timeout_count = timeout_count
		self.umask = default_umask

		self.dir_list = [ ]
		self.file_dict = { }
		f_data_list = include.split (",")

		for f_data in f_data_list:
		#
			if (path.isdir (f_data)): self.dir_list.append (f_data)
			elif (path.isfile (f_data)): self.file_dict[hashlib.md5(f_data).hexdigest ()] = f_data
		#
	#

	def condition_parse (self,condition_list):
	#
		"""
Parse the given condition and returns the corresponding result.

@param  condition_list Condition array
@return (boolean) True if condition is met
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.condition_parse (+condition_list)- (#echo(__LINE__)#)")
		f_return = False

		if (len (condition_list) == 2):
		#
			f_value = self.get_variable (condition_list[1])

			if ((condition_list[0] == "ifdef") and (f_value != None)): f_return = True
			elif ((condition_list[0] == "ifndef") and (f_value == None)): f_return = True
		#

		return f_return
	#

	def add_filetype_ascii (self,extension):
	#
		"""
Adds an extension to the list of ASCII file types.

@param extension File type extension to add
		"""

		global _unicode_object
		if (type (extension) == _unicode_object['type']): extension = _unicode_object['str'] (extension,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.add_filetype_ascii ({0})- (#echo(__LINE__)#)".format (extension))
		self.filetype_ascii_list.append (extension)
	#

	def data_parse (self,data,file_pathname,file_name):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		global _unicode_object
		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.data_parse (data)- (#echo(__LINE__)#)")

		f_return = data.replace ("#" + "echo(__FILE__)#",file_name)
		f_return = f_return.replace ("#" + "echo(__FILEPATH__)#",file_pathname)

		if (f_return.find ("#" + "echo(__LINE__)#") > -1):
		#
			data = re.split ("\r\n|\r|\n",f_return)
			f_line = 0

			for f_result in data:
			#
				data[f_line] = f_result.replace ("#" + "echo(__LINE__)#",(str (f_line + 1)))
				f_line += 1
			#

			f_return = "\n".join (data)
		#

		f_result_list = re.findall ("#" + "echo\(((?!_)\w+)\)#",f_return)

		if (len (f_result_list)):
		#
			f_matched_list = [ ]

			for f_result in f_result_list:
			#
				if (f_result not in f_matched_list):
				#
					if (type (f_result) == _unicode_object['type']): f_result = _unicode_object['str'] (f_result,"utf-8")
					f_value = self.get_variable (f_result)

					if (f_value == None): f_return = f_return.replace ("#" + "echo({0})#".format (f_result),f_result)
					else: f_return = f_return.replace ("#" + "echo({0})#".format (f_result),f_value)

					f_matched_list.append (f_result)
				#
			#
		#

		return f_return
	#

	def dir_create (self,dir_path,timeout = -1):
	#
		"""
Creates a directory (or returns the status of is_writable if it exists).
Use slashes - even on Microsoft(R) Windows(R) machines.

@param  dir_path Path to the new directory.
@param  timeout Timeout to use
@return (boolean) True on success
@since  v0.1.00
		"""

		global _unicode_object
		if (type (dir_path) == _unicode_object['type']): dir_path = _unicode_object['str'] (dir_path,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.dir_create ({0},{1:d})- (#echo(__LINE__)#)" % ( dir_path,timeout ))

		f_dir_path = re.sub ("\/$","",dir_path)
		f_dir_path_os = path.normpath (f_dir_path)

		if ((len (f_dir_path) == 0) or (f_dir_path == ".")): f_return = False
		elif ((path.isdir (f_dir_path_os)) and (os.access (f_dir_path_os,os.W_OK))): f_return = True
		elif (path.exists (f_dir_path_os)): f_return = False
		else:
		#
			f_continue_check = True
			f_dir_list = f_dir_path.split ("/")
			f_dir_count = len (f_dir_list)
			f_return = False

			if (timeout < 0): f_timeout_time = (self.time + self.timeout_count)
			else: f_timeout_time = (self.time + timeout)

			if (f_dir_count > 1):
			#
				f_dir_list.pop ()
				f_dir_basepath = "/".join (f_dir_list)
				f_continue_check = self.dir_create (f_dir_basepath)
			#

			if ((f_continue_check) and (f_timeout_time > (time ()))):
			#
				if (self.umask != None): os.umask (int (self.umask,8))

				try:
				#
					os.mkdir (f_dir_path_os,self.chmod_dirs)
					f_return = os.access (f_dir_path_os,os.W_OK)
				#
				except: pass
			#
		#

		return f_return
	#

	def file_parse (self,file_pathname):
	#
		"""
Handle the given file and call the content parse method.

@param  file_pathname Path to the requested file
@return (boolean) True on success
@since  v0.1.00
		"""

		global _unicode_object
		if (type (file_pathname) == _unicode_object['type']): file_pathname = _unicode_object['str'] (file_pathname,"utf-8")

		if (self.debug == None): f_debug = False
		else:
		#
			f_debug= True
			self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.file_parse ({0})- (#echo(__LINE__)#)".format (file_pathname))
		#

		f_return = False

		( f_file_basename,f_file_ext ) = path.splitext (file_pathname)
		f_file_basename = path.basename (file_pathname)
		f_file_ext = f_file_ext[1:]
		f_file_object = direct_file (self.umask,self.chmod_files,self.time,self.timeout_count,f_debug)
		f_file_text_mode = False

		if ((len (f_file_ext) > 0) and (f_file_ext in self.filetype_ascii_list)): f_file_text_mode = True
		elif (len (f_file_basename) > 0): f_file_text_mode = (f_file_basename in self.filetype_ascii_list)

		if (((f_file_text_mode) and (f_file_object.open (file_pathname,True,"r"))) or (f_file_object.open (file_pathname,True,"rb"))):
		#
			f_file_content = f_file_object.read ()
			f_file_object.close ()
		#
		else: f_file_content = None

		f_file_pathname = re.sub ("^{0}".format (re.escape (self.output_strip_prefix)),"",file_pathname)

		if (f_file_content == None): f_return = self.file_write ("",(self.output_path + f_file_pathname))
		elif (f_file_text_mode):
		#
			f_file_list = self.data_parse (f_file_content,f_file_pathname,f_file_basename)

			if (f_file_content.find ("\r\n") > -1): f_file_content = "\r\n"
			elif (f_file_content.find ("\r") > -1): f_file_content = "\r"
			else: f_file_content = "\n"

			if (type (f_file_list) == list): f_return = self.file_write (f_file_content.join (f_file_list),(self.output_path + f_file_pathname),"w+")
		#
		else: f_return = self.file_write (f_file_content,(self.output_path + f_file_pathname))

		return f_return
	#

	def file_write (self,file_content,file_pathname,file_mode = "w+b"):
	#
		"""
Write the given file to the defined location. Create subdirectories if
needed.

@param  file_content Parsed content
@param  file_pathname Path to the output file
@param  file_mode Filemode to use
@return (boolean) True on success
@since  v0.1.00
		"""

		global _unicode_object
		if (type (file_pathname) == _unicode_object['type']): file_pathname = _unicode_object['str'] (file_pathname,"utf-8")
		if (type (file_mode) == _unicode_object['type']): file_mode = _unicode_object['str'] (file_mode,"utf-8")

		if (self.debug == None): f_debug = False
		else:
		#
			f_debug= True
			self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.file_write (file_content,{0},{1})- (#echo(__LINE__)#)".format (file_pathname,file_mode))
		#

		f_dir_path = path.dirname (file_pathname)
		f_return = False

		if ((len (f_dir_path) < 1) or (self.dir_create (f_dir_path))):
		#
			f_file_object = direct_file (self.umask,self.chmod_files,self.time,self.timeout_count,f_debug)

			if (f_file_object.open (file_pathname,False,file_mode)):
			#
				f_return = f_file_object.write (file_content)
				f_file_object.close ()
			#
		#

		return f_return
	#

	def get_variable (self,name):
	#
		"""
Gets the variable content with the given name.

@param  name Variable name
@return (mixed) Variable content; None if undefined
@since  v0.1.00
		"""

		global _unicode_object
		if (type (name) == _unicode_object['type']): name = _unicode_object['str'] (name,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.get_variable ({0})- (#echo(__LINE__)#)".format (name))
		return self.parameters.get (name,None)
	#

	def make_all (self):
	#
		"""
Parse and rewrite all directories and files given as include definitions.

@return (boolean) True on success
@since  v0.1.00
		"""

		global _unicode_object
		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.make_all ()- (#echo(__LINE__)#)")

		f_return = False

		if ((len (self.dir_list) > 0) and (len (self.filetype_list) > 0)): self.workdir_scan ()

		if (len (self.file_dict) < 1): self.trigger_error ("builderSkel/#echo(__FILEPATH__)# -builderSkel.make_all ()- (#echo(__LINE__)#) reports: No valid files found for parsing",self.E_ERROR)
		else:
		#
			for f_file_id in self.file_dict:
			#
				f_file = self.file_dict[f_file_id]
				if (type (f_file) == _unicode_object['type']): f_file = _unicode_object['str'] (f_file,"utf-8")

				sys.stdout.write (">> Parsing {0} ... ".format (f_file))

				if (self.file_parse (f_file)): sys.stdout.write ("done\n")
				else: sys.stdout.write ("failed\n")
			#
		#

		return f_return
	#

	def parser (self,parser_tag,data,data_position = 0,nested_tag_end_position = None):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		global _unicode_object
		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder.data_parse (data)- (#echo(__LINE__)#)")

		if (nested_tag_end_position == None):
		#
			data_position = data.find (parser_tag,data_position)
			f_nested_check = False
		#
		else:
		#
			data_position = data.find (parser_tag,data_position)
			if (data_position >= nested_tag_end_position): data_position = -1

			f_nested_check = True
			f_tag_end_position = -1
		#

		while (data_position > -1):
		#
			f_tag_definition = self.parser_check (data[data_position:])

			if (f_tag_definition == None): data_position += len (parser_tag)
			else:
			#
				f_tag_length = len (f_tag_definition[0])
				f_tag_start_end_position = self.parser_tag_find_end_position (data,(data_position + f_tag_length),f_tag_definition[1])
				f_tag_end_position = -1

				if (f_tag_start_end_position > -1):
				#
					f_tag_end_position = self.parser_tag_end_find_position (data,f_tag_start_end_position,f_tag_definition[2])

					if (f_tag_end_position < 0): f_nested_data = None
					else: f_nested_data = self.parser (parser_tag,data,(data_position + 1),f_tag_end_position)

					while (f_nested_data != None):
					#
						data = f_nested_data
						f_tag_start_end_position = self.parser_tag_find_end_position (data,(data_position + 1),f_tag_definition[1])
						if (f_tag_start_end_position > -1): f_tag_end_position = self.parser_tag_end_find_position (data,f_tag_start_end_position,f_tag_definition[2])

						f_nested_data = self.parser (parser_tag,data,(data_position + 1),f_tag_end_position)
					#
				#

				if (f_tag_end_position > -1): data = self.parser_change (f_tag_definition,data,data_position,f_tag_start_end_position,f_tag_end_position)
				else: data_position += f_tag_length
			#

			if (f_nested_check): data_position = -1
			else: data_position = data.find (parser_tag,data_position)
		#

		if ((f_nested_check) and (f_tag_end_position < 0)): data = None
		return data
	#

	def parser_change (self,tag_definition,data,tag_position,data_position,tag_end_position):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		raise RuntimeError ("Not implemented")
	#

	def parser_check (self,data):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		return None
	#

	def parser_tag_end_find_position (self,data,data_position,tag_end_list):
	#
		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder.parser_tag_end_find_position (data,data_position,tag_end_list)- (#echo(__LINE__)#)")
		f_return = None

		f_continue_check = True
		f_result = -1

		while (((f_return == None) or (f_return > -1)) and (f_continue_check)):
		#
			for f_tag_end in tag_end_list:
			#
				f_result = data.find (f_tag_end,data_position)
				if ((f_result > -1) and ((f_return == None) or (f_result < f_return))): f_return = f_result
			#

			if (f_return == None): f_return = -1
			elif (f_return > -1):
			#
				data_position = f_return
				if (data[(f_return - 1):f_return] != "\\"): f_continue_check = False
			#
		#

		return f_return
	#

	def parser_tag_find_end_position (self,data,data_position,tag_end):
	#
		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder.parser_tag_find_end_position (data,data_position,tag_end)- (#echo(__LINE__)#)")
		f_return = None

		f_continue_check = True

		while (((f_return == None) or (f_return > -1)) and (f_continue_check)):
		#
			f_return = data.find (tag_end,data_position)

			if (f_return > -1):
			#
				data_position = f_return
				if (data[(f_return - 1):f_return] != "\\"): f_continue_check = False
			#
		#

		if (f_return > -1): f_return += len (tag_end)
		return f_return
	#

	def set_exclude (self,exclude):
	#
		"""
Add "exclude" definitions for directories and files.

@param exclude String (delimiter is ",") with exclude names or pathes
@since v0.1.00
		"""

		global _unicode_object
		if (type (exclude) == _unicode_object['type']): exclude = _unicode_object['str'] (exclude,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude ({0})- (#echo(__LINE__)#)".format (exclude))

		if (type (exclude) == str):
		#
			f_exclude_list = exclude.split (",")

			for f_exclude in f_exclude_list:
			#
				self.dir_exclude_list.append (f_exclude)
				self.file_exclude_list.append (f_exclude)
			#
		#
		else: self.trigger_error ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_exclude_dirs (self,exclude):
	#
		"""
Add "exclude" definitions for directories.

@param exclude String (delimiter is ",") with exclude names or pathes
@since v0.1.00
		"""

		global _unicode_object
		if (type (exclude) == _unicode_object['type']): exclude = _unicode_object['str'] (exclude,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude_dirs ({0})- (#echo(__LINE__)#)".format (exclude))

		if (type (exclude) == str):
		#
			f_exclude_list = exclude.split (",")
			for f_exclude in f_exclude_list: self.dir_exclude_list.append (f_exclude)
		#
		else: self.trigger_error ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude_dirs ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_exclude_files (self,exclude):
	#
		"""
Add "exclude" definitions for files.

@param  exclude String (delimiter is ",") with exclude names or pathes
@since  v0.1.00
		"""

		global _unicode_object
		if (type (exclude) == _unicode_object['type']): exclude = _unicode_object['str'] (exclude,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude_files ({0})- (#echo(__LINE__)#)".format (exclude))

		if (type (exclude) == str):
		#
			f_exclude_list = exclude.split (",")
			for f_exclude in f_exclude_list: self.file_exclude_list.append (f_exclude)
		#
		else: self.trigger_error ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_exclude_files ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_trigger (self,py_function = None):
	#
		"""
Set a given function to be called for each exception or error.

@param py_function Python function to be called
@since v0.1.00
		"""

		self.error_callback = py_function
	#

	def set_strip_prefix (self,strip_prefix):
	#
		"""
Define a prefix to be stripped from output pathes.

@param string $strip_prefix Prefix definition
@since v0.1.00
		"""

		global _unicode_object
		if (type (strip_prefix) == _unicode_object['type']): strip_prefix = _unicode_object['str'] (strip_prefix,"utf-8")

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_strip_prefix ({0})- (#echo(__LINE__)#)".format (strip_prefix))

		if (type (strip_prefix) == str): self.output_strip_prefix = strip_prefix
		else: self.trigger_error ("builderSkel/#echo(__FILEPATH__)# -builderSkel.set_strip_prefix ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def trigger_error (self,message,message_type = None):
	#
		"""
Calls a user-defined function for each exception or error.

@param message Error message
@param message_type Error type
@since v0.1.00
		"""

		if (message_type == None): message_type = self.E_NOTICE
		if (self.error_callback != None): self.error_callback (message,message_type)
	#

	def workdir_scan (self):
	#
		"""
Scan given directories for files to be parsed.

@since v0.1.00
		"""

		if (self.debug != None): self.debug.append ("builderSkel/#echo(__FILEPATH__)# -builderSkel.workdir_scan ()- (#echo(__LINE__)#)")

		f_re_content_estripped = re.compile ("^{0}".format (re.escape (self.output_strip_prefix)))
		"""
----------------------------------------------------------------------------
Create a list of files - we need to scan directories recursively ...
----------------------------------------------------------------------------
		"""

		sys.stdout.write ("> Ready to build file index\n")
		f_dir_counter = 0

		while (len (self.dir_list) > f_dir_counter):
		#
			sys.stdout.write (">> Scanning {0} ... ".format (self.dir_list[f_dir_counter]))
			f_dir_path_os = path.normpath (self.dir_list[f_dir_counter])

			if ((path.isdir (f_dir_path_os)) and (os.access (f_dir_path_os,os.R_OK))):
			#
				f_content_list = os.listdir (f_dir_path_os)

				for f_content in f_content_list:
				#
					if (f_content[0] != "."):
					#
						if (self.dir_list[f_dir_counter].endswith ("/")): f_content_extended = self.dir_list[f_dir_counter] + f_content
						else: f_content_extended = "{0}/{1}".format (self.dir_list[f_dir_counter],f_content)

						f_content_extended_os = path.normpath (f_content_extended)
						f_content_estripped = f_re_content_estripped.sub ("",f_content_extended)
						if (type (f_content_estripped) == _unicode_object['type']): f_content_estripped = _unicode_object['str'] (f_content_estripped,"utf-8")

						if (path.isdir (f_content_extended_os)):
						#
							if ((f_content not in self.dir_exclude_list) and (f_content_estripped not in self.dir_exclude_list)): self.dir_list.append (f_content_extended)
						#
						elif (path.isfile (f_content_extended_os)):
						#
							( f_content_basename,f_content_ext ) = path.splitext (f_content)
							f_content_ext = f_content_ext[1:]
							f_content_id = f_content_estripped

							try:
							#
								if (bytes == _unicode_object['type']):
								#
									if (type (f_content_id) == str): f_content_id = _unicode_object['unicode'] (f_content_id,"utf-8")
								#
								elif (type (f_content_id) == _unicode_object['type']): f_content_id = _unicode_object['str'] (f_content_id,"utf-8")
							#
							except:
							#
								if (type (f_content_id) == _unicode_object['type']): f_content_id = _unicode_object['str'] (f_content_id,"utf-8")
							#

							f_content_id = hashlib.md5(f_content_id).hexdigest ()

							if ((len (f_content_ext) > 0) and (f_content_ext in self.filetype_list) and (f_content not in self.file_exclude_list) and (f_content_estripped not in self.file_exclude_list)): self.file_dict[f_content_id] = f_content_extended
						#
					#
				#

				sys.stdout.write ("done\n")
			#
			else: sys.stdout.write ("failed\n")

			f_dir_counter += 1
		#
	#
#

##j## EOF