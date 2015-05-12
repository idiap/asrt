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

import re, logging
import unicodedata

from Cluster import Cluster
from Classifier import LanguageClassifier
from Punctuation import Punctuation

class TextCluster(Cluster):
    """Concrete type representing a text sentence from
       a bilingual pdf document.

       Sentences are stored as utf-8 encoding.
    """
    
    logger = logging.getLogger("Asrt.TextCluster")

    LANGUAGE_ATTRIBUTE      = 'language'
    FRENCH_ID               = 1
    ID_COUNTER              = 0
    MAX_SENTENCE_LENGTH     = 1000
    MIN_SENTENCE_LENGTH     = 10
    MIN_WORDS_COUNT         = 4
    MAX_DIGITS_GROUPS       = 5
    SPACEREGEX              = '[ ]+'

    def __init__(self, document, sentenceText):
        #Some meta data
        TextCluster.ID_COUNTER += 1
        attributesList = [TextCluster.LANGUAGE_ATTRIBUTE]

        #Key is mlf pattern
        Cluster.__init__(self, str(TextCluster.ID_COUNTER), attributesList)

        self.document = document

        #Actual data
        self.addElement(sentenceText)

    def getTextSentence(self, debug=False):
        """Return the associated utf-8 text sentence.
        """
        if len(self.elementList) == 0:
            return ""

        if debug:
            return "---\n%s\n" % "\n".join(reversed(self.elementList))

        return self.elementList[0]

    def setTextSentence(self, textSentence):
        """Set the new text.
        """
        self.elementList.insert(0, textSentence)
        #self.elementList[0] = textSentence

    def prepareClusterText(self, removePunctuation):
        """Clean and normalize.
        """
        #Regex substitution using punctuation symbols
        self._cleanClusterText()

        #We may still want to remove all punctuation
        #in case of non verbalization
        self._normalizeClusterText(removePunctuation)

    def verbaliseTextPunctuation(self):
        """Transform punctuation symbols to words.
        """
        if self.isFrench():
            p = Punctuation()
            self.setTextSentence(p.replaceText(self.getTextSentence()))

    def setLanguage(self, languageId):
        """Language for sentence.
        """
        if languageId != TextCluster.FRENCH_ID:
            self.setAttribute(TextCluster.LANGUAGE_ATTRIBUTE,
                              LanguageClassifier.GERMAN_LABEL)
        else:
            self.setAttribute(TextCluster.LANGUAGE_ATTRIBUTE,
                              LanguageClassifier.FRENCH_LABEL)

    def classify(self, classifier):
        """Classify between french and german.
        """
        l, score = classifier.classify(self.getTextSentence())
        self.setAttribute(TextCluster.LANGUAGE_ATTRIBUTE, l)

    def isFrench(self):
        """Content is French
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                LanguageClassifier.FRENCH_LABEL

    def isGerman(self):
        """Content is German
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                LanguageClassifier.GERMAN_LABEL


    def isItalian(self):
        """Content is Italian
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                LanguageClassifier.ITALIAN_LABEL

    def isEnglish(self):
        """Content is English
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                LanguageClassifier.ENGLISH_LABEL

    def isValid(self):
        """Check validity of sentence.

           Use:
            - sentence length
            - number of digits groups
        """
        strText = self.getTextSentence()

        #Nb characters
        if len(strText) > TextCluster.MAX_SENTENCE_LENGTH or\
           len(strText) < TextCluster.MIN_SENTENCE_LENGTH:
            TextCluster.logger.info("Discard sentence: inappropriate length: %d!" % len(strText))
            return False

        #Nb words
        if len(strText.split(' ')) < TextCluster.MIN_WORDS_COUNT:
            TextCluster.logger.info("Discard sentence, not enough words!")
            return False

        #Nb digit groups
        if len(re.split("\d+", strText)) > TextCluster.MAX_DIGITS_GROUPS:
            TextCluster.logger.info("Discard sentence, to manny groups of digits!")
            return False

        #Try decode
        #Use some regex
        if not self._isTextValid(strText):
            return False

        return True

    def getClusterInfo(self):
        """Return key.
        """
        return "[%s] %s" % (self.key, self.getTextSentence())

    ########################
    # Implementation
    #
    def _cleanClusterText(self):
        """Use a set of regex rules to clean sentences.

           This should be call before normalizing.
        """
        strText = self.getTextSentence()
        strText = self._cleanText(strText)
        self.setTextSentence(strText)

    def _normalizeClusterText(self, removePunctuation):
        """Normalize text.
        """
        strText = self.getTextSentence()

        #Normalize prior to classification.
        #Do not encode in bytes string!
        strText =  TextCluster.normalizeText(strText, removePunctuation)

        self.setTextSentence(strText)

    def _cleanText(self, strText):
        """Use a set of regex rules to clean sentences.
           Regexes are in utf-8 encoding.
        """
        strText = TextCluster.removeControlCharacters(strText)

        #Spaces are normalized to two spaces for regex matching
        strText = re.sub(TextCluster.SPACEREGEX,'  ', strText)

        #print "Before", unicode(strText).encode('utf-8')

        #Regex from database
        for regex, alternate in self.document.regex_patterns_list:
            if alternate == None:
                alternate = ''
                
            #print regex.encode('utf-8'), unicode(strText).encode('utf-8')
            #No ignore case available
            strText = re.sub(regex, alternate, strText)

        #print "After", unicode(strText).encode('utf-8')

        #Spaces are normalized to one space
        strText = re.sub(TextCluster.SPACEREGEX,' ', strText)

        return strText

    def _isTextValid(self, strText):
        """Assess the validity of the text using
           a set of regex rules.

           'strText' is in utf-8 encoding
        """
        #Some regex
        for regex in self.document.regex_filter_list:
            #Ignore case available
            #if re.search(regex, strText, re.IGNORECASE) != None:
            if re.search(regex, strText, flags=re.UNICODE) != None:
                TextCluster.logger.info("Discard:%s\n%s" % (regex.encode("utf-8"), strText.encode("utf-8")))
                return False

        return True

    def __str__(self):
        """Override built in method.
        """
        key = self.getClusterInfo()
        return str(key)

    ########################
    # Implementation
    #
    @staticmethod
    def normalizeText(textUtterance, removePunctuation, ntext=""):
        """Normalize text:

           - remove some punctuation
           - remove new line character at the end
           - remove prepended and trailing spaces

           It keep case for acronyms detection.
           Keep dots for acronyms detection.
           Do not decode string.

        """
        if removePunctuation :
            textUtterance = LanguageClassifier.removePunctuation(strText = textUtterance,
                                                                 removeDots = False)
        textUtterance = textUtterance.rstrip()
        textUtterance = textUtterance.strip()

        return textUtterance

    @staticmethod
    def removeControlCharacters(str):
        """Control characters are replaced
           by spaces.
        """
        lineList = []

        for ch in str:
            if unicodedata.category(ch)[0] != "C":
                lineList.append(ch)
            else:
                lineList.append(' ')

        return "".join(lineList)