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
__version__ = "Revision: 1.0 "
__date__ = "Date: 2020/01"
__copyright__ = "Copyright (c) 2020 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest
import logging

from asrt.common.ioread import Ioread


class TestIoread(unittest.TestCase):
    logger = logging.getLogger("Asrt.TestIoread")
    testFile = scriptsDir + "/resources/ioread_utf8.txt"
    testFileCSV = scriptsDir + "/resources/ioread_utf8.csv"

    testsString = [
        """Utf-8 test\nLatin characters é à ä\nNon latin characters 镕\n""",
        """Non latin characters 镕"""]

    testList = [['Utf-8 test', 'Latin characters é à ä',
                 'Non latin characters 镕']]

    def setUp(self):
        self.ioread = Ioread()

    ############
    # Tests
    #
    def testOpenFile(self):
        try:
            fd = self.ioread.openFile(self.testFile)
            self.ioread.closeFile(fd)
        except Exception:
            self.fail("testOpenFile raised ExceptionType unexpectedled")

    def testReadFileContent(self):
        strContent = self.ioread.readFileContent(self.testFile)
        self.assertEquals(self.testsString[0], strContent)

    def testReadFileContentList(self):
        strContentList = self.ioread.readFileContentList(self.testFile)
        self.assertEquals(3, len(strContentList))
        self.assertEquals(self.testsString[1], strContentList[2])

    def testReadCSV(self):
        strContentList = self.ioread.readCSV(self.testFileCSV)
        self.assertEquals(1, len(strContentList))
        self.assertEquals(strContentList, self.testList)

    def testWriteFileContent(self):
        strContent = self.testsString[0]
        self.ioread.writeFileContent("test.txt", strContent)

        readStrContent = self.ioread.readFileContent(self.testFile)
        self.assertEquals(strContent, readStrContent)
