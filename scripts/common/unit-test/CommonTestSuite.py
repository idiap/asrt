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
__date__ = "Date: 2015/04"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import sys 
import os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../")

import unittest

from TaskUnitTest import TestTaskInfo, TestTask
from DataPreparationAPIUnitTest import TestDataPreparationAPI
from TextRepresentationUnitTest import TestTextRepresentation
from ListUnitTest import TestDataList, TestDataMap
from PunctuationUnitTest import PunctuationUnitTest

def getCommonTestSuite(unitTestList):
    """Build the test suite for the common package.
    """
    suiteList = None

    if unitTestList[0] == 'all':
        suiteList = getSuite('all')
    else:
        #Specific unit tests
        if unitTestList[0] != 'all':
            suiteList = []
            for m in unitTestList:
                suiteList.append(getSuite(m))

    allCommonSuites = unittest.TestSuite(suiteList)

    return allCommonSuites

def getSuite(strName = None):
    """Get all available suite for the common package.
    """
    taskInfoSuite = unittest.TestLoader().loadTestsFromTestCase(TestTaskInfo)
    taskSuite = unittest.TestLoader().loadTestsFromTestCase(TestTask)
    dataPreparationAPISuite = unittest.TestLoader().loadTestsFromTestCase(TestDataPreparationAPI)
    dataListSuite = unittest.TestLoader().loadTestsFromTestCase(TestDataList)
    dataMapSuite = unittest.TestLoader().loadTestsFromTestCase(TestDataMap)
    textRepresentationSuite = unittest.TestLoader().loadTestsFromTestCase(TestTextRepresentation)
    punctuationSuite = unittest.TestLoader().loadTestsFromTestCase(PunctuationUnitTest)
    
    testSuiteMap = {'taskInfo': taskInfoSuite, 'task': taskSuite, 'dataPreparationAPI': dataPreparationAPISuite, 
                    'dataList': dataListSuite, 'dataMap' : dataMapSuite, 
                    'textRepresentation' : textRepresentationSuite, 'punctuation': punctuationSuite}

    if strName == None:
        return ", ".join(sorted(testSuiteMap.keys()))

    #All unit tests
    if strName == 'all':
        return [taskInfoSuite, taskSuite, dataPreparationAPISuite, dataListSuite,
                dataMapSuite, textRepresentationSuite, punctuationSuite]

    if strName not in testSuiteMap:
        raise Exception("Unknown test %s" % strName)

    return testSuiteMap[strName]