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
sys.path.append(scriptsDir + "/..")

import logging, re
from FormulaLMPreparation import LMPreparationFormula

class NumberFormula():
    """Various number formats expansion.
    """
    logger                  = logging.getLogger("Asrt.NumberFormula")

    CARDINALNUMBERREGEX     = re.compile(u"[0-9]+$", flags=re.UNICODE)
    ORDINALNUMBERREGEX      = re.compile(u"(1er|1re|[0-9]+e||[0-9]+ème)$", flags=re.UNICODE)
    DECIMALNUMBERREGEX      = re.compile(u"[0-9]+[,.][0-9]+$", flags=re.UNICODE)
    ROMANNUMBERREGEX        = re.compile(u"(I|V|X|L|C|D|M)+(er|re|e|eme|ème)$", flags=re.UNICODE)

    ##################
    #Public interface
    #
    def apply(self, strText):
        """Apply formula to numbers.
           
           Numbers cateories are:
             - Decimal numbers
             - Ordinal numbers 
             - Cardinal numbers
             - Roman numbers

           param strText: an utf-8 encoded string
           return an utf-8 encoded string 
        """
        wordsList = re.split(LMPreparationFormula.SPACEREGEX, strText, flags=re.UNICODE)

        newWordsList = []
        for w in wordsList:
            if self._isCardinalNumber(w):
                pass
            elif self._isOrdinalNumber(w):
                pass
            elif self._isDecimalNumber(w):
                pass
            elif self._isRomanNumber(w):
                pass
            else:
                newWordsList.append(w)

        return u" ".join(newWordsList)

    ##################
    #Implementation
    #
    @staticmethod
    def _cardinal2word(strNumber):
        """Convert a cardinal number to a written
           word.

           param strNumber: an utf-8 cardinal number
           return a 'written' cardinal number
        """
        pass

    @staticmethod
    def _ordinal2word(strNumber):
        """Convert an ordinal number to a written
           word.

           param strNumber: an utf-8 ordinal number
           return a 'written' ordinal number
        """
        pass

    @staticmethod
    def _decimal2word(strNumber):
        """Convert a decimal number to a written
           word.

           param strNumber: an utf-8 decimal number
           return a 'written' decimal number
        """
        pass

    @staticmethod
    def _roman2word(strNumber):
        """Convert a roman number to a written
           word.

           param strNumber: an utf-8 roman number
           return a 'written' roman number
        """
        pass

    @staticmethod
    def _isCardinalNumber(strWord):
        """Check if 'strWord' is a cardinal number.

           param strWord: an utf-8 encoded words
           return True or False
        """
        return NumberFormula.CARDINALNUMBERREGEX.match(strWord) != None

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
