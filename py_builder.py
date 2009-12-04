# -*- coding: utf-8 -*-
##j## BOF

"""/*n// NOTE
----------------------------------------------------------------------------
pyBuilder
Build Python code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pyBuilder

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(pyBuilderVersion)#
pyBuilder/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n*/"""
"""
This is the main Python "make" worker class file.

@internal   We are using epydoc (JavaDoc style) to automate the
            documentation process for creating the Developer's Manual.
            Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage pyBuilder
@since      v0.1.00
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
"""

from file import direct_file
from os import path
import os,re,stat,sys,time

try: import hashlib as pyHashlib
except Exception,g_handled_exception: import md5 as pyHashlib

class direct_py_builder (object):
#
	"""
Provides a Python "make" environment object.

@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage pyBuilder
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
	dir_array = [ ]
	"""
Directories to be scanned
	"""
	dir_exclude_array = [ ]
	"""
Directories to be ignored while scanning
	"""
	error_callback = None
	"""
Function to be called for logging exceptions and other errors
	"""
	file_array = { }
	"""
Files to be parsed
	"""
	file_exclude_array = [ ]
	"""
Files to be ignored while scanning
	"""
	filetype_array = [ ]
	"""
Filetype extensions to be parsed
	"""
	filetype_ascii_array = [ ]
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

	def __init__ (self,f_parameters,f_include,f_output_path,f_filetype,f_umask = None,f_chmod_files = None,f_chmod_dirs = None,f_time = -1,f_timeout_count = 5,f_debug = False):
	#
		"""
Constructor __init__ (direct_py_builder)

@param f_parameters DEFINE statements
@param f_include String (delimiter is ",") with directory or file names to
       be included.
@param f_output_path Output path
@param f_filetype String (delimiter is ",") with extensions of files to be
       parsed.
@param f_umask umask to set before creating new directories or files
@param f_chmod_files chmod to set when creating a new file
@param f_chmod_dirs chmod to set when creating a new directory
@param f_time Current UNIX timestamp
@param f_timeout_count Retries before timing out
@since v0.1.00
		"""

		if (f_debug): self.debug = [ "pyBuilder/#echo(__FILEPATH__)# -pyBuilder->__construct (direct_py_builder)- (#echo(__LINE__)#)" ]
		else: self.debug = None

		if (f_chmod_dirs == None): self.chmod_dirs = 0750
		else: self.chmod_dirs = int (f_chmod_dirs,8)

		self.chmod_files = f_chmod_files
		self.dir_exclude_array = [ ]
		self.error_callback = None
		self.file_exclude_array = [ ]
		self.filetype_array = f_filetype.split (",")
		self.filetype_ascii_array = [ "txt","js","py","xml" ]

		if ((len (f_output_path)) and (not f_output_path.endswith ("/")) and (not f_output_path.endswith ("\\"))): f_output_path += path.sep
		self.output_path = f_output_path

		self.output_strip_prefix = "";

		if (type (f_parameters) == dict): self.parameters = f_parameters
		else: self.parameters = { }

		if (f_time < 0): self.time = time.time ()
		else: self.time = f_time

		self.timeout_count = f_timeout_count
		self.umask = f_umask

		self.dir_array = [ ]
		self.file_array = { }
		f_data_array = f_include.split (",")

		for f_data in f_data_array:
		#
			if (path.isdir (f_data)): self.dir_array.append (f_data)
			elif (path.isfile (f_data)): self.file_array[pyHashlib.md5(f_data).hexdigest ()] = f_data
		#
	#

	def condition_parse (self,f_condition_array):
	#
		"""
Parse the given condition and returns the corresponding result.

@param  f_condition_array Condition array
@return (boolean) True if condition is met
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->condition_parse (+f_condition_array)-")
		f_return = False

		if (len (f_condition_array) == 2):
		#
			f_value = self.get_variable (f_condition_array[1])

			if ((f_condition_array[0] == "ifdef") and (f_value != None)): f_return = True
			elif ((f_condition_array[0] == "ifndef") and (f_value == None)): f_return = True
		#

		return f_return
	#

	def add_filetype_ascii (self,f_extension):
	#
		"""
Adds an extension to the list of ASCII file types.

@param f_extension File type extension to add
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->add_filetype_ascii (%s)-" % f_extension)
		self.filetype_ascii_array.append (f_extension)
	#

	def data_parse (self,f_data,f_file_path,f_file_name):
	#
		"""
Parse the given content and return a line based array.

@param  f_data Data to be parsed
@param  f_file_path File path
@param  f_file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->data_parse (+f_data)-")
		f_return = False

		f_data = self.data_parse_walker(f_data).replace ("#echo(__FILE__)#",f_file_name)
		f_data = f_data.replace ("#echo(__FILEPATH__)#",f_file_path)
		f_result_array = re.findall ("#echo\(((?!_)\w+)\)#",f_data)

		if (len (f_result_array)):
		#
			f_matched_array = [ ]

			for f_result in f_result_array:
			#
				if (not f_result in f_matched_array):
				#
					f_value = self.get_variable (f_result)

					if (f_value == None): f_data = f_data.replace ("#echo(%s)#" % f_result,f_result)
					else: f_data = f_data.replace ("#echo(%s)#" % f_result,f_value)

					f_matched_array.append (f_result)
				#
			#
		#

		f_return = re.split ("\r\n|\r|\n",f_data)

		if (f_data.find ("#echo(__LINE__)#") > -1):
		#
			f_line = 0

			for f_data in f_return:
			#
				f_return[f_line] = f_data.replace ("#echo(__LINE__)#",(str (f_line + 1)))
				f_line += 1
			#
		#

		return f_return
	#

	def data_parse_walker (self,f_data,f_zone_valid = False,f_zone_tag = ""):
	#
		"""
Parse the given content part recursively and returns the result.

@param  f_data Input data
@param  f_zone_valid True if the zone condition resulted in false
@param  f_zone_tag Zone end tag
@return (mixed) Parsed content part
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->data_parse_walker (+f_data,+f_zone_valid,%s)-" % f_zone_tag)
		f_return = False

		if (len (f_zone_tag) > 0):
		#
			f_return = [ "","" ]
			f_sub = True
		#
		else:
		#
			f_return = ""
			f_sub = False
			f_zone_valid = True
		#

		f_command_object = None
		f_command_false_positive = False
		f_data_pointer = 0
		f_re_command = re.compile ("^\"\"\"#(\w+)\((\w+)\)$")
		f_re_condition = re.compile ("(\"\"\"#\w+\(\w+\))")
		f_re_condition_single = re.compile ("^\:(\r\n|\r|\n)(.*?)$",re.S)
		f_re_condition_multiline = re.compile ("^[ ]\"\"\"(\r\n|\r|\n)(.*?)$",re.S)
		f_re_newline = re.compile ("^(\r\n|\r|\n)")

		if (f_sub): f_data_array = [ f_data ]
		else: f_data_array = f_re_condition.split (f_data,1)

		while (len (f_data_array) > f_data_pointer):
		#
			f_command_object = f_re_command.match (f_data_array[f_data_pointer])
			if (f_command_object != None): f_data_pointer += 1

			if (len (f_data_array) > f_data_pointer):
			#
				if (f_command_object == None):
				#
					if (f_sub):
					#
						f_command_false_positive = True
						f_data_sub_array = f_data_array[f_data_pointer].split (f_zone_tag,2)

						while ((f_command_false_positive) and (len (f_data_sub_array) == 2)):
						#
							f_data_sub_length = len (f_data_sub_array[1])

							if ((f_data_sub_length > 1) and (f_data_sub_array[1][:3] == '"""')):
							#
								f_command_false_positive = False
								if (f_zone_valid): f_return[0] += f_data_sub_array[0].replace ("*\/","*/")
								f_return[1] += f_data_sub_array[1][3:]
							#
							elif ((f_data_sub_length > 3) and (f_data_sub_array[1][:5] == '\\n"""')):
							#
								f_command_false_positive = False
								if (f_zone_valid): f_return[0] += f_data_sub_array[0].replace ("*\/","*/")
								f_return[1] += f_re_newline.replace ("",f_data_sub_array[1][5:])
							#
							else:
							#
								if (f_zone_valid): f_return[0] += "%s%s" % ( (f_data_sub_array[0].replace ('"\""','"""')),f_zone_tag )
								f_data_array[f_data_pointer] = f_data_sub_array[1]
								f_data_sub_array = f_data_array[f_data_pointer].split (f_zone_tag,2)
							#
						#
					#
					else: f_return += f_data_array[f_data_pointer]
				#
				elif (f_zone_valid):
				#
					f_return_array = None
					f_condition_single_object = f_re_condition_single.match (f_data_array[f_data_pointer])
					f_condition_multiline_object = f_re_condition_multiline.match (f_data_array[f_data_pointer])

					if (f_condition_single_object != None):
					#
						if ((f_command_object.group (1) == "ifdef") or (f_command_object.group (1) == "ifndef")): f_return_array = self.data_parse_walker (f_condition_single_object.group (2),(self.condition_parse (f_command_object.groups ())),":#")
						else: f_command_false_positive = True
					#
					elif (f_data_array[f_data_pointer][0] == ":"):
					#
						if ((f_command_object.group (1) == "ifdef") or (f_command_object.group (1) == "ifndef")): f_return_array = self.data_parse_walker (f_data_array[f_data_pointer][1:],(self.condition_parse (f_command_object.groups ())),":#")
						else: f_command_false_positive = True
					#
					elif (f_data_array[f_data_pointer][:4] == '#"""'):
					#
						if (f_command_object.group (1) == "echo"):
						#
							if (f_command_object.group (1) != "__LINE__"):
							#
								f_value = self.get_variable (f_command_object.group (2))

								if (f_value == None): f_return += f_command_object.group (2)
								else: f_return += f_value
							#

							f_return += f_data_array[f_data_pointer][3:]
						#
						else: f_command_false_positive = True
					#
					elif (f_condition_multiline_object != None):
					#
						if ((f_command_object.group (1) == "ifdef") or (f_command_object.group (1) == "ifndef")): f_return_array = self.data_parse_walker (f_re_condition_multiline.group (2),(self.condition_parse (f_command_object.groups ())),'""" #')
						else: f_command_false_positive = True
					#
					elif (f_data_array[f_data_pointer][:4] == ' """'):
					#
						if ((f_command_object.group (1) == "ifdef") or (f_command_object.group (1) == "ifndef")): f_return_array = self.data_parse_walker (f_data_array[f_data_pointer][3:],(self.condition_parse (f_command_object.groups ())),'""" #')
						else: f_command_false_positive = True
					#
					else: f_command_false_positive = True

					if (f_command_false_positive): f_return += f_command_object.group (0)
					elif (f_return_array != None):
					#
						f_return += f_return_array[0]
						f_data_array = f_re_condition.split (f_data,1)

						if (len (f_data_array[2]) > 0): f_data_pointer = -1
						else: f_return += f_return_array[1]
					#

					f_command_object = None
				#

				if (f_command_false_positive):
				#
					if (f_sub): f_return[0] += f_data_array[f_data_pointer]
					else: f_return += f_data_array[f_data_pointer]

					f_command_false_positive = False
				#
			#
			else: f_return += f_command_object.group (0)

			f_data_pointer += 1
		#

		return f_return
	#

	def dir_create (self,f_dir_path,f_timeout = -1):
	#
		"""
Creates a directory (or returns the status of is_writable if it exists).
Use slashes - even on Microsoft(R) Windows(R) machines.

@param  f_dir_path Path to the new directory.
@param  f_timeout Timeout to use
@return (boolean) True on success
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->dir_create (%s,%i)-" % ( f_dir_path,f_timeout ))

		f_dir_path = re.sub ("\/$","",f_dir_path)
		f_dir_path_os = path.normpath (f_dir_path)

		if ((len (f_dir_path) == 0) or (f_dir_path == ".")): f_return = False
		elif ((path.isdir (f_dir_path_os)) and (os.access (f_dir_path_os,os.W_OK))): f_return = True
		elif (path.exists (f_dir_path_os)): f_return = False
		else:
		#
			f_continue_check = True
			f_dir_array = f_dir_path.split ("/")
			f_dir_count = len (f_dir_array)
			f_return = False

			if (f_timeout < 0): f_timeout_time = (self.time + self.timeout_count)
			else: f_timeout_time = (self.time + f_timeout)

			if (f_dir_count > 1):
			#
				f_dir_array.pop ()
				f_dir_basepath = "/".join (f_dir_array)
				f_continue_check = self.dir_create (f_dir_basepath)
			#

			if ((f_continue_check) and (f_timeout_time > (time.time ()))):
			#
				if (self.umask != None): os.umask (int (self.umask,8))

				try:
				#
					os.mkdir (f_dir_path_os,self.chmod_dirs)
					f_return = os.access (f_dir_path_os,os.W_OK)
				#
				except Exception,f_unhandled_exception: pass
			#
		#

		return f_return
	#

	def file_parse (self,f_file_path):
	#
		"""
Handle the given file and call the content parse method.

@param  f_file_path Path to the requested file
@return (boolean) True on success
@since  v0.1.00
		"""

		if (self.debug == None): f_debugging = False
		else:
		#
			f_debugging= True
			self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->file_parse (%s)-" % f_file_path)
		#

		f_return = False

		( f_file_basename,f_file_ext ) = path.splitext (f_file_path)
		f_file_basename = path.basename (f_file_path)
		f_file_ext = f_file_ext[1:]
		f_file_object = direct_file (self.umask,self.chmod_files,self.time,self.timeout_count,f_debugging)
		f_file_text_mode = False

		if ((len (f_file_ext) > 0) and (f_file_ext in self.filetype_ascii_array)): f_file_text_mode = True
		elif (len (f_file_basename) > 0): f_file_text_mode = (f_file_basename in self.filetype_ascii_array)

		if (((f_file_text_mode) and (f_file_object.open (f_file_path,True,"r"))) or (f_file_object.open (f_file_path,True,"rb"))):
		#
			f_file_content = f_file_object.read ()
			f_file_object.close ()
		#
		else: f_file_content = None

		f_file_path = re.sub ("^%s" % (re.escape (self.output_strip_prefix)),"",f_file_path)

		if ((f_file_text_mode) and (f_file_content != None)):
		#
			f_file_array = self.data_parse (f_file_content,f_file_path,f_file_basename)

			if (f_file_content.find ("\r\n") > -1): f_file_content = "\r\n"
			elif (f_file_content.find ("\r") > -1): f_file_content = "\r"
			else: f_file_content = "\n"

			if (type (f_file_array) == list): f_return = self.file_write (f_file_content.join (f_file_array),(self.output_path + f_file_path),"w+")
		#
		else: f_return = self.file_write (f_file_content,(self.output_path + f_file_path))

		return f_return
	#

	def file_write (self,f_file_content,f_file_path,f_file_mode = "w+b"):
	#
		"""
Write the given file to the defined location. Create subdirectories if
needed.

@param  f_file_content Parsed content
@param  f_file_path Path to the output file
@param  f_file_mode Filemode to use
@return (boolean) True on success
@since  v0.1.00
		"""

		if (self.debug == None): f_debugging = False
		else:
		#
			f_debugging= True
			self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->file_write (+f_file_content,%s,%s)-" % ( f_file_path,f_file_mode ))
		#

		f_dir_path = path.dirname (f_file_path)
		f_return = False

		if ((len (f_dir_path) < 1) or (self.dir_create (f_dir_path))):
		#
			f_file_object = direct_file (self.umask,self.chmod_files,self.time,self.timeout_count,f_debugging)

			if (f_file_object.open (f_file_path,False,f_file_mode)):
			#
				f_return = f_file_object.write (f_file_content)
				f_file_object.close ()
			#
		#

		return f_return
	#

	def get_variable (self,f_name):
	#
		"""
Gets the variable content with the given name.

@param  f_name Variable name
@return (mixed) Variable content; None if undefined
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->get_variable (%s)-" % f_name)

		if (self.parameters.has_key (f_name)): return self.parameters[f_name]
		else: return None
	#

	def make_all (self):
	#
		"""
Parse and rewrite all directories and files given as include definitions.

@return (boolean) True on success
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->make_all ()-")
		f_return = False

		if ((len (self.dir_array) > 0) and (len (self.filetype_array) > 0)): self.workdir_scan ()

		if (len (self.file_array) < 1): self.trigger_error ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->make_all ()- (#echo(__LINE__)#) reports: No valid files found for parsing",self.E_ERROR)
		else:
		#
			for f_file_id in self.file_array:
			#
				f_file = self.file_array[f_file_id]
				sys.stdout.write (">> Parsing %s ... " % f_file)

				if (self.file_parse (f_file)): print ("done")
				else: print ("failed")
			#
		#

		return f_return
	#

	def set_exclude (self,f_exclude):
	#
		"""
Add "exclude" definitions for directories and files.

@param f_exclude String (delimiter is ",") with exclude names or pathes
@since v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude (%s)-" % f_exclude)

		f_type = type (f_exclude)

		if ((f_type == str) or (f_type == unicode)):
		#
			f_exclude_array = f_exclude.split (",")

			for f_exclude_array in f_exclude:
			#
				self.dir_exclude_array.append (f_exclude)
				self.file_exclude_array.append (f_exclude)
			#
		#
		else: self.trigger_error ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_exclude_dirs (self,f_exclude):
	#
		"""
Add "exclude" definitions for directories.

@param f_exclude String (delimiter is ",") with exclude names or pathes
@since v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude_dirs (%s)-" % f_exclude)

		f_type = type (f_exclude)

		if ((f_type == str) or (f_type == unicode)):
		#
			f_exclude_array = f_exclude.split (",")
			for f_exclude_array in f_exclude: self.dir_exclude_array.append (f_exclude)
		#
		else: self.trigger_error ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude_dirs ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_exclude_files (self,f_exclude):
	#
		"""
Add "exclude" definitions for files.

@param  f_exclude String (delimiter is ",") with exclude names or pathes
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude_files (%s)-" % f_exclude)

		f_type = type (f_exclude)

		if ((f_type == str) or (f_type == unicode)):
		#
			f_exclude_array = f_exclude.split (",")
			for f_exclude_array in f_exclude: self.file_exclude_array.append (f_exclude)
		#
		else: self.trigger_error ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_exclude_files ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def set_trigger (self,f_function = None):
	#
		"""
Set a given function to be called for each exception or error.

@param f_function Python function to be called
@since v0.1.00
		"""

		self.error_callback = f_function
	#

	def set_strip_prefix (self,f_strip_prefix):
	#
		"""
Define a prefix to be stripped from output pathes.

@param string $f_strip_prefix Prefix definition
@since v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_strip_prefix (%s)-" % f_strip_prefix)

		f_type = type (f_strip_prefix)

		if ((f_type == str) or (f_type == unicode)): self.output_strip_prefix = f_strip_prefix
		else: self.trigger_error ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->set_strip_prefix ()- (#echo(__LINE__)#) reports: Given parameter is not a string",self.E_NOTICE)
	#

	def trigger_error (self,f_message,f_type = None):
	#
		"""
Calls a user-defined function for each exception or error.

@param f_message Error message
@param f_type Error type
@since v0.1.00
		"""

		if (f_type == None): f_type = self.E_NOTICE
		if (self.error_callback != None): self.error_callback (f_message,f_type)
	#

	def workdir_scan (self):
	#
		"""
Scan given directories for files to be parsed.

@since v0.1.00
		"""

		if (self.debug != None): self.debug.append ("pyBuilder/#echo(__FILEPATH__)# -pyBuilder->workdir_scan ()-")

		f_re_content_estripped = re.compile ("^%s" % re.escape (self.output_strip_prefix))
		"""
----------------------------------------------------------------------------
Create a list of files - we need to scan directories recursively ...
----------------------------------------------------------------------------
		"""

		print ("> Ready to build file index")
		f_dir_counter = 0

		while (len (self.dir_array) > f_dir_counter):
		#
			sys.stdout.write (">> Scanning %s ... " % self.dir_array[f_dir_counter])
			f_dir_path_os = path.normpath (self.dir_array[f_dir_counter])

			if ((path.isdir (f_dir_path_os)) and (os.access (f_dir_path_os,os.R_OK))):
			#
				f_content_array = os.listdir (f_dir_path_os)

				for f_content in f_content_array:
				#
					if (f_content[0] != "."):
					#
						if (self.dir_array[f_dir_counter].endswith ("/")): f_content_extended = self.dir_array[f_dir_counter] + f_content
						else: f_content_extended = "%s/%s" % ( self.dir_array[f_dir_counter],f_content )

						f_content_extended_os = path.normpath (f_content_extended)
						f_content_estripped = f_re_content_estripped.sub ("",f_content_extended)

						if (path.isdir (f_content_extended_os)):
						#
							if ((not f_content in self.dir_exclude_array) and (not f_content_estripped in self.dir_exclude_array)): self.dir_array.append (f_content_extended)
						#
						elif (path.isfile (f_content_extended_os)):
						#
							( f_content_basename,f_content_ext ) = path.splitext (f_content)
							f_content_ext = f_content_ext[1:]
							f_content_id = pyHashlib.md5(f_content_estripped).hexdigest ()

							if ((len (f_content_ext) > 0) and (f_content_ext in self.filetype_array) and (not f_content in self.file_exclude_array) and (not f_content_estripped in self.file_exclude_array)): self.file_array[f_content_id] = f_content_extended
						#
					#
				#

				print ("done")
			#
			else: print ("failed")

			f_dir_counter += 1
		#
	#
#

##j## EOF