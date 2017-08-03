# -*- coding: utf-8 -*-

"""
builderSuite
Build code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?py;builder_suite

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(builderSuiteVersion)#
#echo(__FILEPATH__)#
"""

from os import path

from dNG.distutils.js_builder import JsBuilder

class InstallJsData(object):
    """
This class provides the callback for JavaScript files.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.1
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    @staticmethod
    def callback(source_directory, target_path, target_parameters):
        """
Callback to be used in "dNG.distutils.InstallData".

:param source_directory: Source directory to work in
:param target_path: Target directory for build
:param target_parameters: Target parameters

:since: v0.1.1
        """

        js_builder = JsBuilder(target_parameters,
                               source_directory,
                               target_path,
                               "js",
                               default_chmod_files = "0644",
                               default_chmod_dirs = "0755"
                              )

        if (target_parameters.get("js_strip_source_directory", False)): js_builder.set_strip_prefix(source_directory + path.sep)

        js_builder.make_all()
    #
#
