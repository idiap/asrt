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

import logging, re
from asrt.common.english.FormulaNumber import NumberFormula as EnglishNumberFormula
from asrt.common.french.FormulaNumber import NumberFormula as FrenchNumberFormula
from asrt.common.german.FormulaNumber import NumberFormula as GermanNumberFormula
from asrt.common.formula.FormulaRegularExpression import RegularExpressionFormula
from asrt.common.RegularExpressionList import RegexList
from asrt.common.AsrtConstants import UTF8MAP, PUNCTUATIONEXCLUDE, PUNCTUATIONKEEPINWORD, DOTCOMMAEXCLUDE
from asrt.common.AsrtConstants import PUNCTUATIONMAP, PUNCTUATIONPATTERN, SPACEPATTERN
from asrt.common.AsrtConstants import DATEREGEXLIST, CONTRACTIONPREFIXELIST, ACRONYMREGEXLIST
from asrt.common.AsrtConstants import ABBREVIATIONS, APOSTHROPHELIST, CAPTURINGDIGITPATTERN
from asrt.common.AsrtConstants import GROUPINGDOTCOMMAPATTERN, EXPANDEXCEPTIONS
from asrt.common.AsrtConstants import ACRONYMDELIMITER
from asrt.config.AsrtConfig import FRENCH, GERMAN, ENGLISH

class LMPreparationFormula():
    """Main formula for language modeling text
       preparation.
    """
    logger                      = logging.getLogger("Asrt.LMPreparationFormula")

    ordDict                     = {}
    abbreviationsDict           = {}

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
    ALLPUNCTUATIONSYMBOLS       = "".join(PUNCTUATIONEXCLUDE + DOTCOMMAEXCLUDE)

    def __init__(self):
        """Default constructor.
        """
        self.strText = ""
        self.languageId = 0
        self.keepNewWords = True
        self.numberFormula = {
            FRENCH: FrenchNumberFormula,
            GERMAN: GermanNumberFormula,
            ENGLISH: EnglishNumberFormula
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
        LMPreparationFormula.ordDict = {}
        LMPreparationFormula.ordDict = LMPreparationFormula._getOrdDict(self.languageId)

    def setKeepNewWords(self, keepNewWords):
        """Keep new words.
        """
        self.keepNewWords = keepNewWords

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
        #print self.strText
        #Some preprocessing
        self._filterNoiseWords()
        self._normalizeUtf8()
        #Before punctuation removal, some rules
        #are applied
        self._normalizeDates()
        self._expandAbbreviations()

        if not self.keepNewWords:
            self._expandNumberInWords()
            #print self.strText

        #Removal of some of punctuation symbols
        self._normalizePunctuation(PUNCTUATIONEXCLUDE)
        #print self.strText

        #Dot and comman punctuation symbols are still needed
        self._normalizeWords()
        #print self.strText

        self._normalizeContractionPrefixes()
        #print self.strText

        #Make sure no punctuation is remaining
        self._normalizePunctuation(self.ALLPUNCTUATIONSYMBOLS)
        #print self.strText

        if not self.keepNewWords:
            self._expandAcronyms()
            #print self.strText

        self._normalizeCase()
        #print self.strText

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

        languageId = self.getLanguageId()

        #Mapping dictionary
        ordDict = LMPreparationFormula._getOrdDict(languageId)

        utf8List = []
        #Loop through unicode characters
        for i, c in enumerate(self.strText):
            if ord(c) in ordDict:
                utf8List.append(ordDict[ord(c)])
            else:
                utf8List.append(c)

        self.strText = u"".join(utf8List).rstrip().strip()

        if len(self.strText) > 1 and \
               self.strText[-1] in self.ALLPUNCTUATIONSYMBOLS and \
               self.strText[-2].isdigit():
            self.strText = self.strText.rstrip(self.ALLPUNCTUATIONSYMBOLS)

        self.strText = re.sub(SPACEPATTERN, u" ", self.strText, flags=re.UNICODE)

    def _normalizeDates(self):
        """Normalize dates.
        """
        self.strText = self.dateFormula.apply(self.strText, self.languageId)

    def _expandAbbreviations(self):
        """Expand language abbreviations.
        """
        aDict = self._getAbbreviationsDict()
        if self.languageId not in aDict:
            return

        wordsList = re.split(SPACEPATTERN, self.strText, flags=re.UNICODE)
        newWordsList = []
        for w in wordsList:
            wByte = w.encode('utf-8')
            if wByte in aDict[self.languageId]:
                newWordsList.append(aDict[self.languageId][wByte])
            else:
                newWordsList.append(w)

        self.strText = u" ".join(newWordsList)

    def _expandNumberInWords(self):
        """If there are numbers in words, split them.

           i.e. A1   --> A. 1
                P3B  --> P. 3 B.
                P5B4 --> P. 5 B. 4
                PPB5 --> PPB 5 (acronyms are expanded later on)
        """
        wordsList = re.split(SPACEPATTERN, self.strText, flags=re.UNICODE)

        newWordsList = []
        for w in wordsList:
            tokenList = re.split(CAPTURINGDIGITPATTERN, w, flags=re.UNICODE)
            #Numbers need to contain a digit
            #Ordinal numbers are not expanded
            if not re.search(u"[0-9]", w) or w.endswith(EXPANDEXCEPTIONS):
                newWordsList.append(w)
            #We have a match
            elif len(tokenList) > 1:
                #Single letter acronyms
                for i, t in enumerate(tokenList):
                    #Digit return false
                    if len(t) == 1 and t.isupper():
                        tokenList[i] = tokenList[i] + u"."
                newWord = u" ".join(tokenList).strip()
                #Group P . 5 into P. 5
                newWord = re.sub(GROUPINGDOTCOMMAPATTERN,u"\g<2> ",newWord)
                newWordsList.append(newWord)
            else:
                newWordsList.append(w)

        self.strText = u" ".join(newWordsList)

    def _expandAcronyms(self):
        """Acronyms are splitted.

           i.e. PDC --> p. d. c.
        """
        self.strText = self.acronymFormula.apply(self.strText, self.languageId)
        self.strText = re.sub(ACRONYMDELIMITER, u"", self.strText, flags=re.UNICODE)

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
        unicodeList, prevC, beforePrevC = [], u"", u""
        for i, c in enumerate(self.strText):
            strC = c.encode('utf-8')
            #For date format, i.e. 21-Jul
            if strC in excludeList:
                #Keep dots after uppercase letters
                if beforePrevC in (""," ") and not prevC.isdigit() \
                    and strC == ".":
                    unicodeList.append(c)
                    unicodeList.append(u" ")
                #Keep some special characters if they appear after a non-space value
                elif self.keepNewWords and prevC not in ("", " ") and strC in PUNCTUATIONKEEPINWORD:
                    unicodeList.append(c)
            elif self.languageId != 0 and strC in PUNCTUATIONMAP:
                unicodeList.append(u" " + PUNCTUATIONMAP[strC][self.languageId] + u" ")
            else:
                unicodeList.append(c)
            beforePrevC = prevC
            prevC = strC

        self.strText = u"".join(unicodeList).rstrip().strip()
        self.strText = re.sub(u"(^- *| - |-$)", u"", self.strText, flags=re.UNICODE)
        self.strText = re.sub(u"(- )", u" ", self.strText, flags=re.UNICODE)
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
            self.logger.warning("LM preparation not implemented for language id %d" % languageId)
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
    def _getOrdDict(langId):
        """Utf-8 characters mapping in the form of a
           code point dictionary.
        """
        if len(LMPreparationFormula.ordDict.keys()) > 0:
            return LMPreparationFormula.ordDict

        #Substitution dictionary, assume one character only
        ordDict = {}
        for match, sub, comment, languageId in UTF8MAP:
            if ord(match) in ordDict:
                raise Exception("Already in dictionary '%s' '%s'!" % (unichr(ord(match)),
                                  comment.encode('utf8')))
            if (langId == int(languageId) or int(languageId) == 0):
                ordDict[ord(match)] = sub

        LMPreparationFormula.ordDict = ordDict
        return LMPreparationFormula.ordDict

    @staticmethod
    def _getAbbreviationsDict():
        """Get the abbreviations dictionary with keys
           encoded in byte string for comparison.
        """
        if len(LMPreparationFormula.abbreviationsDict.keys()) > 0:
            return LMPreparationFormula.abbreviationsDict

        aDict = {}
        for lang in ABBREVIATIONS.keys():
            if lang not in aDict:
                aDict[lang] = {}
            for k,v in ABBREVIATIONS[lang].items():
                aDict[lang][k.encode('utf-8')] = v

        LMPreparationFormula.abbreviationsDict = aDict
        return LMPreparationFormula.abbreviationsDict

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
