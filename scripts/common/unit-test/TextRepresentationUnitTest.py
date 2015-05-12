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
__date__ = "Date: 2014/04"
__copyright__ = "Copyright (c) 2014 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import sys, os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../")
sys.path.append(scriptsDir + "/../../config")


import unittest
from MyFile import MyFile
from TextRepresentation import TextRepresentation
from config import TEMPDIRUNITTEST, LOGDIR


class TestTextRepresentation(unittest.TestCase):
	workingDirectory = TEMPDIRUNITTEST
	targetDirectory = scriptsDir + "/resources"
	pdfFile = targetDirectory + "/test.pdf"
	tmpPdfFile = targetDirectory + "/test.pdf.tmp"
	textFile = targetDirectory + "/punctuation.txt"
	tmpTextFile = targetDirectory + "/punctuation.txt.tmp"


	############
	#Tests
	#
	def testConvertToText(self):
		rep = TextRepresentation(TestTextRepresentation.pdfFile,
			                     TEMPDIRUNITTEST, LOGDIR)

		rep.convertToText()
		MyFile.checkFileExists(TestTextRepresentation.tmpPdfFile)

		rep = TextRepresentation(TestTextRepresentation.textFile,
			                     TEMPDIRUNITTEST, LOGDIR)

		rep.convertToText()
		MyFile.checkFileExists(TestTextRepresentation.tmpTextFile)		

	def testLoadTextFile(self):
		rep = TextRepresentation(TestTextRepresentation.textFile,
			                     TEMPDIRUNITTEST, LOGDIR)

		rep.convertToText()
		rep.loadTextFile()

		self.assertEqual(6, len(rep.sentencesList))