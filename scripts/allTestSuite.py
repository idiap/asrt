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
__date__ = "Date: 2015/04"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys
import unittest

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/common")
sys.path.append(scriptsDir + "/common/unit-test")
sys.path.append(scriptsDir + "/config")

from CommonTestSuite import getSuite, getCommonTestSuite
from MyFile import MyFile
from config import TEMPDIRUNITTEST

usage = """ 
    Run specific unit tests or all.

    Available unit tests are: %s
""" % getSuite()

def asrtTestSuite(unitTestList = None):
    """Build test suite for all test suites in the script folder
    """
    commonTestSuite = getCommonTestSuite(unitTestList)
    allTests = unittest.TestSuite([commonTestSuite])

    return allTests

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print usage
        print "    usage: %s 'unit test name 1 or all' 'unit test name 2' " % sys.argv[0]
        print ""
        sys.exit(0)

    MyFile.checkDirExists(TEMPDIRUNITTEST)

    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(asrtTestSuite(sys.argv[1:]))
