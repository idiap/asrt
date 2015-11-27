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

import logging

from asrt.common.ioread import Ioread
from asrt.common.TextDocument import TextDocument
from asrt.common.ClassifierWord import WordClassifier
from asrt.common.RegularExpressionList import RegexList
from asrt.common.formula.FormulaRegularExpression import RegularExpressionFormula
from asrt.common.AsrtUtility import getErrorMessage
from asrt.config.AsrtConfig import VALIDATION_TYPE
from asrt.config.AsrtConfig import FRENCH_LABEL, GERMAN_LABEL, ENGLISH_LABEL
from asrt.config.AsrtConfig import ITALIAN_LABEL, UNKNOWN_LABEL

class DataPreparationAPI():
    """Import sentences from one file, classifying
       sentences into languages.
    """
    logger  = logging.getLogger("Asrt.DataPreparationAPI")

    def __init__(self, inputFile, outputDir):
        """Default constructor.
        """
        self.inputFile = inputFile
        self.outputDir = outputDir
        self.tempDir = outputDir
        self.formattedText = None
        self.debug = False
        self.regexFile = None
        self.lmModeling = False
        self.filterSentences = False
        self.removePunctuation = False
        self.verbalizePunctuation = False
        self.doc = None
        self.wordClassifier = None
        self.substitutionRegexFormula = RegularExpressionFormula(None)
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

    def setFormattedText(self, formattedText):
        self.formattedText = formattedText

    def getCleanedText(self):
        if self.doc != None:
            return self.doc.getCleanedText()
        return ""

    def getCleanedTextPerLanguage(self):
        if self.doc != None:
            return self.doc.getCleanedTextPerLanguage()
        return ""

    def setDebugMode(self, debug):
        self.debug = debug

    def setRegexFile(self, regexFile):
        self.regexFile = regexFile

    def setRegexList(self, regexList):
        """Set both validation and substitution user regexes.

           param regexList: a list of the following form:

           ['matching pattern', 'substitution', 'type', 'language id']
        """
        #Reset current lists
        self.substitutionRegexFormula = RegularExpressionFormula(None)
        self.validationPatternList = []

        substitutionList = []

        for row in regexList:
            if int(row[2]) == VALIDATION_TYPE:
                self.validationPatternList.append((row[0],row[3]))
            else:
                substitutionList.append((row[0],row[1],row[2],row[3]))
            
        self.substitutionRegexFormula.setSubstitutionPatternList(substitutionList)

    def getSubstitutionList(self):
        """Get the user defined substitution list.
        """
        return self.substitutionRegexFormula.getSubstitutionPatterns()

    def setSubstitutionList(self, regexList):
        """Set the user regexes substitution list.

           param regexList: a four columns list of lists:
          
           ['matching pattern', 'substitution', 'type', 'language id']
        """
        self.substitutionRegexFormula = RegularExpressionFormula(None)
        
        substitutionList = []

        for row in regexList:
            substitutionList.append((row[0],row[1],row[2],row[3]))

        self.substitutionRegexFormula.setSubstitutionPatternList(substitutionList)

    def getValidationList(self):
        """Get the user defined validation list.
        """
        return self.validationPatternList

    def setValidationList(self, regexList):
        """Set the user regexes validation list.

           param regexList: a four columns list of lists:
          
           ['matching pattern', 'substitution', 'type', 'language id']
        """
        self.validationPatternList = []

        for row in regexList:
            if int(row[2]) == VALIDATION_TYPE:
                self.validationPatternList.append((row[0],row[3]))

    def setLMModeling(self, modelNgram):
        self.lmModeling = modelNgram

    def setFilterSentences(self, filterSentences):
        self.filterSentences = filterSentences

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
    
    def getRegexes(self):
        """Fetch validation and substitution regexes
           from csv file.
        """
        #User did not specified rules
        if self.regexFile == None:
            return

        #Are regexes already loaded in API
        if self.substitutionRegexFormula.hasPatterns() or \
            len(self.validationPatternList) > 0:
            return

        regexList = RegexList().loadFromFile(self.regexFile)
        self.setRegexList(regexList)

    def prepareDocument(self, language = 0):
        """Segment the document into sentences and prepare them.

           param language: an int between 0-4
                - unknown : 0
                - french  : 1
                - german  : 2
                - english : 3
                - italian : 4
        """
        if language> 4 or language < 0:
            raise Exception("Unknown language")

        #Done at the API level to share resources between
        #documents
        self.logger.info("Getting regexes")
        self.getRegexes()

        if self.substitutionRegexFormula.hasPatterns():
            self.logger.info("Using following regexes substitution:\n" +\
                    str(self.substitutionRegexFormula.getSubstitutionPatterns()[0:3]))

        if len(self.validationPatternList) > 0:
            self.logger.info("Using following regexes for sentence validation:\n" +\
                    str(self.validationPatternList[0:3]))

        try:
            self.logger.info("Document file: %s" % self.inputFile)

            #The main document
            self.doc = TextDocument(self.inputFile, language,
                                    self.substitutionRegexFormula,
                                    self.validationPatternList,
                                    self.outputDir)
            
            if self.inputFile != None:
                self.logger.info("Load file, convert to text when pdf document")
                self.doc.loadDocumentAsSentences(self.tempDir)
            elif self.formattedText != None:
                self.logger.info("Load text string as sentences")
                self.doc.loadAsSentences(self.formattedText)
            else:
                raise Exception("No input file or text string provided!")

            #print self.doc.getCleanedText()

            #Control character and strip
            self.logger.info("Cleaning control characters")
            self.doc.cleanTextSentences()

            #print self.doc.getCleanedText()

            if language == 0:
                self.logger.info("Classifying sentences")
                self.doc.setClassifier(self.wordClassifier)
                self.doc.classifySentences()
            else:
                self.doc.setSentencesLanguage(language)

            #print self.doc.getCleanedText()

            #User's supplied regular expression
            if self.substitutionRegexFormula.hasPatterns():
                self.logger.info("Applying user regular expressions per language")
                self.doc.normalizeTextSentences()

            #print self.doc.getCleanedText()

            if self.filterSentences:
                self.logger.info("Filtering data")
                self.doc.filterTextSentences()

            #If LM option is selected, it will be done at
            #the prepareLM stage
            if self.removePunctuation and not self.lmModeling:
                self.doc.removeTextPunctuation()
            
            if self.verbalizePunctuation and not self.removePunctuation:
                self.doc.verbalizeTextPunctuation()

            #print self.doc.getCleanedText()

            #After language id has been set as it depends of
            #languages (i.e. numbers expansion)
            if self.lmModeling:
                self.logger.info("Preparing for language modeling")
                self.doc.prepareLM()

        except Exception, e:
            errorMessage = "An error as occurred when importing sentences: %s\n%s" % (str(e), self.inputFile)
            errorMessage = getErrorMessage(e, errorMessage)
            
            self.logger.critical(errorMessage)

            raise Exception(e)

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

