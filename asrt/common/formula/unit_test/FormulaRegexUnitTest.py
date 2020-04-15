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
__version__ = "Revision: 1.0 "
__date__ = "Date: 2015/09"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import unittest
import re

from asrt.common.formula.FormulaRegularExpression import RegularExpressionFormula
from asrt.common.RegularExpressionList import RegexList
from asrt.common.AsrtConstants import CONTRACTIONPREFIXELIST, ACRONYMREGEXLIST
from asrt.common.AsrtConstants import DATEREGEXLIST, APOSTHROPHELIST, ACRONYMDELIMITER

class TestFormulaRegex(unittest.TestCase):
    def setUp(self):
        print("")

    def verifyEqual(self, testList, f, languageId):
        for t, gt in testList:
            resultString = f.apply(t, languageId, False)
            self.assertEqual(gt.encode('utf-8'), resultString.encode('utf-8'))

    ############
    #Tests
    #
    def testContractionPrefixes(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(CONTRACTIONPREFIXELIST))
        
        for p, s, t, i, c in CONTRACTIONPREFIXELIST:
            if not p.find("gr1"):
                resultString = f.apply(p, 1, False)
                self.assertEqual(s.encode('utf-8'), 
                              resultString.encode('utf-8'))

        testList = [(r"d une",r"d' une"),(r"j' ai",r"j' ai"), (r"l' y ",r"l' y "),
                    (r"m' a",r"m' a"), (r"n' est",r"n' est"),(r"n' a",r"n' a"),
                    (r"d' y",r"d' y"),(r"c' en",r"c' en"), (r"qu' y",r"qu' y"),
                    (r"qu' en",r"qu' en"), (r"-t-on",r" -t-on")]

        for p, gt in testList:
            resultString = f.apply(p, 1, False)
            self.assertEqual(gt.encode('utf-8'), 
                              resultString.encode('utf-8'))

    def testAcronyms(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(ACRONYMREGEXLIST))

        testList = [("ADG SPO PS","a. d. g.  s. p. o.  p. s."),
                    ("ADG SPO PS PDCC","a. d. g.  s. p. o.  p. s.  p. d. c. c."),
                    ("A ADG SPO PS PDCCC","A a. d. g.  s. p. o.  p. s.  p. d. c. c. c."),
                    ("ABCDs ABCs ABs","a. b. c. d. s.  a. b. c. s.  a. b. s.")]

        for t, gt in testList:
            resultString = f.apply(t, 0, False)
            resultString = re.sub(ACRONYMDELIMITER, "", resultString, flags=re.UNICODE)
            self.assertEqual(gt.encode('utf-8'), resultString.encode('utf-8'))

    def testDates(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(DATEREGEXLIST))

        testList = [("01.01.2015","01 01 2015"),
                    ("01/01/2015","01 01 2015"),
                    ("01.01.15","01 01 15"),]

        self.verifyEqual(testList, f, 0)


    def testApostrophe(self):
        f = RegularExpressionFormula(None,
                RegexList.removeComments(APOSTHROPHELIST))

        testList = [("d'avant","d' avant")]

        self.verifyEqual(testList, f, 1)

    def testRegexTypes(self):
        TYPEREGEXLIST = [(r"ADG", r"a. d. g.",r"6",r"0",r"")]

        TESTLIST = [("ADG","a. d. g."),
                    ("ADG/LA","ADG/LA"),
                    ("a ADG b","a a. d. g. b"),
                    ("l ADG ","l a. d. g. "),
                    ("l'ADG'","l'a. d. g.'"),
                    ("\"ADG\"","\"a. d. g.\""),
                    ("\"ADG","\"a. d. g."),
                    ("e-ADG-","e-ADG-"),
                    ("l'ADG,","l'a. d. g.,"),
                    ("l'ADG.","l'a. d. g.."),
                    ("l'ADG?","l'a. d. g.?"),
                    ("l'ADG!","l'a. d. g.!"),
                    ("l'ADG;","l'a. d. g.;"),
                    ("l'ADG:","l'a. d. g.:")]

        f = RegularExpressionFormula(None,
                RegexList.removeComments(TYPEREGEXLIST))
        
        for t, gt in TESTLIST:
            r = f.apply(t, 0)
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))
