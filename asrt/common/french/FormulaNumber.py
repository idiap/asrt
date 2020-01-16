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

import logging
import re
from num2words import num2words
from roman import fromRoman
from asrt.common.AsrtUtility import convertNumber
from asrt.common.AsrtConstants import SPACEPATTERN, TRANSITIONNUMBERS
from asrt.config.AsrtConfig import FRENCH


class NumberFormula():
    """A set of rules to 'unformat' formatted numbers.
    """

    logger = logging.getLogger("Asrt.NumberFormula")

    THOUSANDSEPARATOR = "'"

    HASNUMBERREGEX = re.compile("([0-9]|I|V|X|L|C|D|M)+", flags=re.UNICODE)
    CARDINALNUMBERREGEX = re.compile("[0-9]+$", flags=re.UNICODE)
    TRANSITIONNUMBERREGEX = re.compile("([1-9]|10)[.]( |$)", flags=re.UNICODE)
    ORDINALNUMBERREGEX = re.compile(
        "(1er|1re|1ère|[0-9]+e|[0-9]+ème|Ier|Ire|Ière|[IVXLCDM]+ème|[IVXLCDM]{2,}e)$", flags=re.UNICODE)
    DECIMALNUMBERREGEX = re.compile("[0-9,.]+[0-9,.]*$", flags=re.UNICODE)
    ROMANNUMBERREGEX = re.compile("[IVXLCDM]{2,}$", flags=re.UNICODE)

    ##################
    # Public interface
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
    # Implementation
    #
    @staticmethod
    def _normalizeNumber(strWord):
        """Remove tousand separator.

           param strWord: an utf-8 encoded words
           return an utf-8 encoded string
        """
        strWord = strWord.replace(NumberFormula.THOUSANDSEPARATOR, "")

        # Case when there is a full stop, comma
        # after a number
        if strWord.endswith((".", ",")):
            strWord = strWord[:-1]

        return strWord

    @staticmethod
    def _cardinal2word(strNumber):
        """Convert a cardinal number to a written
           word.

           param strNumber: an utf-8 cardinal number
           return a 'written' cardinal number
        """
        strNumber = num2words(int(strNumber), lang='fr')
        return strNumber.replace("-", " ")

    @staticmethod
    def _transition2word(strNumber):
        """Convert an transition number to a written
           word.

           param strNumber: an utf-8 transition number
           return a 'written' transition number
        """
        # Only number from 1-10
        if strNumber not in TRANSITIONNUMBERS[FRENCH]:
            return strNumber

        return TRANSITIONNUMBERS[FRENCH][strNumber]

    @staticmethod
    def _ordinal2word(wordsList, indice):
        """Convert an ordinal number to a written
           word.

           i.e. 1er --> premier

           param strNumber: an utf-8 ordinal number
           return a 'written' ordinal number
        """
        strNumber = NumberFormula._normalizeNumber(wordsList[indice])
        if strNumber.encode('utf-8') == "1ère".encode('utf-8'):
            return "première"

        strNewNumber = re.sub("[erèm]", "", strNumber)
        if NumberFormula._isCardinalNumber(strNewNumber):
            strNewNumber = num2words(
                int(strNewNumber), ordinal=True, lang='fr')
        elif NumberFormula._isRomanNumber(strNewNumber):
            # Roman to cardinal
            strNewNumber = strNewNumber
            cardinalNumber = fromRoman(strNewNumber)
            # Digits to ordinal
            strNewNumber = num2words(cardinalNumber, ordinal=True, lang='fr')
        else:
            strNewNumber = strNumber

        strNewNumber = re.sub(r'vingtsi', 'vingti', strNewNumber)
        strNewNumber = re.sub(r'centsi', 'centi', strNewNumber)
        strNewNumber = re.sub(r'millionsi', 'millioni', strNewNumber)
        strNewNumber = re.sub(r'milliardsi', 'milliardi', strNewNumber)

        return strNewNumber

    @staticmethod
    def _decimal2word(strNumber):
        """Convert a decimal number to a written
           word.

           param strNumber: an utf-8 decimal number
           return a 'written' decimal number
        """
        strNumber = " virgule ".join(re.split("[,]", strNumber))
        strNumber = " point ".join(re.split("[.]", strNumber))

        tokenList = []
        for w in re.split(SPACEPATTERN, strNumber):
            w = w.strip()
            if NumberFormula._isCardinalNumber(w):
                w = NumberFormula._cardinal2word(w)
            tokenList.append(w)

        return " ".join(tokenList)

    @staticmethod
    def _roman2word(strNumber):
        """Convert a roman number to a written
           word.

           param strNumber: an utf-8 roman number
           return a 'written' roman number
        """
        strNumber = strNumber
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
        """Check if 'strWord' is an transition number.

           Adverb numbers are:
              premièrement
              deuxièmement
              ...
              neuvièmement
        """
        return NumberFormula.TRANSITIONNUMBERREGEX.match(strWord) != None \
            and NumberFormula.THOUSANDSEPARATOR not in strWord

    @staticmethod
    def _isOrdinalNumber(strWord):
        """Check if 'strWord' is an ordinal number.

           i.e. 1er, 2e, 2ème
           see http://french.about.com/od/vocabulary/a/romannumerals.htm
               https://francais.lingolia.com/fr/vocabulaire/nombres-date-et-heure/les-nombres-ordinaux

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
