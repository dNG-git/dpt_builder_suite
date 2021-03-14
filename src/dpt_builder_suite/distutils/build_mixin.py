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

from os import path

class BuildMixin(object):
    """
This mixin is used to map Distutils methods with a build directory.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: builder_suite
:since:      v0.1.1
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = ( )
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _build_target_path = None
    """
Target directory for build
    """
    _build_target_parameters = { }
    """
Target parameters
    """

    @classmethod
    def set_build_target_path(cls, target_path):
        """
Sets the target directory used during build.

:param target_path: Target directory for build

:since: v0.1.1
        """

        cls._build_target_path = path.normpath(target_path)
    #

    @classmethod
    def set_build_target_parameters(cls, parameters):
        """
Sets the target parameters.

:param parameters: Target parameters

:since: v0.1.1
        """

        cls._build_target_parameters = parameters
    #
#
