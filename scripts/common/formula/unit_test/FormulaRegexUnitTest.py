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
__version__ = "Revision: 1.0 "
__date__ = "Date: 2015/09"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest

from formula.FormulaRegularExpression import RegularExpressionFormula
from RegularExpressionList import RegexList
from AsrtConstants import CONTRACTIONPREFIXELIST, ACRONYMREGEXLIST
from AsrtConstants import DATEREGEXLIST, APOSTHROPHELIST

class TestFormulaRegex(unittest.TestCase):
    def setUp(self):
        print ""

    def verifyEqual(self, testList, f, languageId):
        for t, gt in testList:
            resultString = f.apply(t, languageId, False)
            self.assertEquals(gt.encode('utf-8'), resultString.encode('utf-8'))

    ############
    #Tests
    #
    def testContractionPrefixes(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(CONTRACTIONPREFIXELIST))
        
        for p, s, t, i, c in CONTRACTIONPREFIXELIST:
            if not p.find("gr1"):
                resultString = f.apply(p, 1, False)
                self.assertEquals(s.encode('utf-8'), 
                              resultString.encode('utf-8'))

        testList = [(ur"d une",ur"d' une"),(ur"j' ai",ur"j' ai"), (ur"l' y ",ur"l' y "),
                    (ur"m' a",ur"m' a"), (ur"n' est",ur"n' est"),(ur"n' a",ur"n' a"),
                    (ur"d' y",ur"d' y"),(ur"c' en",ur"c' en"), (ur"qu' y",ur"qu' y"),
                    (ur"qu' en",ur"qu' en"), (ur"-t-on",ur" -t-on")]

        for p, gt in testList:
            resultString = f.apply(p, 1, False)
            self.assertEquals(gt.encode('utf-8'), 
                              resultString.encode('utf-8'))

    def testAcronyms(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(ACRONYMREGEXLIST))

        testList = [(u"ADG SPO PS",u"a. d. g. s. p. o. p. s."),
                    (u"ADG SPO PS PDCC",u"a. d. g. s. p. o. p. s. p. d. c. c."),
                    (u"A ADG SPO PS PDCCC",u"A a. d. g. s. p. o. p. s. p. d. c. c. c."),]

        self.verifyEqual(testList, f, 0)

    def testDates(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(DATEREGEXLIST))

        testList = [(u"01.01.2015",u"01 01 2015"),
                    (u"01/01/2015",u"01 01 2015"),
                    (u"01.01.15",u"01 01 15"),]

        self.verifyEqual(testList, f, 0)


    def testApostrophe(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(APOSTHROPHELIST))

        testList = [(u"d'avant",u"d' avant")]

        self.verifyEqual(testList, f, 1)
