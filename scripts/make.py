# -*- coding: utf-8 -*-
##j## BOF

"""
This is a Python "make" script to generate different output Javascript
scripts based on "makefile.py" definitions for example for GPL/commercial
differences.
"""
"""n// NOTE
----------------------------------------------------------------------------
jsBuilder
Build Javascript code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?js;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(jsBuilderVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from optparse import OptionParser
from js_builder import direct_js_builder
import os, re, sys

sys.path.append(os.getcwd())

try: import makefile
except: pass

_direct_js_builder_make = None

class direct_make(object):
#
	"""
"direct_make" is the main application object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   jsBuilder
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	option_parser = None
	"""
OptionParser instance
	"""

	"""
----------------------------------------------------------------------------
Construct the class
----------------------------------------------------------------------------
	"""

	def __init__(self):
	#
		"""
Constructor __init__ (direct_make)

:since: v0.1.00
		"""

		self.option_parser = OptionParser()
		self.option_parser.add_option("--define", action = "store", type = "string", dest = "define")
		self.option_parser.add_option("--filetype", action = "store", type = "string", dest = "filetype")
		self.option_parser.add_option("--include", action = "store", type = "string", dest = "include")
		self.option_parser.add_option("--output_dirs_chmod", action = "store", type = "string", dest = "output_dirs_chmod")
		self.option_parser.add_option("--output_files_chmod", action = "store", type = "string", dest = "output_files_chmod")
		self.option_parser.add_option("--output_path", action = "store", type = "string", dest = "output_path")
		self.option_parser.add_option("--exclude", action = "store", type = "string", dest = "exclude")
		self.option_parser.add_option("--exclude_dirs", action = "store", type = "string", dest = "exclude_dirs")
		self.option_parser.add_option("--exclude_files", action = "store", type = "string", dest = "exclude_files")
		self.option_parser.add_option("--strip_prefix", action = "store", type = "string", dest = "strip_prefix")
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v1.0.0
		"""

		( options, invalid_args ) = self.option_parser.parse_args()

		global _direct_jsBuilder_parameters
		targets = [ ]

		if (len(_direct_jsBuilder_parameters) > 0 and type(_direct_jsBuilder_parameters) == list):
		#
			for target in _direct_jsBuilder_parameters:
			#
				if ("make_output_path" in target): targets.append(target)
			#
		#
		elif (options.output_path != None):
		#
			_direct_jsBuilder_parameters.update({ "make_output_path":options.output_path })
			targets.append(_direct_jsBuilder_parameters)
		#

		if (options.filetype == None or options.include == None or len(targets) == 0): self.option_parser.print_help()
		else:
		#
			js_builder = None
			self.option_parser = None

			for target in targets:
			#
				if (options.define != None):
				#
					define_array = options.define.split(",")
					re_define = re.compile("^(\w+)\=(.+?)$")

					for define in define_array:
					#
						result_object = re_define.match(define)

						if (result_object == None):
						#
							define_key = define
							define_value = True
						#
						else:
						#
							define_key = result_object.group(1)
							define_value = result_object.group(2)
						#

						target[define_key] = define_value
					#
				#

				if (js_builder == None): js_builder = direct_js_builder(target, options.include, target['make_output_path'], options.filetype, default_chmod_files = options.output_files_chmod, default_chmod_dirs = options.output_dirs_chmod)
				else: js_builder.set_new_target(target, options.include, target['make_output_path'], options.filetype)

				if (options.exclude != None): js_builder.set_exclude(options.exclude)
				if (options.exclude_dirs != None): js_builder.set_exclude_dirs(options.exclude_dirs)
				if (options.exclude_files != None): js_builder.set_exclude_files(options.exclude_files)
				if (options.strip_prefix != None): js_builder.set_strip_prefix(options.strip_prefix)
				js_builder.make_all()
			#
		#
	#
#

print("""
----------------------------------------------------------------------------
jsBuilder #echo(jsBuilderVersion)#
(C) direct Netware Group - All rights reserved
----------------------------------------------------------------------------
""");

try:
#
	if (hasattr(makefile, "direct_makefile_js_set")): _direct_jsBuilder_parameters = makefile.direct_makefile_js_set()
	else: _direct_jsBuilder_parameters = makefile.direct_makefile_set()
#
except: _direct_jsBuilder_parameters = { }

try:
#
	_direct_js_builder_make = direct_make()
	_direct_js_builder_make.run()
#
except:
#
	sys.stderr.write("{0!r}".format(sys.exc_info()))
	sys.exit(1)
#
else: sys.exit(0)

##j## EOF