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
from french.FormulaNumber import NumberFormula as FrenchNumberFormula
from german.FormulaNumber import NumberFormula as GermanNumberFormula
from formula.FormulaRegularExpression import RegularExpressionFormula
from RegularExpressionList import RegexList
from AsrtConstants import UTF8MAP, PUNCTUATIONEXCLUDE, DOTCOMMAEXCLUDE
from AsrtConstants import PUNCTUATIONMAP, PUNCTUATIONPATTERN, SPACEPATTERN
from AsrtConstants import DATEREGEXLIST, CONTRACTIONPREFIXELIST, ACRONYMREGEXLIST
from AsrtConstants import ABBREVIATIONS, APOSTHROPHELIST
from config import FRENCH, GERMAN

class LMPreparationFormula():
    """Main formula for language modeling text
       preparation.
    """
    logger                      = logging.getLogger("Asrt.LMPreparationFormula")
    
    ordDict                     = {}

    #Regular expressions formulas
    dateFormula                 = RegularExpressionFormula(None, 
                                    RegexList.removeComments(DATEREGEXLIST))
    apostropheFormula           = RegularExpressionFormula(None, 
                                    RegexList.removeComments(APOSTHROPHELIST))
    contractionPrefixFormula    = RegularExpressionFormula(None, 
                                    RegexList.removeComments(CONTRACTIONPREFIXELIST))
    acronymFormula              = RegularExpressionFormula(None, 
                                    RegexList.removeComments(ACRONYMREGEXLIST))

    PUNCTUATIONREGEX            = re.compile(PUNCTUATIONPATTERN, flags=re.UNICODE)

    def __init__(self):
        """Default constructor.
        """
        self.strText = ""
        self.languageId = 0
        self.numberFormula = {
            FRENCH: FrenchNumberFormula,
            GERMAN: GermanNumberFormula
        }

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

           param 'languageId': a value between 0 and 4:

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
                Dates normalization
                Language based abbreviations expansion
                Word based normalization
                Acronyms normalization
                Contraction prefixes separation
                Lowercase normalization

            return the normalized text in utf-8 encoding
        """
        #Some preprocessing
        self._filterNoiseWords()
        self._normalizeUtf8()

        #Before punctuation removal, some rules
        #are applied
        self._normalizeDates()
        self._expandAbbreviations()

        #Removal of some of punctuation symbols
        self._normalizePunctuation(PUNCTUATIONEXCLUDE)

        #Dot and comman punctuation symbols are still needed
        self._normalizeWords()
        self._normalizeContractionPrefixes()

        #Make sure no punctuation is remaining
        self._normalizePunctuation(DOTCOMMAEXCLUDE + PUNCTUATIONEXCLUDE)

        self._expandAcronyms()
        self._normalizeCase()

        return self.strText

    ##################
    #Implementation
    #
    def _filterNoiseWords(self):
        """Do not keep some words considered as noise.

           For example words consisting of 4 or more punctuation 
           characters. 
        """
        wordsList = re.split(SPACEPATTERN, self.strText, flags=re.UNICODE)
        newWordsList = []
        for w in wordsList:
            if not LMPreparationFormula._isNoise(w):
                newWordsList.append(w)

        self.strText = u" ".join(newWordsList)
        return self.strText

    def _normalizeUtf8(self):
        """Some punctuation characters are normalized.
        """
        #Mapping dictionary
        ordDict = LMPreparationFormula._getOrdDict()
        
        utf8List = []
        #Loop through unicode characters
        for i, c in enumerate(self.strText):
            if ord(c) in ordDict:
                utf8List.append(ordDict[ord(c)])
            else:
                utf8List.append(c)

        self.strText = u"".join(utf8List).rstrip().strip()
        self.strText = re.sub(SPACEPATTERN, u" ", self.strText, flags=re.UNICODE)

    def _normalizeDates(self):
        """Normalize dates.
        """
        self.strText = self.dateFormula.apply(self.strText, self.languageId)
        
    def _expandAbbreviations(self):
        """Expand language abbreviations.
        """
        #Should not happen, as filtered before
        if self.languageId not in ABBREVIATIONS:
            return

        wordsList = re.split(SPACEPATTERN, self.strText, flags=re.UNICODE)
        newWordsList = []
        for w in wordsList:
            wByte = w.encode('utf-8')
            if wByte in ABBREVIATIONS[self.languageId]:
                newWordsList.append(ABBREVIATIONS[self.languageId][wByte])
            else:
                newWordsList.append(w)

        self.strText = u" ".join(newWordsList)

    def _expandAcronyms(self):
        """Acronyms are splitted.

           i.e. PDC --> p. d. c.
        """
        self.strText = self.acronymFormula.apply(self.strText, self.languageId)
        
    def _normalizePunctuation(self, excludeList):
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

            param 'excludeList' : a list of exclude punctuation symbols
        """
        unicodeList = []
        for i, c in enumerate(self.strText):
            strC = c.encode('utf-8')
            #For date format, i.e. 21-Jul
            if strC in excludeList:
                unicodeList.append(u" ")
            elif self.languageId != 0 and strC in PUNCTUATIONMAP:
                unicodeList.append(u" " + PUNCTUATIONMAP[strC][self.languageId] + u" ")
            else:
                unicodeList.append(c)

        self.strText = u"".join(unicodeList).rstrip().strip()
        self.strText = re.sub(u"(^- *| - |- |-$)", u"", self.strText, flags=re.UNICODE)
        self.strText = re.sub(SPACEPATTERN, u" ", self.strText, flags=re.UNICODE)

    def _normalizeWords(self):
        """Word base normalization.

           This is language dependant.

            - Contraction prefixes, suffixes --> separate
            - Abbreviations --> normalize
            - Acronyms (upper case words) --> split into letters
            - Decimal numbers --> add comma or dot words
            - Ordinal numbers  --> transform
            - Cardinal numbers --> transform
        """
        languageId = self.getLanguageId()
        if languageId not in self.numberFormula:
            #self.logger.warning("LM preparation not implemented for language id %d" % languageId)
            return
        numberFormula = self.numberFormula[languageId]

        self.strText = numberFormula.apply(self.strText)

    def _normalizeContractionPrefixes(self):
        """Contraction prefixes are separated and
           acronyms are normalized.
        """
        self.strText = self.apostropheFormula.apply(self.strText, self.languageId)
        self.strText = self.contractionPrefixFormula.apply(self.strText, self.languageId, False)
    
    def _normalizeCase(self):
        """Case normalization (change to lower case)
        """
        self.strText = self.strText.lower()

    @staticmethod
    def _getOrdDict():
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
    def _isNoise(strWord):
        """Check if 'strWord' is a noise word.

           return True or False
        """
        return LMPreparationFormula.PUNCTUATIONREGEX.search(strWord) != None

    @staticmethod
    def _applyRegexes(strText, regexList):
        for p, r, t in regexList:
            strText = re.sub(p, r, strText, flags=re.UNICODE)
        return strText
