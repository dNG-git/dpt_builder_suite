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

import re

from .builder_skel import BuilderSkel

class PyBuilder(BuilderSkel):
    """
Provides a Python "make" environment object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.1
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def __init__(self, parameters, include, output_path, filetype, default_umask = None, default_chmod_files = None, default_chmod_dirs = None, timeout_retries = 5, event_handler = None):
        """
Constructor __init__(PyBuilder)

:param parameters: DEFINE statements
:param include: String (delimiter is ",") with directory or file names to
                be included.
:param output_path: Output path
:param filetype: String (delimiter is ",") with extensions of files to be
                 parsed.
:param default_umask umask: to set before creating new directories or files
:param default_chmod_files: chmod to set when creating a new file
:param default_chmod_dirs: chmod to set when creating a new directory
:param timeout_retries: Retries before timing out
:param event_handler: EventHandler to use

:since: v0.1.1
        """

        BuilderSkel.__init__(self,
                             parameters,
                             include,
                             output_path,
                             filetype,
                             default_umask,
                             default_chmod_files,
                             default_chmod_dirs,
                             timeout_retries,
                             event_handler
                            )

        self.dir_exclude_list = [ "__pycache__" ]
    #

    def _change_match(self, tag_definition, data, tag_position, data_position, tag_end_position):
        """
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.1
        """

        if (self.event_handler is not None): self.event_handler.debug("#echo(__FILEPATH__)# -PyBuilder._change_match({0:d}, {1:d}, {2:d})- (#echo(__LINE__)#)".format(tag_position, data_position, tag_end_position))
        _return = data[:tag_position]

        data_closed = data[self._find_tag_end_position(data, tag_end_position, '"""'):]

        if (tag_definition[0] == '"""#ifdef'):
            variable = re.match('^"""#ifdef\\((\\w+)\\)', data[tag_position:data_position]).group(1)
            tag_end = data[tag_end_position:self._find_tag_end_position(data, tag_end_position, '"""')]

            if (self._get_variable(variable) is not None):
                if (data[data_position:data_position + 1] == "\n"):
                    _return += data[data_position + 1:tag_end_position].replace('"\\"', '"""')
                else: _return += data[data_position:tag_end_position].replace('"\\"', '"""')
            #

            if (tag_end == '#\\n"""' or tag_end == ':#\\n"""'): data_closed = re.sub("^\n", "", data_closed)
        elif (tag_definition[0] == '"""#ifndef'):
            variable = re.match('^"""#ifndef\\((\\w+)\\)', data[tag_position:data_position]).group(1)
            tag_end = data[tag_end_position:self._find_tag_end_position(data, tag_end_position, '"""')]

            if (self._get_variable(variable) is None):
                if (data[data_position:data_position + 1] == "\n"):
                    _return += data[data_position + 1:tag_end_position].replace('"\\"', '"""')
                else: _return += data[data_position:tag_end_position].replace('"\\"', '"""')
            #

            if (tag_end == '#\\n"""' or tag_end == ':#\\n"""'): data_closed = re.sub("^\n", "", data_closed)
        #

        _return += data_closed

        return _return
    #

    def _check_match(self, data):
        """
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (tuple) Matched tag definition; None if false positive
:since:  v0.1.1
        """

        if (self.event_handler is not None): self.event_handler.debug("#echo(__FILEPATH__)# -PyBuilder._check_match()- (#echo(__LINE__)#)")
        _return = None

        if (data[:9] == '"""#ifdef'):
            re_result = re.match('^"""#ifdef\\((\\w+)\\) """\n', data)

            if (re_result is None):
                re_result = re.match('^"""#ifdef\\((\\w+)\\):\n', data)

                if (re_result is None): _return = None
                else: _return = ( '"""#ifdef', ":", ( ':#\\n"""', ':#"""' ) )
            else: _return = ( '"""#ifdef', '"""', ( '#\\n"""', '#"""' ) )
        elif (data[:10] == '"""#ifndef'):
            re_result = re.match('^"""#ifndef\\((\\w+)\\) """\n', data)

            if (re_result is None):
                re_result = re.match('^"""#ifndef\\((\\w+)\\):\n', data)

                if (re_result is None): _return = None
                else: _return = ( '"""#ifndef', ":", ( ':#\\n"""', ':#"""' ) )
            else: _return = ( '"""#ifndef', '"""', ( '#\\n"""', '#"""' ) )
        #

        return _return
    #

    def _parse_data(self, data, file_pathname, file_name):
        """
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:return: (str) Filtered data
:since:  v0.1.1
        """

        if (self.event_handler is not None): self.event_handler.debug("#echo(__FILEPATH__)# -PyBuilder._parse_data()- (#echo(__LINE__)#)")
        data = self._parse('"""#', BuilderSkel._parse_data(self, data, file_pathname, file_name))

        if (self._get_variable("dev_comments") is None): return self._remove_data_dev_comments(data)
        else: return data
    #

    def _remove_data_dev_comments(self, data):
        """
Remove all development comments from the content.

:param data: Data to be parsed

:return: (str) Filtered data
:since:  v0.1.1
        """

        if (self.event_handler is not None): self.event_handler.debug("#echo(__FILEPATH__)# -PyBuilder._remove_data_dev_comments()- (#echo(__LINE__)#)")
        return re.sub('(\n[ \t]*"""\n---.+?---\n[ \t]*"""\n)|("""\\w//.+?//\\w"""\n)', "", data, flags = re.S)
    #
#
