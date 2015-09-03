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

import os, copy
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest
from DataList import DataList
from DataMap import DataMap
from config import TEMPDIRUNITTEST


class TestDataList(unittest.TestCase):
	IDATALIST = scriptsDir + "/resources/target-folder-1/data.ilist"
	ODATALIST = scriptsDir + "/resources/target-folder-1/data.olist"
	OUTPUTDIR = TEMPDIRUNITTEST + "/target-folder-1"
	
	def compareDict(self, dict1, dict2):
		for key,value in dict1.items():
			self.assertTrue(key in dict2)
			self.assertEqual(value, dict2[key])

	############
	#Tests
	#
	def testReadFile(self):
		dataList = DataList()
		dataList.readFile(TestDataList.IDATALIST)
		self.assertEqual(15, len(dataList.dataDictionary))

	def testGetPath(self):
		dataList = DataList()
		dataList.readFile(TestDataList.IDATALIST)

		self.assertEqual('/path/to/mlf1', dataList.getPath("mlf1"))

	def testWriteFile(self):
		dataList = DataList()
		dataList.readFile(TestDataList.IDATALIST)
		dataList.writeFile(TestDataList.ODATALIST)

		tempDataDict = copy.deepcopy(dataList.dataDictionary)
		dataList.readFile(TestDataList.ODATALIST)
		dataDict = dataList.dataDictionary

		self.compareDict(tempDataDict, dataDict)
		self.compareDict(dataDict,tempDataDict)


class TestDataMap(unittest.TestCase):
	IMAPLIST = scriptsDir + "/resources/target-folder-1/audio.imap"
	OMAPLIST = scriptsDir + "/resources/target-folder-1/audio.omap"
	OUTPUTDIR = TEMPDIRUNITTEST + "/target-folder-1"
	
	def compareDict(self, dict1, dict2):
		for key,value in dict1.items():
			self.assertTrue(key in dict2)
			self.assertEqual(value, dict2[key])

			for key1,value1 in value.items():
				self.assertTrue(key1 in dict2[key])
				self.assertEqual(value1, dict2[key][key1])

				for key2,value2 in value1.items():
					self.assertTrue(key2 in dict2[key][key1])
					self.assertEqual(value2, dict2[key][key1][key2])

	############
	#Tests
	#
	def testReadFile(self):
		dataMap = DataMap()
		dataMap.readFile(TestDataMap.IMAPLIST)
		
		self.assertEqual(2, len(dataMap.dataMap))
		self.assertEqual(2, len(dataMap.dataMap['audio1']))
		self.assertEqual(2, len(dataMap.dataMap['audio1']['segment1']))

	def testWriteFile(self):
		dataMap = DataMap()
		dataMap.readFile(TestDataMap.IMAPLIST)
		dataMap.writeFile(TestDataMap.OMAPLIST)

		tempDataMap = copy.deepcopy(dataMap.dataMap)

		dataMap.readFile(TestDataMap.OMAPLIST)

		dataMap = dataMap.dataMap

		self.compareDict(tempDataMap, dataMap)
		self.compareDict(dataMap, tempDataMap)
		
	def testSetDictionaryMapFromList(self):
		dataList = [['audio1', 'segment1', 'mlf1'],
				   ['audio1', 'segment1', 'mlf2'],
				   ['audio1', 'segment2', 'mlf3'],
				   ['audio1', 'segment2', 'mlf4'],
				   ['audio2', 'segment3', 'mlf5'],
				   ['audio2', 'segment3', 'mlf6'],
				   ['audio2', 'segment4', 'mlf8'],
				   ['audio2', 'segment4', 'mlf7']]

		dataMap = DataMap()
		dataMap.readFile(TestDataMap.IMAPLIST)
		tempDataMap = copy.deepcopy(dataMap.dataMap)

		dataMap.setDictionaryMapFromList(dataList)
		dataMap = dataMap.dataMap

		self.compareDict(tempDataMap, dataMap)
		self.compareDict(dataMap, tempDataMap)