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
__date__ = "Date: 2016/12"
__copyright__ = "Copyright (c) 2016 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging, re
from asrt.common.AsrtUtility import convertNumber

class NumberFormula():
    """A set of rules to 'unformat' formatted numbers.
    """

    logger                  = logging.getLogger("Asrt.english.NumberFormula")

    THOUSANDSEPARATOR       = u"'"

    HASNUMBERREGEX          = re.compile(u"([0-9]|I|V|X|L|C|D|M)+", flags=re.UNICODE)
    CARDINALNUMBERREGEX     = re.compile(u"[0-9]+$", flags=re.UNICODE)
    TRANSITIONNUMBERREGEX   = re.compile(u"([1-9]|10)[.]( |$)", flags=re.UNICODE)
    ORDINALNUMBERREGEX      = re.compile(u"(1er|1re|1ère|[0-9]+e|[0-9]+ème|Ier|Ire|Ière|[IVXLCDM]+ème|[IVXLCDM]{2,}e)$", flags=re.UNICODE)
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
        pass

    @staticmethod
    def _cardinal2word(strNumber):
        """Convert a cardinal number to a written
           word.

           param strNumber: an utf-8 cardinal number
           return a 'written' cardinal number
        """
        pass

    @staticmethod
    def _transition2word(strNumber):
        """Convert an transition number to a written
           word.

           param strNumber: an utf-8 transition number
           return a 'written' transition number
        """
        pass

    @staticmethod
    def _ordinal2word(wordsList, indice):
        """Convert an ordinal number to a written
           word.

           i.e. 1er --> premier

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
        pass

    @staticmethod
    def _isTransitionNumber(strWord):
        """Check if 'strWord' is an transition number.

           Adverb numbers are:
              premièrement
              deuxièmement
              ...
              neuvièmement
        """
        pass

    @staticmethod
    def _isOrdinalNumber(strWord):
        """Check if 'strWord' is an ordinal number.

           i.e. 1er, 2e, 2ème

           param strWord: an utf-8 encoded words
           return True or False
        """
        pass

    @staticmethod
    def _isDecimalNumber(strWord):
        """Check if 'strWord' is a decimal number.

           A decimal number contains a decimal symbol
           that can be a comma or a dot.

           param strWord: an utf-8 encoded words
           return True or False
        """
        pass

    @staticmethod
    def _isRomanNumber(strWord):
        """Check if 'strWord' is a roman number.

           A roman number can be followed by the
           following suffixes: er|re|e|eme|ème.

           Int that case they are ordial numbers

           param strWord: an utf-8 encoded words
           return True or False
        """
        pass
