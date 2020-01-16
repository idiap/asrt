#!/usr/bin/env python2
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
__date__ = "Date: 2016/12"
__copyright__ = "Copyright (c) 2016 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import sys, unittest

thisMod = sys.modules[__name__]

import asrt.common.AsrtUtility as AsrtUtility
from asrt.common.english.unit_test.FormulaNumberUnitTest import FormulaNumberUnitTest

def getSuite(strName = None):
    """Get all available suite for the English package.
    """
    formulaNumberSuite = unittest.TestLoader().loadTestsFromTestCase(FormulaNumberUnitTest)

    testSuiteMap = {'numberFormulaEnglish' : formulaNumberSuite}

    if strName == None:
        return ", ".join(sorted(testSuiteMap.keys()))

    #All unit tests
    if strName == 'all':
        return [formulaNumberSuite]

    if strName not in testSuiteMap:
        return []

    return testSuiteMap[strName]


def getEnglishTestSuite(unitTestList):
    """Build the test suite for the English package.
    """
    return AsrtUtility.getTestSuite(thisMod.getSuite, unitTestList)
