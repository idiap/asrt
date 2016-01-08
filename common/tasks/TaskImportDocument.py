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

import logging, shutil, os

from asrt.common.MyFile import MyFile
from asrt.common.tasks.AsrtTask import Task
from asrt.common.DataPreparationAPI import DataPreparationAPI
from asrt.common.AsrtUtility import getErrorMessage
from asrt.config.AsrtConfig import LANGUAGE2ID
from asrt.config.AsrtConfig import UNKNOWN_LABEL, FRENCH_LABEL, GERMAN_LABEL
from asrt.config.AsrtConfig import ENGLISH_LABEL, ITALIAN_LABEL

class ImportDocumentTask(Task):
    """Import sentences from a pdf files, classifying
       them into languages.
    """
    logger                  = logging.getLogger("task.ImportDocumentTask")

    PARAMREGEXFILE          = 'regexfile'
    PARAMDEBUG              = 'debug'
    TEXTFILTERING           = 'textFiltering'
    REMOVEPUNCTUATION       = 'removePunctuation'
    VERBALIZEPUNCTUATION    = 'verbalizePunctuation'
    SEGMENTWITHNLTK         = 'segmentWithNLTK'
    LMMODELING              = 'lmModeling'
    PARAMETERS              = [PARAMREGEXFILE,TEXTFILTERING,PARAMDEBUG,REMOVEPUNCTUATION,
                               VERBALIZEPUNCTUATION, SEGMENTWITHNLTK, LMMODELING]

    def __init__(self, taskInfo):
        """Default constructor.
        """
        Task.__init__(self, taskInfo)

        self.count = 0
        self.debug = False
        self.textFiltering = False
        self.removePunctuation = False
        self.verbalizePunctuation = False
        self.segmentWithNLTK = True
        self.lmModeling = False

    ############
    #Interface
    #
    def validateParameters(self):
        """Check that language and batch file
           parameters are specified.
        """

        self._log(logging.INFO, "Validate parameters")

        return Task.validateParameters(self,
                    ImportDocumentTask.PARAMETERS)

    def setParameters(self):
        """Set parameters from given values.
        """
        self.regexFile = self.taskParameters[ImportDocumentTask.PARAMREGEXFILE]
        self.debug = self.taskParameters[ImportDocumentTask.PARAMDEBUG] == "True"
        self.textFiltering = self.taskParameters[ImportDocumentTask.TEXTFILTERING] == "True"
        self.removePunctuation = self.taskParameters[ImportDocumentTask.REMOVEPUNCTUATION] == "True"
        self.verbalizePunctuation = self.taskParameters[ImportDocumentTask.VERBALIZEPUNCTUATION] == "True"
        self.segmentWithNLTK = self.taskParameters[ImportDocumentTask.SEGMENTWITHNLTK] == "True"
        self.lmModeling = self.taskParameters[ImportDocumentTask.LMMODELING] == "True"
        
        self._log(logging.INFO, "Debug is set to " + str(self.debug))

    def doWork(self):
        """The actual upload of sentences.
        """
        self._log(logging.INFO, "Do work!")

        if len(self.mapLists) > 1:
            self._log(logging.CRITICAL,"Only one map list accepted!")

        documentUrl = None

        try:
            #All pdf documents
            textDocumentsList = []
            dictMap = self.mapLists[0].getDictionaryMap()

            totalCount = len(dictMap.keys())
            count = 0

            self._log(logging.INFO, "Temp dir is: %s" % self.getTempDirectory())
            self._log(logging.INFO, "Output dir is: %s" % self.getOutputDirectory())
            self._log(logging.INFO, "%d files to process!" % totalCount)

            #Setup once for all documents
            api = DataPreparationAPI(None, self.getOutputDirectory())
            if self.regexFile != None and len(self.regexFile) > 0:
                api.setRegexFile(self.regexFile)

            api.setFilterSentences(self.textFiltering)
            api.setDebugMode(self.debug)
            api.setRemovePunctuation(self.removePunctuation)
            api.setVerbalizePunctuation(self.verbalizePunctuation)
            api.setSegmentWithNLTK(self.segmentWithNLTK)
            api.setLMModeling(self.lmModeling)
            api.trainClassifier()

            #Loop trough map file
            for documentName in dictMap.keys():
                for language in dictMap[documentName]:
                    documentUrl = self.inputList.getPath(documentName)

                    #Set the current document information
                    api.setInputFile(documentUrl)
                   
                    #Main processing
                    api.prepareDocument(LANGUAGE2ID[language])
                    textDocumentsList.append(api.getDocument())

                count += 1
                self._log(logging.INFO, "%d remaining files to process!" % (totalCount-count))

            self._log(logging.INFO, "Output results to language files.")
            self.outputSentencesToFiles(textDocumentsList)

            #Outcome of the work to be saved
            self.setResult(False, "Success importing sentences from %s" % self.mapLists[0].getDataMapFile())

        except Exception, e:
            errorMessage = "An error as occurred when importing sentences from %s" % documentUrl
            self._log(logging.CRITICAL, getErrorMessage(e, errorMessage))
            raise e

    def prepareOutputData(self):
        """Copy results, old lists and build new input
           and map lists.
        """
        self._log(logging.INFO, "Copy results files to output folder:%s" %
                        self.getOutputDirectory())

        #Data maps
        dataMapFiles = MyFile.dirContent(self.getTempDirectory(),
                                         "*sentences_*.txt")
        for sentenceFile in dataMapFiles:
            srcFile = self.getTempDirectory() + os.sep + sentenceFile
            shutil.copy(srcFile,self.getOutputDirectory())

    def outputSentencesToFiles(self, textDocumentsList):
        """Output the original sentences with language
           information to the database.
        """
        sentencesDict = {FRENCH_LABEL:[], GERMAN_LABEL:[],
                         ITALIAN_LABEL:[], ENGLISH_LABEL:[],
                         UNKNOWN_LABEL:[]}

        for textDocument in textDocumentsList:
            DataPreparationAPI.appendDocumentSentences(textDocument, sentencesDict)

        DataPreparationAPI.outputPerLanguage(sentencesDict, self.getTempDirectory())
        
