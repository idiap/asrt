#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of asrt.

# asrt is free software: you can redistribute it and/or modify
# it under the terms of the BSD 3-Clause License as published by
# the Open Source Initiative.

# asrt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# BSD 3-Clause License for more details.

# You should have received a copy of the BSD 3-Clause License
# along with asrt. If not, see <http://opensource.org/licenses/>.

__author__ = "Alexandre Nanchen"
__version__ = "Revision: 1.0"
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys, traceback
import unittest

##############
#Debug
#
def getErrorMessage(e, prefix):
    """Get full error message with stack trace.
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    stackMessage = "\n------------ Begin stack ------------\n" + \
                   traceback.format_exc().rstrip() + "\n" + \
                   "------------ End stack --------------"
    strError = "%s: %s (line: %d), %s\n%s" % \
        (prefix, fname, exc_tb.tb_lineno,str(e),stackMessage)

    return strError

##############
#Test
#
def getTestSuite(pGetSuite, unitTestList):
    """Given a list of test, return the
       corresponding test suite.
    """
    suiteList = None

    if unitTestList[0] == 'all':
        suiteList = pGetSuite('all')
    else:
        #Specific unit tests
        if unitTestList[0] != 'all':
            suiteList = []
            for m in unitTestList:
                suiteList.extend(pGetSuite(m))

    # No test suites found
    if len(suiteList) == 0:
        return None

    return unittest.TestSuite(suiteList)
