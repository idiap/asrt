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
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../")
sys.path.append(scriptsDir + "/../../config")

import logging
import traceback

from ioread import Ioread
from TextDocument import TextDocument
from config import FRENCH_PICKLE_FOLDER
from ClassifierWord import WordClassifier
from config import SUBSTITUTION_TYPE, VALIDATION_TYPE
from config import FRENCH_LABEL, GERMAN_LABEL, ENGLISH_LABEL
from config import ITALIAN_LABEL, UNKNOWN_LABEL

class DataPreparationAPI():
    """Import sentences from one file, classifying
       sentences into languages.
    """
    logger                  = logging.getLogger("Asrt.DataPreparationAPI")

    def __init__(self, inputFile, outputDir):
        """Default constructor.
        """
        self.inputFile = inputFile
        self.outputDir = outputDir
        self.tempDir = outputDir
        self.debug = False
        self.regexFile = None
        self.lmModeling = False
        self.removePunctuation = False
        self.verbalizePunctuation = False
        self.doc = None
        self.wordClassifier = None
        self.substitutionPatternList = []
        self.validationPatternList = []

    #####################
    #Getters and setters
    #
    def setInputFile(self, inputFile):
        self.inputFile = inputFile

    def setOutputDir(self, outputDir):
        self.outputDir = outputDir

    def setTempDir(self, tempDir):
        self.tempDir = tempDir

    def setDebugMode(self, debug):
        self.debug = debug

    def setRegexFile(self, regexFile):
        self.regexFile = regexFile

    def setLMModeling(self, modelNgram):
        self.lmModeling = modelNgram

    def setRemovePunctuation(self, removePunctuation):
        self.removePunctuation = removePunctuation

    def setVerbalizePunctuation(self, verbalizePunctuation):
        self.verbalizePunctuation = verbalizePunctuation

    def getDocument(self):
        """Get the underlying 'TextDocument'.
        """
        return self.doc

    #####################
    #Public interface
    #
    def trainClassifier(self):
        """Train the underlying classifier.
        """
        if self.wordClassifier == None:
            self.logger.info("Prepare the word classifier ...")
            self.wordClassifier = WordClassifier()
            self.wordClassifier.train()

    def prepareDocument(self, language = 0):
        """Segment the document into sentences and prepare them.

           param language:
                - unknown : 0
                - french  : 1
                - german  : 2
                - english : 3
                - italian : 4
        """
        if language> 4 or language < 0:
            raise Exception("Unknown language")

        self.logger.info("Getting regexes")
        substitutionPatternsString, validationPatternsString = self._getRegexes()

        if len(substitutionPatternsString) > 0:
            self.logger.info("Using following regexes substitution:\n" +\
                    str(substitutionPatternsString[0:3]))

        if len(validationPatternsString) > 0:
            self.logger.info("Using following regexes for replacement:\n" +\
                    str(validationPatternsString[0:3]))

        try:
            self.logger.info("Document file: %s" % self.inputFile)

            #The main document
            self.doc = TextDocument(self.inputFile, FRENCH_PICKLE_FOLDER,
                                    substitutionPatternsString,
                                    validationPatternsString,
                                    self.outputDir)

            self.logger.info("Load file, convert to text when pdf document")

            self.doc.loadDocumentAsSentences(self.tempDir)

            self.logger.info("Cleaning and normalizing data ...")
            self.doc.cleanTextSentences()
            self.doc.normalizeTextSentences()

            self.logger.info("Filtering data ...")
            self.doc.filterTextSentences()

            #Do that before classifying
            if self.removePunctuation:
                self.doc.removeTextPunctuation()

            if language == 0:
                self.logger.info("Classifying sentences ...")
                self.doc.setClassifier(self.wordClassifier)
                self.doc.classifySentences()
            else:
                self.doc.setSentencesLanguage(language)

            if not self.removePunctuation and \
                self.verbalizePunctuation:
                self.doc.verbalizeTextPunctuation()

        except Exception, e:
            errorMessage = "An error as occurred when importing sentences: %s\n%s" % (str(e), self.inputFile)
            errorMessage += "\n" + \
                "------------ Begin stack ------------\n" + \
                traceback.format_exc().rstrip() + "\n" + \
                "------------ End stack --------------"
            self.logger.info(logging.WARNING, errorMessage)

            raise Exception(errorMessage)

        return self.doc

    def outputSentencesToFiles(self, outputDir):
        """Output the original sentences with language
           information to the 'outputFile'
        """
        self.logger.info("Output results to language files.")

        sentencesDict = {FRENCH_LABEL:[], GERMAN_LABEL:[],
                         ITALIAN_LABEL:[], ENGLISH_LABEL:[],
                         UNKNOWN_LABEL:[]}

        self.appendDocumentSentences(self.doc, sentencesDict)
        self.outputPerLanguage(sentencesDict, outputDir)

    @staticmethod
    def appendDocumentSentences(textDocument, sentencesDict):
        """Update 'sentencesDict' with the 'textDocument'
           content.
        """
        #Save all sentences
        for textCluster in textDocument.getListContent():
             strSentence = textCluster.getTextSentence()
             currentLanguage = UNKNOWN_LABEL

             if textCluster.isFrench():
                 currentLanguage = FRENCH_LABEL
             elif textCluster.isGerman():
                 currentLanguage = GERMAN_LABEL
             elif textCluster.isItalian():
                 currentLanguage = ITALIAN_LABEL
             elif textCluster.isEnglish():
                 currentLanguage = ENGLISH_LABEL

             #strOut = u"<" + textDocument.sourceFileName + u">: " + strSentence
             strOut = strSentence.rstrip()
             sentencesDict[currentLanguage].append(strOut)

    @staticmethod
    def outputPerLanguage(sentencesDict, outputDir):
        """Output sentences in language files.
        """
        io = Ioread()
        #Finally output to disk
        for resultLanguage, results in sentencesDict.items():
            if len(results) > 0:
                DataPreparationAPI.logger.info("%d sentences found for: %s" % (len(results), resultLanguage))
                strContent = "\n".join(results)
                strContent = strContent.rstrip() + "\n"
                outputPath = "%s/sentences_%s.txt" % (outputDir,\
                                                      resultLanguage)
                DataPreparationAPI.logger.info("Writing content to: %s" % outputPath)
                io.writeFileContent(outputPath,strContent)
            else:
                DataPreparationAPI.logger.info("No sentences found for: %s" % resultLanguage)

    #####################
    #Implementation
    #
    def _getRegexes(self):
        """Fetch from database validation and substitution
           regexes.
        """
        if len(self.substitutionPatternList) > 0 or \
           len(self.validationPatternList) > 0:
           return self.substitutionPatternList, self.validationPatternList

        if self.regexFile != None:
            io = Ioread()
            regexList = io.readCSV(self.regexFile,'\t','"')

            #Skip header
            for row in regexList[1:]:
                if int(row[4]) == SUBSTITUTION_TYPE:
                    self.substitutionPatternList.append((row[1],row[2]))
                elif int(row[4]) == VALIDATION_TYPE:
                    self.validationPatternList.append(row[1])
                else:
                    raise Exception("Unknown regular expression type!")

        return self.substitutionPatternList, self.validationPatternList
