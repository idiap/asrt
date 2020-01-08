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

import unittest
from asrt.common.german.Number import Number


class NumberUnitTest(unittest.TestCase):

    ###############
    # Unit tests
    #
    def testCardinalConvertNumberIntoLetters(self):
        test = [(u'1', u'eins'),
                (u'12', u'zwölf'),
                (u'15', u'fünfzehn'),
                (u'51', u'ein und fünfzig'),
                (u'69', u'neun und sechzig'),
                (u'76', u'sechs und siebzig'),
                (u'100', u'hundert'),
                (u'101', u'hundert eins'),
                (u'134', u'hundert vier und dreissig'),
                (u'318', u'drei hundert achtzehn'),
                (u'1000', u'tausend'),
                (u'1004', u'tausend vier'),
                (u'1504', u'tausend fünf hundert vier'),
                (u'2000', u'zwei tausend'),
                (u'589217', u'fünf hundert neun und achtzig tausend zwei hundert siebzehn'),
                (u'1000000', u'ein million'),
                (u'100000000', u'hundert millionen')]

        for digit, letters in test:
            strLetters = Number.convertNumberIntoLetters(digit)
            self.assertEquals(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))

    def testOrdinalConvertNumberIntoLetters(self):
        test = [(u'1', u'erste'),
                (u'3', u'dritte'),
                (u'8', u'achte'),
                (u'12', u'zwölfte'),
                (u'15', u'fünfzehnte'),
                (u'51', u'ein und fünfzigste'),
                (u'69', u'neun und sechzigste'),
                (u'76', u'sechs und siebzigste'),
                (u'100', u'hundertste'),
                (u'101', u'hundert erste'),
                (u'134', u'hundert vier und dreissigste'),
                (u'318', u'drei hundert achtzehnte'),
                (u'1000', u'tausendste'),
                (u'1004', u'tausend vierte'),
                (u'1504', u'tausend fünf hundert vierte'),
                (u'2000', u'zwei tausendste'),
                (u'134', u'hundert vier und dreissigste'),
                (u'589217', u'fünf hundert neun und achtzig tausend zwei hundert siebzehnte'),
                (u'017688088605', u'siebzehn billionen sechs hundert acht und achtzig millionen acht und achtzig tausend sechs hundert fünfte')]

        for digit, letters in test:
            strLetters = Number.convertNumberIntoLetters(digit, False, True)
            self.assertEquals(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))

    def testConvertDecimalNumberIntoLetters(self):
        test = [(u'1,4', u'eins komma vier'),
                (u'134,2', u'hundert vier und dreissig komma zwei'),
                (u'589217,346', u'fünf hundert neun und achtzig tausend zwei hundert siebzehn komma drei hundert sechs und vierzig')]

        for digit, letters in test:
            strLetters = Number.convertDecimalNumberIntoLetters(digit)
            self.assertEquals(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))
