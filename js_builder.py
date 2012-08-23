# -*- coding: utf-8 -*-
##j## BOF

"""
This is the main JavaScript "make" worker class file.

@internal   We are using epydoc (JavaDoc style) to automate the
            documentation process for creating the Developer's Manual.
            Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage jsBuilder
@since      v0.1.00
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
jsBuilder
Build JavaScript code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?jsBuilder

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(jsBuilderVersion)#
jsBuilder/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
from slimit.minifier import minify

from builder_skel import direct_builder_skel

class direct_js_builder (direct_builder_skel):
#
	"""
Provides a Javascript "make" environment object.

@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage jsBuilder
@since      v1.0.0
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
	"""

	def data_parse (self,data,file_pathname,file_name):
	#
		"""
Parse the given content.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("jsBuilder/#echo(__FILEPATH__)# -jsBuilder.data_parse (data)- (#echo(__LINE__)#)")

		if (self.get_variable ("debug") == None): data = minify (data,True)
		if (self.get_variable ("js_header") != None): data = "// {0}\n{1}".format (self.get_variable ("js_header"),data)
		return direct_builder_skel.data_parse (self,data,file_pathname,file_name)
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

		if ((self.get_variable ("debug") == None) and (self.get_variable ("js_min_filenames") != None)):
		#
			( f_file_pathname,f_file_ext ) = path.splitext (file_pathname)
			if (len (f_file_ext) > 0): file_pathname = "{0}.min{1}".format (f_file_pathname,f_file_ext)
		#

		return direct_builder_skel.file_write (self,file_content,file_pathname,file_mode = "w+b")
	#
#

##j## EOF