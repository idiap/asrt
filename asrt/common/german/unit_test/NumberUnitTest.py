#!/usr/bin/env python3
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
        test = [('1', 'eins'),
                ('12', 'zwölf'),
                ('15', 'fünfzehn'),
                ('51', 'ein und fünfzig'),
                ('69', 'neun und sechzig'),
                ('76', 'sechs und siebzig'),
                ('100', 'hundert'),
                ('101', 'hundert eins'),
                ('134', 'hundert vier und dreissig'),
                ('318', 'drei hundert achtzehn'),
                ('1000', 'tausend'),
                ('1004', 'tausend vier'),
                ('1504', 'tausend fünf hundert vier'),
                ('2000', 'zwei tausend'),
                ('589217', 'fünf hundert neun und achtzig tausend zwei hundert siebzehn'),
                ('1000000', 'ein million'),
                ('100000000', 'hundert millionen')]

        for digit, letters in test:
            strLetters = Number.convertNumberIntoLetters(digit)
            self.assertEqual(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))

    def testOrdinalConvertNumberIntoLetters(self):
        test = [('1', 'erste'),
                ('3', 'dritte'),
                ('8', 'achte'),
                ('12', 'zwölfte'),
                ('15', 'fünfzehnte'),
                ('51', 'ein und fünfzigste'),
                ('69', 'neun und sechzigste'),
                ('76', 'sechs und siebzigste'),
                ('100', 'hundertste'),
                ('101', 'hundert erste'),
                ('134', 'hundert vier und dreissigste'),
                ('318', 'drei hundert achtzehnte'),
                ('1000', 'tausendste'),
                ('1004', 'tausend vierte'),
                ('1504', 'tausend fünf hundert vierte'),
                ('2000', 'zwei tausendste'),
                ('134', 'hundert vier und dreissigste'),
                ('589217', 'fünf hundert neun und achtzig tausend zwei hundert siebzehnte'),
                ('017688088605', 'siebzehn billionen sechs hundert acht und achtzig millionen acht und achtzig tausend sechs hundert fünfte')]

        for digit, letters in test:
            strLetters = Number.convertNumberIntoLetters(digit, False, True)
            self.assertEqual(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))

    def testConvertDecimalNumberIntoLetters(self):
        test = [('1,4', 'eins komma vier'),
                ('134,2', 'hundert vier und dreissig komma zwei'),
                ('589217,346', 'fünf hundert neun und achtzig tausend zwei hundert siebzehn komma drei hundert sechs und vierzig')]

        for digit, letters in test:
            strLetters = Number.convertDecimalNumberIntoLetters(digit)
            self.assertEqual(letters, strLetters, "Error with: '%s' --> '%s' " %
                              (letters.encode('utf-8'), strLetters.encode('utf-8')))
