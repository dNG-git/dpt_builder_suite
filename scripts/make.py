# -*- coding: utf-8 -*-
##j## BOF

"""
This is a Python "make" script to generate different output Python scripts
based on "makefile.py" definitions for example for GPL/commercial
differences.
"""
"""n// NOTE
----------------------------------------------------------------------------
pyBuilder
Build Python code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?py;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(pyBuilderVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from argparse import ArgumentParser
from py_builder import direct_py_builder
import os, re, sys

sys.path.append(os.getcwd())

try: import makefile
except: pass

class direct_make(object):
#
	"""
"direct_make" is the main application object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pyBuilder
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	arg_parser = None
	"""
ArgumentParser instance
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

		self.arg_parser = ArgumentParser()
		self.arg_parser.add_argument("--define", action = "store", type = str, dest = "define")
		self.arg_parser.add_argument("--filetype", action = "store", type = str, dest = "filetype")
		self.arg_parser.add_argument("--include", action = "store", type = str, dest = "include")
		self.arg_parser.add_argument("--output_dirs_chmod", action = "store", type = str, dest = "output_dirs_chmod")
		self.arg_parser.add_argument("--output_files_chmod", action = "store", type = str, dest = "output_files_chmod")
		self.arg_parser.add_argument("--output_path", action = "store", type = str, dest = "output_path")
		self.arg_parser.add_argument("--exclude", action = "store", type = str, dest = "exclude")
		self.arg_parser.add_argument("--exclude_dirs", action = "store", type = str, dest = "exclude_dirs")
		self.arg_parser.add_argument("--exclude_files", action = "store", type = str, dest = "exclude_files")
		self.arg_parser.add_argument("--strip_prefix", action = "store", type = str, dest = "strip_prefix")

		self.arg_parser.add_argument("-v", "--version", action="version", version="http://www.direct-netware.de/redirect.php?py;builder")
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v1.0.0
		"""

		args = self.arg_parser.parse_args()

		global _direct_pyBuilder_parameters
		targets = [ ]

		if (len(_direct_pyBuilder_parameters) > 0 and type(_direct_pyBuilder_parameters) == list):
		#
			for target in _direct_pyBuilder_parameters:
			#
				if ("make_output_path" in target): targets.append(target)
			#
		#
		elif (args.output_path != None):
		#
			_direct_pyBuilder_parameters.update({ "make_output_path": args.output_path })
			targets.append(_direct_pyBuilder_parameters)
		#

		if (args.filetype == None or args.include == None or len(targets) == 0): self.option_parser.print_help()
		else:
		#
			py_builder = None
			self.option_parser = None

			for target in targets:
			#
				if (args.define != None):
				#
					define_array = args.define.split(",")
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

				if (py_builder == None): py_builder = direct_py_builder(target, args.include, target['make_output_path'], args.filetype, default_chmod_files = args.output_files_chmod, default_chmod_dirs = args.output_dirs_chmod)
				else: py_builder.set_new_target(target, args.include, target['make_output_path'], args.filetype)

				if (args.exclude != None): py_builder.set_exclude(args.exclude)
				if (args.exclude_dirs != None): py_builder.set_exclude_dirs(args.exclude_dirs)
				if (args.exclude_files != None): py_builder.set_exclude_files(args.exclude_files)
				if (args.strip_prefix != None): py_builder.set_strip_prefix(args.strip_prefix)
				py_builder.make_all()
			#
		#
	#
#

print("""
----------------------------------------------------------------------------
pyBuilder #echo(pyBuilderVersion)#
(C) direct Netware Group - All rights reserved
----------------------------------------------------------------------------
""");

try:
#
	if (hasattr(makefile, "direct_makefile_py_set")): _direct_pyBuilder_parameters = makefile.direct_makefile_py_set()
	else: _direct_pyBuilder_parameters = makefile.direct_makefile_set()
#
except: _direct_pyBuilder_parameters = { }

try:
#
	g_make = direct_make()
	g_make.run()
#
except SystemExit: pass
except:
#
	sys.stderr.write("{0!r}".format(sys.exc_info()))
	sys.exit(1)
#

##j## EOF