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
from formula.FormulaLMPreparation import LMPreparationFormula
from config import FRENCH_LABEL, GERMAN_LABEL, ENGLISH_LABEL
from config import ITALIAN_LABEL, LANGUAGEID2LABELS
from config import MAX_SENTENCE_LENGTH, MIN_SENTENCE_LENGTH
from config import MIN_WORDS_COUNT, MAX_WORDS_COUNT
from config import MAX_DIGITS_GROUPS, LANGUAGE2ID

class TextCluster(Cluster):
    """Concrete type representing a text sentence from
       a bilingual pdf document.

       Sentences are stored as utf-8 encoding.
    """
    
    logger = logging.getLogger("Asrt.TextCluster")

    LANGUAGE_ATTRIBUTE      = 'language'
    FRENCH_ID               = 1
    ID_COUNTER              = 0
    SPACEREGEX              = '[ ]+'

    def __init__(self, document, sentenceText):
        """Constructor.
        """
        #Give a unique id to cluster
        TextCluster.ID_COUNTER += 1

        #Unknown language
        attributesList = [(TextCluster.LANGUAGE_ATTRIBUTE, 0)]

        #Key is mlf pattern
        Cluster.__init__(self, str(TextCluster.ID_COUNTER), attributesList)

        self.document = document

        #Actual data
        self.addElement(sentenceText)

        #LM normalization
        self.lmPreparationFormula = LMPreparationFormula()

    #####################
    #Getters and setters
    #
    def getTextSentence(self, noPunctuation = False, debug=False):
        """Return the associated utf-8 text sentence.
        """
        if len(self.elementList) == 0:
            return ""

        if debug:
            return u"---\n%s\n" % u"\n".join(reversed(self.elementList))

        return self.elementList[0]

    def getLanguageId(self):
        """Get the cluster language id.

           Return an integer between 0-4
             unknown : 0
             french  : 1
             german  : 2
             english : 3
             italian : 4
        """
        strLanguage = self.getAttribute(self.LANGUAGE_ATTRIBUTE)
        return LANGUAGE2ID[strLanguage]

    def setTextSentence(self, textSentence):
        """Set the new text.

           param textSentence: an utf-8 encoded string
        """
        self.elementList[0] = textSentence

    def setLanguage(self, languageId):
        """Language for sentence.

           param 'languageId' : a value between 0 and 4
            unknown : 0
            french  : 1
            german  : 2
            english : 3
            italian : 4
        """
        if languageId > 4 or languageId < 0:
            raise Exception("Unknown language")

        strLanguage = LANGUAGEID2LABELS[languageId]
        self.setAttribute(TextCluster.LANGUAGE_ATTRIBUTE, strLanguage)

    #####################
    #Public interface
    #
    def clean(self):
        """Perform text cleaning.

           Heuristic is:
              - remove control characters
              - normalize spaces to one space
              - strip spaces from beginning and end of string
        """
        strText = self.getTextSentence()
        strText = TextCluster.removeControlCharacters(strText)
        self.setTextSentence(strText.rstrip().strip())
    
    def classify(self, classifier):
        """Classify between french and german.
        """
        l, score = classifier.classify(self.getTextSentence())
        self.setAttribute(TextCluster.LANGUAGE_ATTRIBUTE, l)

    def removeTextPunctuation(self):
        """Remove punctuation symbols.
        """
        strText = self.getTextSentence()
        strText = LanguageClassifier.removePunctuation(strText = strText,
                                                       removeDots = False)
        self.setTextSentence(strText)

    def verbalizeTextPunctuation(self):
        """Transform punctuation symbols to words.
           Currently only implemented for French.
        """
        if self.isFrench():
            p = Punctuation()
            self.setTextSentence(p.replaceText(self.getTextSentence()))
        else:
            raise Exception("Text verbalization is only implemented for French!")

    def prepareLM(self):
        """Prepare for language modeling.
        """
        strText = self.getTextSentence()
        languageId = self.getLanguageId()

        self.lmPreparationFormula.setText(strText)
        self.lmPreparationFormula.setLanguageId(languageId)
        strText = self.lmPreparationFormula.prepareText()
        
        self.setTextSentence(strText)

    #####################
    #Predicates
    #
    def isValid(self):
        """Check validity of sentence.

           Heuristic is:
            - sentence length
            - number of digits groups
        """
        strText = self.getTextSentence()

        #Nb characters
        if len(strText) > MAX_SENTENCE_LENGTH or\
           len(strText) < MIN_SENTENCE_LENGTH:
            #print strText.encode('utf-8')
            TextCluster.logger.info("Discard sentence: inappropriate length: %d!" % len(strText))
            return False

        #Nb words
        nbWords = len(strText.split(' '))
        if nbWords < MIN_WORDS_COUNT or \
           nbWords > MAX_WORDS_COUNT:
            #print strText.encode('utf-8')
            TextCluster.logger.info("Discard sentence, not enough or to many words!")
            return False

        #Nb digit groups
        if len(re.split("\d+", strText)) > MAX_DIGITS_GROUPS:
            #print strText.encode('utf-8')
            TextCluster.logger.info("Discard sentence, to many groups of digits!")
            return False

        #Try decode
        #Use some regex
        if not self._isTextValid(strText):
            return False

        return True

    def isFrench(self):
        """Content is French
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                     FRENCH_LABEL

    def isGerman(self):
        """Content is German
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                     GERMAN_LABEL

    def isItalian(self):
        """Content is Italian
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                     ITALIAN_LABEL

    def isEnglish(self):
        """Content is English
        """
        return self.getAttribute(TextCluster.LANGUAGE_ATTRIBUTE) ==\
                     ENGLISH_LABEL

    def getClusterInfo(self):
        """Return key.
        """
        return "[%s] %s" % (self.key, self.getTextSentence())

    ########################
    # Implementation
    #
    def _isTextValid(self, strText):
        """Assess the validity of the text using
           a set of regex rules.

           'strText' is in utf-8 encoding
        """
        clusterLanguageId = self.getLanguageId()

        #Some regex
        for regex, regexLanguageId in self.document.regex_filter_list:
            regexLanguageId = int(regexLanguageId)
            #Does it match the text language
            if regexLanguageId != clusterLanguageId and \
               regexLanguageId != 0:
                continue
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
        return str(key.encode('utf-8'))

    ########################
    # Implementation
    #
    @staticmethod
    def normalizeText(textUtterance):
        """Normalize text:

           - remove new line character at the end
           - remove prepended and trailing spaces

           
        """
        textUtterance = textUtterance.rstrip().strip()
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
