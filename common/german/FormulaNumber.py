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
from roman import fromRoman
from asrt.common.Rule import Rule, Pattern
from asrt.common.AsrtUtility import convertNumber
from asrt.common.AsrtConstants import SPACEPATTERN
from asrt.common.german.Number import Number

class NumberFormula():
    """A set of rules to 'unformat' formatted numbers.
    """

    logger                  = logging.getLogger("Asrt.NumberFormula")

    THOUSANDSEPARATOR       = u"'"

    HASNUMBERREGEX          = re.compile(u"([0-9]|I|V|X|L|C|D|M)+", flags=re.UNICODE)
    CARDINALNUMBERREGEX     = re.compile(u"[0-9]+$", flags=re.UNICODE)
    ORDINALNUMBERREGEX      = re.compile(u"([0-9]+er|[0-9]+[.]|[IVXLCDM]{2,}[.])$", flags=re.UNICODE)
    DECIMALNUMBERREGEX      = re.compile(u"[0-9,.]+[0-9,.]*$", flags=re.UNICODE)
    ROMANNUMBERREGEX        = re.compile(u"[IVXLCDM]{2,}$", flags=re.UNICODE)

    ##################
    #Public interface
    #
    @classmethod
    def apply(cls, strText):
        """Apply formula to numbers.

           Numbers cateories are:
             - Decimal numbers
             - Ordinal numbers
             - Cardinal numbers
             - Roman numbers

           param strText: an utf-8 encoded string
           return an utf-8 encoded string
        """
        return convertNumber(cls, strText)

    ##################
    #Implementation
    #
    @staticmethod
    def _normalizeNumber(strWord):
        """Remove tousand separator.

           param strWord: an utf-8 encoded words
           return an utf-8 encoded string
        """
        strWord = strWord.replace(NumberFormula.THOUSANDSEPARATOR, u"")

        #Case when there are two full stops, or one comma
        #after a number
        if strWord.endswith(("..",",")):
            strWord = strWord[:-1]
    
        return strWord

    @staticmethod
    def _cardinal2word(strNumber):
        """Convert a cardinal number to a written
           word.

           param strNumber: an utf-8 cardinal number
           return a 'written' cardinal number
        """
        return Number.convertNumberIntoLetters(strNumber)

    @staticmethod
    def _ordinal2word(wordsList, indice):
        """Convert an ordinal number to a written
           word.

           i.e. 1. --> erste

           param strNumber: an utf-8 ordinal number
           return a 'written' ordinal number
        """
        strNumber = NumberFormula._normalizeNumber(wordsList[indice])

        #Update with correct form
        wordsList[indice] = strNumber

        #Check for specific ordinal ending with dates
        ending = NumberFormula._getOrdinalEnding(strNumber, wordsList, indice)
        bOrdinal = len(ending) > 0

        #ending = u""
        strNewNumber = re.sub(u"([.]|er)", "", strNumber)

        if NumberFormula._isCardinalNumber(strNewNumber):
            strNewNumber =  Number.convertNumberIntoLetters(strNewNumber, ordinal=bOrdinal)
        elif NumberFormula._isRomanNumber(strNewNumber):
            #Roman to cardinal
            strNewNumber = strNewNumber.encode('utf-8')
            cardinalNumber = fromRoman(strNewNumber)
            #Digits to ordinal
            strNewNumber =  Number.convertNumberIntoLetters(cardinalNumber, ordinal=bOrdinal)
        else:
            #Original word is kept
            strNewNumber = strNumber
            ending = u""

        #Already included in convertNumberIntLetters        
        if ending == u"e":
          ending = u""

        return strNewNumber + ending

    @staticmethod
    def _getOrdinalEnding(strNumber, wordsList, indice):
        """Given a cardinal number and its context,
           determine ending.

           This only fix part of all the cases.

           i.e. das zeite Dezember
                am zweiten Dezember
        """
        #Default to nothing
        ending = u""

        #Check for am 2. December
        enRule = Rule(Pattern(NumberFormula.ORDINALNUMBERREGEX.pattern, 
                       u"(an|am|im|de[nmrs]|vo[nm]|ein[nmrs]|jede[nmrs]"+\
                       u"|solche[nmrs]|jene[nmrs]|welche[nmrs])", None,-1,1))

        if enRule.doesApply(wordsList, indice) and \
            enRule.match(wordsList, indice):
            ending = u"n"

        #Check for am 2. December
        eRule = Rule(Pattern(NumberFormula.ORDINALNUMBERREGEX.pattern, 
                       u"(der|die|das|jede"+\
                       u"|solche|jene|welche)", None,-1,1))

        if eRule.doesApply(wordsList, indice) and \
            eRule.match(wordsList, indice):
            ending = u"e"

        return ending

    @staticmethod
    def _decimal2word(strNumber):
        """Convert a decimal number to a written
           word.

           param strNumber: an utf-8 decimal number
           return a 'written' decimal number
        """
        strNumber = u" komma ".join(re.split("[,]",strNumber))
        strNumber = u" punkt ".join(re.split("[.]",strNumber))

        tokenList = []
        for w in re.split(SPACEPATTERN, strNumber):
            w = w.strip()
            if NumberFormula._isCardinalNumber(w):
                w = NumberFormula._cardinal2word(w)
            tokenList.append(w)

        return u" ".join(tokenList)

    @staticmethod
    def _roman2word(strNumber):
        """Convert a roman number to a written
           word.

           param strNumber: an utf-8 roman number
           return a 'written' roman number
        """
        strNumber = strNumber.encode('utf-8')
        cardinalNumber = fromRoman(strNumber)
        return NumberFormula._cardinal2word(cardinalNumber)

    @staticmethod
    def _isCardinalNumber(strWord):
        """Check if 'strWord' is a cardinal number.

           param strWord: an utf-8 encoded words
           return True or False
        """
        return NumberFormula.CARDINALNUMBERREGEX.match(strWord) != None

    @staticmethod
    def _isTransitionNumber(strWord):
        """Check if 'strWord' is a transition number.

           param strWord: an utf-8 encoded words
           currently return False only
        """
        return False

    @staticmethod
    def _isOrdinalNumber(strWord):
        """Check if 'strWord' is an ordinal number.


           param strWord: an utf-8 encoded words
           return True or False
        """
        return NumberFormula.ORDINALNUMBERREGEX.match(strWord) != None

    @staticmethod
    def _isDecimalNumber(strWord):
        """Check if 'strWord' is a decimal number.

           A decimal number contains a decimal symbol
           that can be a comma or a dot.

           param strWord: an utf-8 encoded words
           return True or False
        """
        return NumberFormula.DECIMALNUMBERREGEX.match(strWord) != None

    @staticmethod
    def _isRomanNumber(strWord):
        """Check if 'strWord' is a roman number.

           A roman number can be followed by the
           following suffixes: er|re|e|eme|ème.

           Int that case they are ordial numbers

           param strWord: an utf-8 encoded words
           return True or False
        """
        return NumberFormula.ROMANNUMBERREGEX.match(strWord) != None
