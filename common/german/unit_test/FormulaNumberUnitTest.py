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
from asrt.common.german.FormulaNumber import NumberFormula
from asrt.common.AsrtUtility import hasNumber


class FormulaNumberUnitTest(unittest.TestCase):

    testDict = {"cardinal": [("10", "zehn"), ("25", "fünf und zwanzig")],
                "ordinal": [("der 1.", "der erste"), ("der 2.", "der zweite"),
                            ("der XXV.", "der fünf und zwanzigste"), ("der XX.", "der zwanzigste")],
                "decimal": [("2,5", "zwei komma fünf"), ("2.5,3", "zwei punkt fünf komma drei")],
                "roman": [("XX", "zwanzig"), ("II", "zwei")],
                "all": [("1ab", "1ab"), ("ab", "ab"),
                        ("die 25 März 2015 2.5 die XX.",
                         "die fünf und zwanzig März zwei tausend fünfzehn zwei punkt fünf die zwanzigste"),
                        ("am 21. dezember 2011",
                         "am ein und zwanzigsten dezember zwei tausend elf"),
                        ("das 21.", "das ein und zwanzigste"), ("2,", "zwei"),
                        ("das 2.,", "das zweite"), ("das 2..", "das zweite"),
                        ("2,", "zwei"),
                        ("am 2. Dezember", "am zweiten Dezember")]
                }

    #################
    # Implementation
    #
    def evaluateListValues(self, testList, callback):
        for t, gt in testList:
            r = callback(t).encode('utf-8')
            self.assertEqual(gt.encode('utf-8'), r,
                              "%s is not %s" % (r, gt.encode('utf-8')))

    #################
    # Unit tests
    #
    def test_isCardinal(self):
        testList = [("2", True), ("123", True), ("123.", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isCardinalNumber(
                t), gt, t.encode('utf-8'))

    def test_isOrdinal(self):
        testList = [("1.", True), ("3.", True), ("8.", True), ("2.", True), ("10.", True),
                    ("I.", False), ("XII.", True), ("017688088605", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isOrdinalNumber(
                t), gt, t.encode('utf-8'))

    def test_isDecimal(self):
        testList = [("2.5", True), ("2,5", True),
                    ("2,5,3", True), ("2-5", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isDecimalNumber(
                t), gt, t.encode('utf-8'))

    def test_isRoman(self):
        testList = [("V", False), ("XII", True)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isRomanNumber(t),
                              gt, t.encode('utf-8'))

    def test_hasNumber(self):
        testList = [("12", True), ("1ab", True), ("ab22", True), ("Xab", True),
                    ("xab", False), ("a1ab", True)]

        for t, gt in testList:
            self.assertEqual(hasNumber(NumberFormula, t),
                              gt, t.encode('utf-8'))

    def test_normalizeNumber(self):
        testList = [("50'000", "50000"), ("550'000'000", "550000000")]
        self.evaluateListValues(testList, NumberFormula._normalizeNumber)

    def test_cardinal2word(self):
        testList = self.testDict["cardinal"]
        self.evaluateListValues(testList, NumberFormula._cardinal2word)

    def testOrdinal2word(self):
        testList = self.testDict["ordinal"]
        for i, (t, gt) in enumerate(testList):
            tList = t.split(" ")
            gt = " ".join(gt.split(" ")[1:])
            r = NumberFormula._ordinal2word(tList, 1)
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'),
                              "%s is not %s" % (r.encode('utf-8'), gt.encode('utf-8')))

    def test_decimal2word(self):
        testList = self.testDict["decimal"]
        self.evaluateListValues(testList, NumberFormula._decimal2word)

    def test_roman2word(self):
        testList = self.testDict["roman"]
        self.evaluateListValues(testList, NumberFormula._roman2word)

    def test_apply(self):
        f = NumberFormula()

        for k in list(self.testDict.keys()):
            # print "Testing %s " % k
            testList = self.testDict[k]
            self.evaluateListValues(testList, f.apply)
