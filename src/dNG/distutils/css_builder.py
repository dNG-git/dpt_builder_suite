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
from rcssmin import cssmin
from scss import config, Scss

from .builder_skel import BuilderSkel

class CssBuilder(BuilderSkel):
    """
Provides a (S)CSS "make" environment object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.1
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def _is_excluded_file(self, file_name):
        """
Returns true if the file should be excluded.

:param file_name: File name

:return: (bool) True if excluded
:since:  v0.1.0
        """

        return (file_name[0] == "_" or BuilderSkel._is_excluded_file(self, file_name))
    #

    def _parse_data(self, data, file_pathname, file_name):
        """
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:return: (str) Filtered data
:since:  v0.1.0
        """

        if (self.event_handler is not None): self.event_handler.debug("#echo(__FILEPATH__)# -CssBuilder._parse_data()- (#echo(__LINE__)#)")

        if (path.splitext(file_name)[-1].lower() == ".scss"):
            config.STATIC_URL = ""
            data = Scss().compile(data)
        #

        if (self._get_variable("css_min_filenames") is not None
            and file_name[-8:].lower() != ".min.css"
            and self._get_variable("debug") is None
           ): data = cssmin(data)

        if (self._get_variable("css_header") is not None): data = "/* {0} */\n{1}".format(self._get_variable("css_header"), data)
        return BuilderSkel._parse_data(self, data, file_pathname, file_name)
    #

    def _write_file(self, file_content, file_pathname, file_mode = "w+b"):
        """
Write the given file to the defined location. Create subdirectories if
needed.

:param file_content: Parsed content
:param file_pathname: Path to the output file
:param file_mode: Filemode to use

:return: (bool) True on success
:since:  v0.1.0
        """

        if (file_pathname[-8:].lower() != ".min.css"):
            ( file_pathname_no_ext, file_ext ) = path.splitext(file_pathname)

            if (file_ext.lower() == ".scss"):
                file_ext = ".css"
                file_pathname = file_pathname_no_ext + file_ext
            #

            if (self._get_variable("css_min_filenames") is not None
                and self._get_variable("debug") is None
                and len(file_ext) > 0
               ): file_pathname = "{0}.min{1}".format(file_pathname_no_ext, file_ext)
        #

        return BuilderSkel._write_file(self, file_content, file_pathname, file_mode)
    #
#
