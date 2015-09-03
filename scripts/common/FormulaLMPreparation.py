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
__date__ = "Date: 2015/09"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../config")

import logging, re
from AsrtConstants import UTF8MAP, PUNCTUATIONEXCLUDE
from AsrtConstants import PUNCTUATIONMAP, PUNCTUATIONPATTERN

class LMPreparationFormula():
    """Main formula for language modeling text
       preparation.
    """
    logger              = logging.getLogger("Asrt.LMPreparationFormula")
    ordDict             = {}
    SPACEPATTERN          = u"[ ]+"
    PUNCTUATIONREGEX    = re.compile(PUNCTUATIONPATTERN, flags=re.UNICODE)

    def __init__(self):
        """Default constructor.
        """
        self.strText = ""
        self.languageId = 0

    #####################
    #Getters and setters
    #
    def getText(self):
        return self.strText
    
    def getLanguageId(self):
        """Return a number between 0 and 4:

           0:'unknown', 1:'French', 2:'German', 
           3:'English', 4:'Italian'
        """
        return self.languageId

    def setText(self, strText):
        """Set the underlying text with 'strText'.

           param strText: an utf-8 encoded string
        """
        self.strText = strText

    def setLanguageId(self, languageId):
        """Set the language id.

           A value between 0 and 4:

           0:'unknown', 1:'French', 2:'German', 
           3:'English', 4:'Italian'
        """
        self.languageId = languageId

    ##################
    #Public interface
    #
    def prepareText(self):
        """Prepare 'strText' for language modeling.

           Heuristic is :
                Noise words filtering
                Character based normalization
                Word based normalization 
                    
            param strText: an utf-8 encoded string
            return the normalized text in utf-8 encoding
        """
        self.filterNoiseWords()
        self.normalizeCharacters()
        self.normalizeWords()

    def filterNoiseWords(self):
        """Do not keep some words considered as noise.

           For example words consisting of 4 or more punctuation 
           characters. 
        """
        wordsList = re.split(self.SPACEPATTERN, self.strText, flags=re.UNICODE)
        newWordsList = []
        for w in wordsList:
            if not LMPreparationFormula.isNoise(w):
                newWordsList.append(w)

        self.strText = u" ".join(newWordsList)
        return self.strText

    def normalizeCharacters(self):
        """Character normalization:
            - UTF8 normalization
            - Punctuation normalization 
        """
        self._normalizeUtf8()
        self._normalizePunctuation()

        return self.strText

    def normalizeWords(self):
        """Word base normalization.

           This is language dependant.

            - Contraction prefixes, suffixes --> separate
            - Abbreviations --> normalize
            - Acronyms (upper case words) --> split into letters
            - Decimal numbers --> add comma or dot words
            - Ordinal numbers  --> transform
            - Cardinal numbers --> transform
            - Case normalization (change to lower case)
        """
        pass

    @staticmethod
    def getOrdDict():
        """Utf-8 characters mapping in the form of a
           code point dictionary.
        """
        if len(LMPreparationFormula.ordDict.keys()) > 0:
            return LMPreparationFormula.ordDict

        #Substitution dictionary, assume one character only
        ordDict = {}
        for match, sub, comment, languageId in UTF8MAP:
            if ord(match) in ordDict:
                raise Exception("Already in dictionary %s !" % unichr(ord(match)))
            ordDict[ord(match)] = sub

        LMPreparationFormula.ordDict = ordDict
        return LMPreparationFormula.ordDict

    @staticmethod
    def isNoise(strWord):
        """Check if 'strWord' is a noise word.

           return True or False
        """
        return LMPreparationFormula.PUNCTUATIONREGEX.search(strWord) != None
    
    ##################
    #Implementation
    #
    def _normalizeUtf8(self):
        """Some punctuation characters are normalized.

           param 'strText': utf-8 encoded string
           return an utf-8 encoded string
        """
        #Mapping dictionary
        ordDict = LMPreparationFormula.getOrdDict()
        
        utf8List = []
        #Loop through unicode characters
        for i, c in enumerate(self.strText):
            if ord(c) in ordDict:
                utf8List.append(ordDict[ord(c)])
            else:
                utf8List.append(c)

        self.strText = u"".join(utf8List).rstrip().strip()
        self.strText = re.sub(self.SPACEPATTERN, u" ", self.strText, flags=re.UNICODE)

    def _normalizePunctuation(self):
        """Some punctuation characters are 
           normalized:
           - Removal by spacing
                    - Single, double quotes
                    - Exclamation, Interrogation marks
                    - Braces, round, square, curly
                    - Slashes, back, forward
                    - Sharp symbol
                    - Star, plus, minus
                    - Comma, column, semi-column, dot (keep it for abbreviations)
                    - Lower, greater equal sign
                    - Alone diacritics marks (circumflex accent)
                    - Hyphen, underscore
                    - Back quote
                    - Pipe
                    - Tilde
                - Modification
                    - Percent % --> percent
                    - Ampersand & --> and
                    - At sign @ --> at
                    - Dollars symbol $ --> dollars

            param 'strText': utf-8 encoded string
            return an utf-8 encoded string
        """
        unicodeList = []
        for i, c in enumerate(self.strText):
            strC = c.encode('utf-8')
            if strC in PUNCTUATIONEXCLUDE:
                continue
            elif self.languageId != 0 and strC in PUNCTUATIONMAP:
                unicodeList.append(u" " + PUNCTUATIONMAP[strC][self.languageId] + u" ")
            else:
                unicodeList.append(c)

        self.strText = u"".join(unicodeList).rstrip().strip()
        self.strText = re.sub(self.SPACEPATTERN, u" ", self.strText, flags=re.UNICODE)
