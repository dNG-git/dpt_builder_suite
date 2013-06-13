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
http://www.direct-netware.de/redirect.py?js;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(jsBuilderVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from argparse import ArgumentParser
from js_builder import JsBuilder
import os
import re
import sys

sys.path.append(os.getcwd())

try: import makefile
except: pass

class Make(object):
#
	"""
"Make" is the main application object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   jsBuilder
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Make)

:since: v0.1.00
		"""

		self.arg_parser = ArgumentParser()
		"""
ArgumentParser instance
		"""

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

		self.arg_parser.add_argument("-v", "--version", action="version", version="http://www.direct-netware.de/redirect.py?js;builder")
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v1.0.0
		"""

		args = self.option_parser.parse_args()

		global _parameters
		targets = [ ]

		if (len(_parameters) > 0 and type(_parameters) == list):
		#
			for target in _parameters:
			#
				if ("make_output_path" in target): targets.append(target)
			#
		#
		elif (args.output_path != None):
		#
			_parameters.update({ "make_output_path": args.output_path })
			targets.append(_parameters)
		#

		if (args.filetype == None or args.include == None or len(targets) == 0): self.option_parser.print_help()
		else:
		#
			js_builder = None
			self.option_parser = None

			for target in targets:
			#
				if (args.define != None):
				#
					define_array = args.define.split(",")
					re_define = re.compile("^(\w+)\=(.+?)$")

					for define in define_array:
					#
						re_result = re_define.match(define)

						if (re_result == None):
						#
							define_key = define
							define_value = True
						#
						else:
						#
							define_key = re_result.group(1)
							define_value = re_result.group(2)
						#

						target[define_key] = define_value
					#
				#

				if (js_builder == None): js_builder = JsBuilder(target, args.include, target['make_output_path'], args.filetype, default_chmod_files = args.output_files_chmod, default_chmod_dirs = args.output_dirs_chmod)
				else: js_builder.set_new_target(target, args.include, target['make_output_path'], args.filetype)

				if (args.exclude != None): js_builder.set_exclude(args.exclude)
				if (args.exclude_dirs != None): js_builder.set_exclude_dirs(args.exclude_dirs)
				if (args.exclude_files != None): js_builder.set_exclude_files(args.exclude_files)
				if (args.strip_prefix != None): js_builder.set_strip_prefix(args.strip_prefix)
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
	if (hasattr(makefile, "direct_makefile_js_set")): _parameters = makefile.direct_makefile_js_set()
	else: _parameters = makefile.direct_makefile_set()
#
except: _parameters = { }

try:
#
	make = Make()
	make.run()
#
except SystemExit: pass
except:
#
	sys.stderr.write("{0!r}".format(sys.exc_info()))
	sys.exit(1)
#

##j## EOF