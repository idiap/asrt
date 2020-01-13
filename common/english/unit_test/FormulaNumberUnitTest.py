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

import unittest
from common.english.FormulaNumber import NumberFormula
from common.AsrtUtility import hasNumber

class FormulaNumberUnitTest(unittest.TestCase):

    testDict = { "cardinal"   : [("10","ten"),("25","twenty five"),("1416000","one million, four hundred and sixteen thousand")],
                 "transition" : [("1.","first"),("10.","tenth")],
                 "ordinal"    : [("1st","first"),("2nd","second"),("23rd","twenty-third"),("80th","eightieth"),
                                 ("XXth","twentieth"),("XXIIIrd","twenty-third")],
                 "roman"      : [("XXIII","twenty-three"), ("XX","twenty")],
                 "decimal"    : [("2.5","two point five"), ("2.53","two point fifty three"),
                                 ("2.55","two point fifty five")],
                 "all"        : [("1ab","1ab"),("ab","ab"),
                                 ("the 25 march 2015 2.5 XXth","the twenty five march two thousand and fifteen two point five twentieth"),
                                 ("the 25.","the twenty five"),
                                 ("the 25.5.","the twenty five point five"),
                                 ("14 paragraph 1, some text","fourteen paragraph one some text"),
                                 ("the article 12,","the article twelve"),
                                 ("in the XXIIIrd century", "in the twenty-third century"),
                                 ("This morning", "This morning"),
                                 ("1,416,000","one million, four hundred and sixteen thousand"),
                                 ("2.5,3","two point fifty three"),
                                 ("2,53","two hundred and fifty three"),
                                 ("object 1 5", "object one five")]
    }


    #################
    # Implementation
    #
    def evaluateListValues(self, testList, callback):
        for t, gt in testList:
            r = callback(t).encode('utf-8')
            self.assertEqual(gt.encode('utf-8'), r)

    #################
    # Unit tests
    #
    def test_normalizeNumber(self):
        testList = [("2,5","25"), # Notation error, comma is for thousand
                    ("123,","123"), ("123.","123"),
                    ("50,000","50000"),("550,000,000","550000000"),("1,416,000","1416000")]

        for t, gt in testList:
            self.assertEqual(NumberFormula._normalizeNumber(t), gt, t.encode('utf-8'))

    def test_isCardinal(self):
        testList = [("2",True),("123",True), ("123.",False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isCardinalNumber(t), gt, t.encode('utf-8'))

    def test_isTransition(self):
        testList = [("1.",True),("10.",True), ("11.",False)]

        for t, gt in testList:
          self.assertEqual(NumberFormula._isTransitionNumber(t), gt, t.encode('utf-8'))

    def test_isOrdinal(self):
        testList = [("1st",True),("2nd",True),("3rd",True),("4th",True)]
        for t, gt in testList:
            self.assertEqual(NumberFormula._isOrdinalNumber(t), gt, t.encode('utf-8'))

    def test_isDecimal(self):
        testList = [("2.5",True), ("2,5",False),("2.5,3",False), ("2-5",False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isDecimalNumber(t), gt, t.encode('utf-8'))

    def test_isRoman(self):
        testList = [("LV",True), ("XII",True), ("La", False)]

        for t, gt in testList:
            self.assertEqual(NumberFormula._isRomanNumber(t), gt, t.encode('utf-8'))

    def test_hasNumber(self):
        testList = [("12",True), ("1ab",True),("ab22",True), ("Xab",True),
                    ("xab",False), ("a1ab",True), ("he has 1'416'000 euro",True)]

        for t, gt in testList:
            self.assertEqual(hasNumber(NumberFormula,t), gt, t.encode('utf-8'))

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
            #print "--> Testing %s " % k
            testList = self.testDict[k]
            self.evaluateListValues(testList, f.apply)
