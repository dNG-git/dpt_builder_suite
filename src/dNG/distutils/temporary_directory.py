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

try: from tempfile import TemporaryDirectory
except ImportError:
    from shutil import rmtree
    from tempfile import mkdtemp

    class TemporaryDirectory(object):
        """
python.org: Create and return a temporary directory.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   builderSuite
:since:     v0.1.1
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
        """

        def __init__(self, suffix = "", prefix = "tmp", dir = None):
            """
Constructor __init__(TemporaryDirectory)

:since: v0.1.1
            """

            self.dir = dir
            self.name = None
            self.prefix = prefix
            self.suffix = suffix
        #

        def __enter__(self):
            """
python.org: Enter the runtime context related to this object.

:since: v0.1.1
            """

            self.name = mkdtemp(self.suffix, self.prefix, self.dir)
            return self.name
        #

        def __exit__(self, exc, value, tb):
            """
python.org: Exit the runtime context related to this object.

:since: v0.1.1
            """

            self.cleanup()
        #

        def cleanup(self, _warn = False):
            """
python.org: The directory can be explicitly cleaned up by calling the cleanup() method.

:since: v0.1.1
            """

            rmtree(self.name)
        #
    #
#
