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
__date__ = "Date: 2012/05"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../")
sys.path.append(scriptsDir + "/../../config")

import logging, shutil
import traceback

from ioread import Ioread
from MyFile import MyFile
from TextDocument import TextDocument
from tasks.Task import Task
from config import FRENCH_PICKLE_FOLDER
from ClassifierWord import WordClassifier

class ImportDocumentTask(Task):
	"""Import sentences from a pdf files, classifying
	   them into languages.

	   Process parameters are:
		   - pdf file url
	"""
	logger                  = logging.getLogger("task.ImportDocumentTask")

	PARAMREGEXFILE			= 'regexfile'
	PARAMDEBUG				= 'debug'
	REMOVEPUNCTUATION		= 'removePunctuation'
	VERBALIZEPUNCTUATION	= 'verbalizePunctuation'
	PARAMETERS              = [PARAMREGEXFILE,PARAMDEBUG,REMOVEPUNCTUATION,VERBALIZEPUNCTUATION]

	REGEXFILE               = ''

	#Pattern types
	SUBSTITUTION_TYPE       = 1
	VALIDATION_TYPE         = 2

	#Language
	FRENCH                  = 'french'
	GERMAN                  = 'german'
	ITALIAN					= 'italian'
	ENGLISH					= 'english'
	UNKNOWN                 = 'unknown'

	LANGUAGETOID			= {FRENCH:1,GERMAN:2,ITALIAN:3,ENGLISH:4,UNKNOWN:5}


	def __init__(self, taskInfo):
		"""Default constructor."""

		Task.__init__(self, taskInfo)

		self.ioread = Ioread()
		self.count = 0
		self.document = None
		self.regexFile = None
		self.debug = False
		self.removePunctuation = False
		self.verbalizePunctuation = False

	#######################################
	#Interface
	#
	def validateParameters(self):
		"""Check that language and batch file
		   parameters are specified."""

		self._log(logging.INFO, "Validate parameters")

		return Task.validateParameters(self,
						ImportDocumentTask.PARAMETERS)

	def setParameters(self):
		"""Set parameters from given values.
		"""
		self.regexFile = self.taskParameters[ImportDocumentTask.PARAMREGEXFILE]
		self.debug = self.taskParameters[ImportDocumentTask.PARAMDEBUG] == "True"
		self.removePunctuation = self.taskParameters[ImportDocumentTask.REMOVEPUNCTUATION] == "True"
		self.verbalizePunctuation = self.taskParameters[ImportDocumentTask.VERBALIZEPUNCTUATION] == "True"
		
		self._log(logging.INFO, "Debug is set to " + str(self.debug))

	def doWork(self):
		"""The actual upload of sentences."""

		self._log(logging.INFO, "Do work!")

		if len(self.mapLists) > 1:
			self._log(logging.CRITICAL,"Only one map list accepted!")

		try:
			self._log(logging.INFO, "Getting regexes ...")
			substitutionPatternsString, validationPatternsString = self._getRegexes()

			self._log(logging.INFO, "Using following regexes:\nSubstitution: " +\
						str(substitutionPatternsString[0:3]) + " ...\nValidation: " +\
						str(validationPatternsString[0:3])+ " ...")

			self._log(logging.INFO, "Prepare the word classifier ...")

			#Train classifiero only once
			wordClassifier = WordClassifier()
			wordClassifier.train()

			#All pdf documents
			textDocumentsList = []
			dictMap = self.mapLists[0].getDictionaryMap()

			totalCount = len(dictMap.keys())
			count = 0

			self._log(logging.INFO, "%d files to process!" % totalCount)

			#Loop trough map file
			for documentName in dictMap.keys():
				for language in dictMap[documentName]:

					documentUrl = self.inputList.getPath(documentName)
					self._log(logging.INFO, "Document file: %s" % documentUrl)

					try:
						#The main document
						doc = TextDocument(documentUrl, FRENCH_PICKLE_FOLDER,
											  substitutionPatternsString,
											  validationPatternsString,
											  self.getLogDirectory())

						#Which classifier to use
						doc.setClassifier(wordClassifier)

						self._log(logging.INFO, "Load document, convert to text when pdf %s" %
								  self.getTempDirectory())

						doc.loadDocumentAsSentences(self.getTempDirectory())

						self._log(logging.INFO, "Preparing data ...")
						doc.prepareTextSentences(self.removePunctuation)
						
						self._log(logging.INFO, "Filtering data ...")
						doc.filterTextSentences()

						if language == ImportDocumentTask.UNKNOWN:
							self._log(logging.INFO, "Classifying sentences ...")
							doc.classifySentences()
						else:
							self._log(logging.INFO, "Setting language %s for document %s" % (language,documentName))
							doc.setSentencesLanguage(ImportDocumentTask.LANGUAGETOID[language])

						if self.verbalizePunctuation:
							doc.verbalizePunctuation()

						#Only append after success
						textDocumentsList.append(doc)

					except Exception, e:
						errorMessage = "An error as occurred when importing sentences: %s\n%s" % (str(e), documentUrl)
						errorMessage += "\n" + \
							"------------ Begin stack ------------\n" + \
							traceback.format_exc().rstrip() + "\n" + \
							"------------ End stack --------------"
						self._log(logging.WARNING, errorMessage)

				count += 1
				self._log(logging.INFO, "%d remaining files to process!" % (totalCount-count))

			self._log(logging.INFO, "Output results to language files.")
			self._outputSentencesToFile(textDocumentsList)

			#Outcome of the work to be saved
			self.setResult(False, "Success importing sentences from %s" % self.mapLists[0].getDataMapFile())

		except Exception, e:

			errorMessage = "An error as occurred when importing sentences: " + str(e)
			errorMessage += "\n" + \
							"------------ Begin stack ------------\n" + \
							traceback.format_exc().rstrip() + "\n" + \
							"------------ End stack --------------"
			self._log(logging.CRITICAL, errorMessage)
			self.setResult(True, errorMessage)

			raise e

	def prepareOutputData(self):
		"""Copy results, old lists and build new
		   input and map lists.
		"""
		self._log(logging.INFO, "Copy results files to ouptut folder")

		#Data maps
		dataMapFiles = MyFile.dirContent(self.getTempDirectory(),
										 "*sentences_*.txt")

		for sentenceFile in dataMapFiles:
			srcFile = self.getTempDirectory() + os.sep + sentenceFile
			shutil.copy(srcFile,self.getOutputDirectory())


	#######################################
	#Implementation
	#
	def _getRegexes(self):
		"""Fetch from database validation and substitution
		   regexes.
		"""
		substitutionPatternList, validationPatternList = [], []

		io = Ioread()
		regexList = io.readCSV(self.regexFile,'\t','"')

		#Skip header
		for row in regexList[1:]:
			if int(row[4]) == ImportDocumentTask.SUBSTITUTION_TYPE:
				substitutionPatternList.append((row[1],row[2]))
			elif int(row[4]) == ImportDocumentTask.VALIDATION_TYPE:
				validationPatternList.append(row[1])
			else:
				raise Exception("Unknown regular expression type!")

		return substitutionPatternList, validationPatternList

	def _outputSentencesToFile(self, textDocumentsList):
		"""Output the original sentences with language
		   information to the database.
		"""
		sentencesDict = {ImportDocumentTask.FRENCH:[],
						 ImportDocumentTask.GERMAN:[],
						 ImportDocumentTask.ITALIAN:[],
						 ImportDocumentTask.ENGLISH:[],
						 ImportDocumentTask.UNKNOWN:[]}

		for textDocument in textDocumentsList:
			self._appendDocumentSentences(textDocument, sentencesDict)

		#Finally output to disk
		io = Ioread()

		for resultLanguage, results in sentencesDict.items():
			if len(results) > 0:
				self._log(logging.INFO, "%d sentences found for: %s" % (len(results), resultLanguage))
				strContent = "\n".join(results)
				strContent = strContent.rstrip() + "\n"
				outputPath = "%s/sentences_%s.txt" % (self.getTempDirectory(),\
													  resultLanguage)
				self._log(logging.INFO, "Writing content to: %s" % outputPath)
				io.writeFileContent(outputPath,strContent)
			else:
				self._log(logging.INFO, "No sentences found for: %s" % resultLanguage)

	def _appendDocumentSentences(self, textDocument, sentencesDict):
		"""Update 'sentencesDict' with the 'textDocument'
		   content.
		"""
		#Save all sentences
		for textCluster in textDocument.getListContent():
			 strSentence = textCluster.getTextSentence(self.debug)
			 currentLanguage = ImportDocumentTask.UNKNOWN

			 if textCluster.isFrench():
				 currentLanguage = ImportDocumentTask.FRENCH
			 elif textCluster.isGerman():
				 currentLanguage = ImportDocumentTask.GERMAN
			 elif textCluster.isItalian():
				 currentLanguage = ImportDocumentTask.ITALIAN
			 elif textCluster.isEnglish():
				 currentLanguage = ImportDocumentTask.ENGLISH

			 #strOut = u"<" + textDocument.sourceFileName + u">: " + strSentence
			 strOut = strSentence.rstrip()
			 sentencesDict[currentLanguage].append(strOut)