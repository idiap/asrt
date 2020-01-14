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
from asrt.common.french.FormulaNumber import NumberFormula
from asrt.common.AsrtUtility import hasNumber


class FormulaNumberUnitTest(unittest.TestCase):

    testDict = {"cardinal": [("10", "dix"), ("25", "vingt cinq"), ("1416000", "un million quatre cent seize mille")],
                "transition": [("1.", "premièrement"), ("10.", "dixièmement")],
                "ordinal": [("1er", "premier"), ("1ère", "première"), ("2ème", "deuxième"),
                            ("80ème", "quatre-vingtième"), ("400ème",
                                                            "quatre centième"),
                            ("380ème", "trois cent quatre-vingtième"), ("4000000ème",
                                                                        "quatre millionième"),
                            ("XXVème", "vingt-cinquième"), ("XXème", "vingtième"),
                            ("XXIIIe", "vingt-troisième")],
                "decimal": [("2,5", "deux virgule cinq"), ("2.5,3", "deux point cinq virgule trois")],
                "roman": [("XXIII", "vingt trois"), ("XX", "vingt")],
                "all": [("1ab", "1ab"), ("ab", "ab"),
                        ("le 25 mars 2015 2.5 XXème",
                         "le vingt cinq mars deux mille quinze deux point cinq vingtième"),
                        ("le 25.", "le vingt cinq"),
                        ("le 25.5.", "le vingt cinq point cinq"),
                        ("14 alinéa 1, some text",
                         "quatorze alinéa un some text"),
                        ("l'article 12,", "l'article douze"),
                        ("dans le XXIIIe siècle",
                         "dans le vingt-troisième siècle"),
                        ("Ce matin", "Ce matin"),
                        ("1'416'000", "un million quatre cent seize mille"),
                        ("Le matin", "Le matin")]
                }

    #################
    # Implementation
    #
    def evaluateListValues(self, testList, callback):
        for t, gt in testList:
            r = callback(t)
            self.assertEqual(gt, r)

    #################
    # Unit tests
    #
    def test_isCardinal(self):
        testList = [("2", True), ("123", True), ("123.", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isCardinalNumber(t), gt, t)

    def test_isTransition(self):
        testList = [("1.", True), ("10.", True), ("11.", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isTransitionNumber(t), gt, t)

    def test_isOrdinal(self):
        testList = [("1er", True), ("1re", True), ("1ère", True), ("2e", True), ("2ème", True),
                    ("Ier", True), ("XIIème", True)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isOrdinalNumber(t), gt, t)

    def test_isDecimal(self):
        testList = [("2.5", True), ("2,5", True),
                    ("2,5,3", True), ("2-5", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isDecimalNumber(t), gt, t)

    def test_isRoman(self):
        testList = [("V", False), ("XII", True), ("La", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isRomanNumber(t), gt, t)

    def test_hasNumber(self):
        testList = [("12", True), ("1ab", True), ("ab22", True), ("Xab", True),
                    ("xab", False), ("a1ab", True), ("il a 1'416'000 francs", True)]

        for t, gt in testList:
            self.assertEqual(hasNumber(NumberFormula, t), gt, t)

    def test_normalizeNumber(self):
        testList = [("50'000", "50000"), ("550'000'000",
                                          "550000000"), ("1'416'000", "1416000")]
        self.evaluateListValues(testList, NumberFormula._normalizeNumber)

    def test_cardinal2word(self):
        testList = self.testDict["cardinal"]
        self.evaluateListValues(testList, NumberFormula._cardinal2word)

    def test_transition2word(self):
        testList = self.testDict["transition"]
        self.evaluateListValues(testList, NumberFormula._transition2word)

    def test_ordinal2word(self):
        testList = self.testDict["ordinal"]
        for i, (t, gt) in enumerate(testList):
            r = NumberFormula._ordinal2word([t], 0)
            self.assertEqual(gt, r,
                             "%s is not %s" % (r, gt))

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
