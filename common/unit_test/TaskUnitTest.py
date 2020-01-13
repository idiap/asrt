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

import os
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest

from asrt.common.tasks.AsrtTask import Task, TaskInfo, TaskException
from asrt.common.MyFile import MyFile
from asrt.config.AsrtConfig import TEMPDIRUNITTEST

class TestTaskInfo(unittest.TestCase):
	def testTaskException(self):
		taskException = TaskException("Message")
		self.assertEqual("Message", taskException.msg)
		self.assertEqual("Message", str(taskException))		

	def testTaskInfo(self):
		taskInfo = TaskInfo("param1=1;param2=2", "","")

		self.assertEqual("param1=1;param2=2", taskInfo.parametersString)		
		self.assertTrue("" != taskInfo.workingDirectory)
		self.assertTrue("" != taskInfo.targetDirectory)

	def testGetParametersDict(self):
		taskInfo = TaskInfo("param1=1;param2=2", "","")
		paramDict = taskInfo.getParametersDict()

		self.assertTrue('param1' in paramDict)
		self.assertTrue('param2' in paramDict)

		taskInfo = TaskInfo("", "","")
		paramDict = taskInfo.getParametersDict()
		self.assertEqual(0,len(paramDict))

		taskInfo = TaskInfo("param1", "","")
		
		with self.assertRaises(Exception):
			taskInfo.getParametersDict()

class TestTask(unittest.TestCase):
	workingDirectory = TEMPDIRUNITTEST
	targetDirectory = scriptsDir + "/resources"
	targetFolder1 = targetDirectory + "/target-folder-1"
	targetFolderErr = targetDirectory + "/target-folder-err"
	targetFolderErr1 = targetDirectory + "/target-folder-err-1"
	targetFolderErr2 = targetDirectory + "/target-folder-err-2"
	dataList = "resources/target-folder/data.ilist"

	def setUp(self):
		print("")

	############
	#Tests
	#
	def testBuildTask(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))
		
		self.assertTrue(task1.taskUniqueId > 0)

	def testBuildTaskPath(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))
		
		with self.assertRaises(Exception):
			task1._buildTaskPath("path")

	def testSetResults(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))
		

		task1.setResult("error", "message")
		self.assertEqual("error", task1.resultErrorFlag)
		self.assertEqual("message", task1.resultMessage)

	def testGatherInputData(self):
		#No data olist
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolderErr1))

		with self.assertRaises(Exception):
			task1.gatherInputData()

		#No map .omap
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolderErr2))

		with self.assertRaises(Exception):
			task1.gatherInputData()

		
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))

		task1.gatherInputData()

		self.assertTrue(MyFile.checkFileExists(task1.getTaskDirectory()))
		self.assertTrue(MyFile.checkFileExists(task1.getInputDirectory()))
		self.assertTrue(MyFile.checkFileExists(task1.getTempDirectory()))
		self.assertTrue(MyFile.checkFileExists(task1.getOutputDirectory()))

		dataListPath = "%s%s%s" % (task1.getInputDirectory(),os.sep,'data.ilist')
		dataMap1Path = "%s%s%s" % (task1.getInputDirectory(),os.sep,'audio.imap')
		dataMap2Path = "%s%s%s" % (task1.getInputDirectory(),os.sep,'model.imap')

		self.assertTrue(MyFile.checkFileExists(dataListPath))
		self.assertTrue(MyFile.checkFileExists(dataMap1Path))
		self.assertTrue(MyFile.checkFileExists(dataMap2Path))

		self.assertEqual(15,task1.inputList.getCount())
		self.assertEqual(2,len(task1.mapLists))

		for dataMap in task1.mapLists:
			self.assertTrue(dataMap.getCount() in [2,1])

		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolderErr))

		#Two input lists
		with self.assertRaises(Exception):
			task1.gatherInputData()

	
	def testBuildParametersDict(self):
		task1 = Task(TaskInfo("param1=v1;param2=v2",
			                   TestTask.workingDirectory,
			                   TestTask.targetFolder1))

		task1._buildParametersDictionary()

		task1 = Task(TaskInfo("param1=;param2=v2",
			                   TestTask.workingDirectory,
			                   TestTask.targetFolder1))

		with self.assertRaises(Exception):
			task1._buildParametersDictionary()

		task1 = Task(TaskInfo("=v1;param2=v2",
			                   TestTask.workingDirectory,
			                   TestTask.targetFolder1))

		with self.assertRaises(Exception):
			task1._buildParametersDictionary()

	def testGetParametersDict(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))

		paramDict = task1.getTaskInfo().getParametersDict()

		self.assertEqual(0, len(paramDict))

	def testExecute(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))

		task1.validateParameters = lambda : Task.validateParameters(task1,[])

		task1.execute()

	def testValidateParameters(self):
		task1 = Task(TaskInfo("",TestTask.workingDirectory,
			                     TestTask.targetFolder1))

		with self.assertRaises(Exception):
			task1.validateParameters(["param1"])

		Task.COMMON_PARAMETERS = ["param1"]

		with self.assertRaises(Exception):
			task1.validateParameters([])

		Task.COMMON_PARAMETERS = []
