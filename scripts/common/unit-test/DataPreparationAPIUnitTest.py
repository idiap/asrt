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
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import sys, os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../")
sys.path.append(scriptsDir + "/../../config")

import unittest

from DataPreparationAPI import DataPreparationAPI
from config import TEMPDIRUNITTEST

class TestDataPreparationAPI(unittest.TestCase):
	workingDirectory = TEMPDIRUNITTEST 
	targetDir = scriptsDir + "/resources"
	targetFolder1 = targetDir + "/target-folder-2"
	regexFile = targetDir + "/regexpattern.csv"

	def setUp(self):
		print ""

	############
	#Tests
	#
	def testLoadRegexes(self):
		api = DataPreparationAPI(None,None)
		api.setRegexFile(self.regexFile)

		substitutionPatternsList, validationPatternsList = api._getRegexes()

		self.assertTrue(len(substitutionPatternsList) > 0)
		self.assertTrue(len(validationPatternsList) > 0)
		self.assertTrue(len(substitutionPatternsList[0]) > 1)
