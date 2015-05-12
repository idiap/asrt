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
__date__ = "Date: 2011/05/21"
__copyright__ = "Copyright (c) 2008 Alexandre Nanchen"
__license__ = "BSD 3-Clause"

import string
import logging

import nltk.data

from MyFile import MyFile
from ioread import Ioread
from Document import Document

from TextCluster import TextCluster
from TextRepresentation import TextRepresentation
from ClassifierWord import WordClassifier


class TextDocument(Document):
    """A text document.
    """
    logger              = logging.getLogger("Asrt.TextDocument")
    CONVERT_COMMAND     = ['pdftotext', '-raw', '-layout', '-enc', 'UTF-8', '-eol', 'unix', '-nopgbrk']

    ########################
    # Default constructor
    #
    def __init__(self, source, tokenizer_path,
                 regex_patterns_list, regex_filter_list,
                 logDir):
        Document.__init__(self, source)

        self.tokenizer_path = tokenizer_path
        self.regex_patterns_list = regex_patterns_list
        self.regex_filter_list = regex_filter_list
        self.logDir = logDir
        self.classifier = None

    ########################
    # Interface
    #
    def loadDocumentAsSentences(self, tempDir):
        """Convert to text, remove new lines and
           segment into sentences using NLTK
           toolkit.
        """
        #Pdf to text
        tempFileName = self.convertToText(self.sourceFileName, tempDir, self.logDir)

        #Segment into sentences using NLTK toolkit
        self._loadTextDocumentAsSentences(tempFileName)

        #Delete temporary file
        MyFile(tempFileName).removeFile(tempFileName)

    def prepareTextSentences(self, removePunctuation=False):
        """Use a set of regex rules to prepare
           the sentences.
        """
        for textCluster in self.listContent:
            textCluster.prepareClusterText(removePunctuation)

    def filterTextSentences(self):
        """Filter sentences after cleaning replacing
           current content.

           Uses:
            - sentence length
            - number of digit groups
            ...
        """
        filteredContentList = []
        for textCluster in self.listContent:
            if textCluster.isValid():
                filteredContentList.append(textCluster)

        self.listContent = filteredContentList

    def setClassifier(self, classifier):
        """Set the language classifier.
           It assumes it has been trained.
        """
        self.classifier = classifier

    def setSentencesLanguage(self, languageId):
        """Language is known (FRENCH or
           GERMAN, ITALIAN, ENGLISH).
        """
        for textCluster in self.listContent:
            textCluster.setLanguage(languageId)

    def classifySentences(self):
        """Classify sentences by language (FRENCH or
           GERMAN, ITALIAN or ENGLISH).
        """
        if self.classifier == None:
            self.classifier = WordClassifier()
            self.classifier.train()

        for textCluster in self.listContent:
            textCluster.classify(self.classifier)

    ########################
    # Implementation
    #
    def _loadTextDocumentAsSentences(self, filePath):
        """Load a text document and segment
           it into sentences using NLTK.

           Initial new lines are first removed.
        """
        io = Ioread()

        #One string for the whole
        #text file as utf-8 string
        data = io.nltkRead(filePath)

        #Trim new lines
        data = self._replaceNewLines(data)

        #Sentences view of document
        self._segmentIntoSentences(data)

    def _replaceNewLines(self, data):
        """Replace new lines by spaces.
        """
        data = string.replace(data,"\t", " ")

        #Last sentence word splited into two
        data = string.replace(data,"-\n", "")

        return string.replace(data,"\n", " ")

    def _segmentIntoSentences(self, data):
        """Replace current content by sentences.

           The sentences segmentation is done using
           the french pickle of the NLTK toolkit.

           data is in utf-8
        """
        try:
            #Get the french tokenizer
            tokenizer = nltk.data.load(self.tokenizer_path)

            #The actual job
            sentences = tokenizer.tokenize(data)

        except Exception, e:
            TextDocument.logger.critical("Tokenizer error: " + str(e))
            raise Exception("Tokenizer error: " + self.tokenizer_path)

        #Add sentences as clusters
        for line in sentences:
            self.addDocumentLine(TextCluster(self, line))

        TextDocument.logger.info("Loaded %d raw sentences!" % len(sentences))

    ########################
    # Static members
    #
    @staticmethod
    def convertToText(sourcePath, destinationPath, logDir):
        """Extract the textual information from a
           pdf.
        """

        tr = TextRepresentation(sourcePath,destinationPath,logDir)
        return tr.convertToText()