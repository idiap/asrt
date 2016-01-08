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

import logging, re

import nltk.data

from asrt.common.MyFile import MyFile
from asrt.common.ioread import Ioread
from asrt.common.Document import Document

from asrt.common.TextCluster import TextCluster
from asrt.common.TextRepresentation import TextRepresentation
from asrt.common.ClassifierWord import WordClassifier
from asrt.config.AsrtConfig import FRENCH_PICKLE_FOLDER, GERMAN_PICKLE_FOLDER

class TextDocument(Document):
    """A text document.
    """
    logger              = logging.getLogger("Asrt.TextDocument")

    CONVERT_COMMAND     = ['pdftotext', '-raw', '-layout', '-enc', 'UTF-8', '-eol', 'unix', '-nopgbrk']

    MERGECLUSTERSEP     = u"\n"
    DIGITANDDOTREGEX    = u"( |^)([0-9]{1,2})[.]( |$)"
    DIGITANDDOTSUB      = u"\g<1>\g<2>.\g<3>"
    #Do not put a ; for character entity, otherwise
    #sentence segmentation is ocurring
    DIGITANDENTITYREGEX = u"( |^)([0-9]{1,2})&#46( |$)"
    DIGITANDENTITYSUB   = u"\g<1>\g<2>&#46\g<3>"
    
    ########################
    # Default constructor
    #
    def __init__(self, source, languageId,
                 regexSubstitutionFormula, regex_filter_list,
                 logDir, segmentWithNLTK):
        Document.__init__(self, source)

        self.languageId = languageId
        self.regexSubstitutionFormula = regexSubstitutionFormula
        self.regex_filter_list = regex_filter_list
        self.logDir = logDir
        self.classifier = None
        self.segmentWithNLTK = segmentWithNLTK

    ########################
    #Getter and setters
    #
    def setClassifier(self, classifier):
        """Set the language classifier.
           It assumes it has been trained.
        """
        self.classifier = classifier

    def setSentencesLanguage(self, languageId):
        """Language is known.

           param 'languageId': a value beetween 0-4
             unknown : 0
             french  : 1
             german  : 2
             english : 3
             italian : 4
        """
        for textCluster in self.listContent:
            textCluster.setLanguage(languageId)

    ########################
    #Interface
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

    def loadAsSentences(self, strText):
        """Load the given text string as sentences.

           param strText: an utf-8 encoded string
        """
        self._loadAsSentences(strText)

    def getCleanedText(self):
        """Get the cleaned text.
        """
        textList = []
        for textCluster in self.listContent:
            textList.append(textCluster.getTextSentence())

        return self.MERGECLUSTERSEP.join(textList)

    def getCleanedTextPerLanguage(self):
        """Get the classified text per language.

           return a dictionary of utf-8 text.
        """
        textDict = {}
        for textCluster in self.listContent:
            languageId = textCluster.getLanguageId()
            if languageId not in textDict:
                textDict[languageId] = []
            textDict[languageId].append(textCluster.getTextSentence())
        
        #One string per language
        resultDict = {}
        for k, textList in textDict.items():
            resultDict[k] = self.MERGECLUSTERSEP.join(textList)
        return resultDict

    def cleanTextSentences(self):
        """Use a set of regex rules to prepare
           the sentences.
        """
        self._applyAllClusters('clean')

    def normalizeTextSentences(self):
        """Use a set of regex rules to prepare
           the sentences.

           First group clusters per languages and then
           apply language based normalization.
        """
        #Get cluster per language
        lang2clusterDict = self._getLanguage2ClustersDict()

        bEmpty = True

        #Normalize text per language
        for languageId, clusterList in lang2clusterDict.items():
            #Read all cluster texts
            textList = []
            for textCluster in clusterList:
                textList.append(textCluster.getTextSentence())

            #Join all text
            allText = self.MERGECLUSTERSEP.join(textList)

            #Normalize text
            allText = self.regexSubstitutionFormula.apply(allText, languageId)
            sentencesList = allText.split(self.MERGECLUSTERSEP)

            #Add and set language id
            self._addSentences(sentencesList, languageId, bEmpty)

            if bEmpty:
                bEmpty = False

    def prepareLM(self):
        """Prepare text sentences for N-Gram modeling.
        """
        self._applyAllClusters("prepareLM")

    def removeTextPunctuation(self):
        """Remove punctuation symbols.
        """
        self._applyAllClusters("removeTextPunctuation")

    def verbalizeTextPunctuation(self):
        """Transform punctuation symbols to words.
           Currently only implemented for French.
        """
        self._applyAllClusters("verbalizeTextPunctuation")

    def filterTextSentences(self):
        """Filter sentences after cleaning.

           Uses:
            - sentence length
            - number of digit groups
            - user defined rules
        """
        filteredContentList = []
        for textCluster in self.listContent:
            if textCluster.isValid():
                filteredContentList.append(textCluster)

        self.listContent = filteredContentList

    def classifySentences(self):
        """Classify sentences by language (FRENCH or
           GERMAN, ITALIAN or ENGLISH).
        """
        if self.classifier == None:
            self.classifier = WordClassifier()
            self.classifier.train()

        for textCluster in self.listContent:
            textCluster.classify(self.classifier)

    def display(self):
        """Display document content.
        """
        for textCluster in self.listContent:
            print textCluster

    ########################
    #Implementation
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
        self._loadAsSentences(data)

    def _loadAsSentences(self, strText):
        """Load the given text as sentences.

           Algorithm is:
             - New lines removal
             - Problematic periods replacement
             - Sentences segmentation with nltk
             - Problematic periods restauration

           param strText: an utf-8 encoded string
        """
        tokenizer_path = FRENCH_PICKLE_FOLDER
        if self.languageId == 2:
            tokenizer_path = GERMAN_PICKLE_FOLDER

        sentences = []
        if self.segmentWithNLTK:
            TextDocument.logger.info("Segment with NLTK")
            #Trim new lines
            strText = self._replaceNewLines(strText)

            #Problematic periods replacement
            strText = self._replaceProblematicPeriods(strText)

            #Nltk segmentation
            sentences = self._segmentIntoSentences(strText, tokenizer_path)

            #Problematic periods restauration
            for i, s in enumerate(sentences):
                sentences[i] = self._replaceProblematicPeriods(s, forward=False)
        else:
            TextDocument.logger.info("Segment with new lines")
            sentences = strText.split(u"\n")

        #Make text clusters with unknown language id
        self._addSentences(sentences)

        TextDocument.logger.info("Loaded %d raw sentences!" % len(sentences))

    def _applyAllClusters(self, method):
        """Apply 'method' to all clusters.
        """
        for textCluster in self.listContent:
            getattr(textCluster, method)()

    def _replaceNewLines(self, data):
        """Replace new lines by spaces.

           New lines are not considered at the end
           of a sentence.

           param data: an utf-8 encoded string
        """
        #Last sentence word splited into two
        data = re.sub(ur"-\n", u"", data, flags=re.UNICODE)
        
        return re.sub(ur"\n", u" ", data, flags=re.UNICODE)

    def _replaceProblematicPeriods(self, data, forward=True):
        """Convert dots preceded from a number and followed
           by a space into an html entity.

           If forward is set to False, it will convert from
           html entity to dots.

           This escaping is done in order to prevent
           segmenting sentences on numbers.
        """
        if not forward:
            return re.sub(self.DIGITANDENTITYREGEX, self.DIGITANDDOTSUB, data, 
                           flags=re.UNICODE)
    
        return re.sub(self.DIGITANDDOTREGEX, self.DIGITANDENTITYSUB, data, 
                        flags=re.UNICODE)

    def _segmentIntoSentences(self, data, tokenizer_path):
        """Replace current content by sentences.

           The sentences segmentation is done using
           the french pickle of the NLTK toolkit.

           param data: an utf-8 encoded string
        """
        try:

            #Get the french tokenizer
            tokenizer = nltk.data.load(tokenizer_path)

            #The actual job
            sentences = tokenizer.tokenize(data)

        except Exception, e:
            TextDocument.logger.critical("Tokenizer error: " + str(e))
            raise Exception("Tokenizer error: " + self.tokenizer_path)

        return sentences
        
    def _addSentences(self, sentencesList, languageId=0, bEmpty = True):
        """Add the given sentences to the document.

           param 'sentencesList': a list of text sentences
           param 'languageId'   : the language id for the sentences list
           param 'bEmpty'       : empty current document is set otherwise
                                  add to existing clusters 
        """
        if bEmpty: self.reset()

        #Add sentences as clusters
        for line in sentencesList:
            if self.segmentWithNLTK:
                #Further sentence split to avoid long paragraphes
                for utterance in re.split(ur"\t|;|:|!|\?", line, flags=re.UNICODE):
                    self._addClusterText(utterance, languageId)
            else:
                self._addClusterText(line, languageId)

    def _addClusterText(self, utterance, languageId):
        """Add 'utterance' as a text cluster.

           param utterance: an utf-8 encoded string
        """
        utterance = utterance.strip()
        if len(utterance) > 0:
            c = TextCluster(self, utterance)
            c.setLanguage(languageId)
            self.addDocumentLine(c)

    def _getLanguage2ClustersDict(self):
        """Map languages with a list of clusters.

           return a dictionary with one entry per
                  language.
        """
        languageDict = {}
        for textCluster in self.listContent:
            clusterLanguageId = textCluster.getLanguageId()
            #First cluster
            if clusterLanguageId not in languageDict:
                languageDict[clusterLanguageId] = []
            languageDict[clusterLanguageId].append(textCluster)
        return languageDict

    ########################
    #Static members
    #
    @staticmethod
    def convertToText(sourcePath, destinationPath, logDir):
        """Extract the textual information from a
           pdf.
        """
        tr = TextRepresentation(sourcePath,destinationPath,logDir)
        return tr.convertToText()
