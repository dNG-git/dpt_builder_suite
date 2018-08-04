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

from .builder_skel import BuilderSkel

class CopyBuilder(BuilderSkel):
    """
Provides a copying "make" environment object with support for custom headers
by extension.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v1.0.0
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def _parse_data(self, data, file_pathname, file_name):
        """
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:return: (str) Filtered data
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -CopyBuilder._parse_data()- (#echo(__LINE__)#)")

        ( _, file_ext ) = path.splitext(file_pathname)

        file_ext = file_ext[1:].lower()
        header_by_extension_list = self._get_variable("copy_builder_header_by_extension")

        if (type(header_by_extension_list) is dict
            and file_ext in header_by_extension_list
           ): data = "{0}\n{1}".format(header_by_extension_list[file_ext], data)

        return BuilderSkel._parse_data(self, data, file_pathname, file_name)
    #
#
