# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;builder_suite

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(dptBuilderSuiteVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error

from argparse import ArgumentParser
import os
import re
import sys

from dpt_builder_suite.py_builder import PyBuilder

sys.path.append(os.getcwd())

try: import makefile
except ImportError: pass

class MakePy(object):
    """
"MakePy" is the main application object for handling Python files.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: builder_suite
:since:      v0.1.1
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = ( "arg_parser", )
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(MakePy)

:since: v0.1.1
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

        self.arg_parser.add_argument("-v", "--version", action = "version", version = "#echo(dptBuilderSuiteVersion)#")
    #

    def run(self):
        """
Executes registered callbacks for the active application.

:since: v0.1.1
        """

        # global: _parameters

        args = self.arg_parser.parse_args()
        targets = [ ]

        if (len(_parameters) > 0 and type(_parameters) is list):
            for target in _parameters:
                if ("make_output_path" in target): targets.append(target)
            #
        elif (args.output_path is not None):
            _parameters.update({ "make_output_path": args.output_path })
            targets.append(_parameters)
        #

        if (args.filetype is None or args.include is None or len(targets) == 0): self.arg_parser.print_help()
        else:
            py_builder = None
            self.arg_parser = None

            for target in targets:
                if (args.define is not None):
                    define_array = args.define.split(",")
                    re_define = re.compile("^(\\w+)\\=(.+)$")

                    for define in define_array:
                        re_result = re_define.match(define)

                        if (re_result is None):
                            define_key = define
                            define_value = True
                        else:
                            define_key = re_result.group(1)
                            define_value = re_result.group(2)
                        #

                        target[define_key] = define_value
                    #
                #

                if (py_builder is None):
                    py_builder = PyBuilder(target,
                                           args.include,
                                           target['make_output_path'],
                                           args.filetype,
                                           default_chmod_files = args.output_files_chmod,
                                           default_chmod_dirs = args.output_dirs_chmod
                                          )
                else: py_builder.set_new_target(target, args.include, target['make_output_path'], args.filetype)

                if (args.exclude is not None): py_builder.set_exclude(args.exclude)
                if (args.exclude_dirs is not None): py_builder.set_exclude_dirs(args.exclude_dirs)
                if (args.exclude_files is not None): py_builder.set_exclude_files(args.exclude_files)
                if (args.strip_prefix is not None): py_builder.set_strip_prefix(args.strip_prefix)
                py_builder.make_all()
            #
        #
    #
#

print("""
----------------------------------------------------------------------------
builderSuite for Python #echo(dptBuilderSuiteVersion)#
(C) direct Netware Group - All rights reserved
----------------------------------------------------------------------------
""")

try:
    if (hasattr(makefile, "direct_makefile_py_set")): _parameters = makefile.direct_makefile_py_set()
    else: _parameters = makefile.direct_makefile_set()
except NameError: _parameters = { }

try:
    make_py = MakePy()
    make_py.run()
except KeyboardInterrupt: pass
except Exception:
    sys.stderr.write("{0!r}".format(sys.exc_info()))
    sys.exit(1)
#
