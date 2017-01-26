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

    testDict = { "cardinal"   : [(u"10",u"ten"),(u"25",u"twenty five"),(u"1416000",u"one million, four hundred and sixteen thousand")],
                 "transition" : [(u"1.",u"first"),(u"10.",u"tenth")],
                 "ordinal"    : [(u"1st",u"first"),(u"2nd",u"second"),(u"23rd",u"twenty-third"),(u"80th",u"eightieth"),
                                 (u"XXth",u"twentieth"),(u"XXIIIrd",u"twenty-third")],
                 "roman"      : [(u"XXIII",u"twenty-three"), (u"XX",u"twenty")],
                 "decimal"    : [(u"2.5",u"two point five"), (u"2.53",u"two point fifty three")],
                 "all"        : [(u"1ab",u"1ab"),(u"ab",u"ab"),
                                 (u"the 25 march 2015 2.5 XXth",u"the twenty five march two thousand and fifteen two point five twentieth"),
                                 (u"the 25.",u"the twenty five"),
                                 (u"the 25.5.",u"the twenty five point five"),
                                 (u"14 paragraph 1, some text",u"fourteen paragraph one some text"),
                                 (u"the article 12,",u"the article twelve"),
                                 (u"in the XXIIIrd century", u"in the twenty-third century"),
                                 (u"This morning", u"This morning"),
                                 (u"1,416,000",u"one million, four hundred and sixteen thousand"),
                                 (u"2.5,3",u"two point fifty three"),
                                 (u"2,53",u"two hundred and fifty three"),
                                 (u"object 1 5", u"object one five")]
    }


    #################
    # Implementation
    #
    def evaluateListValues(self, testList, callback):
        for t, gt in testList:
            r = callback(t).encode('utf-8')
            self.assertEquals(gt.encode('utf-8'), r)

    #################
    # Unit tests
    #
    def test_normalizeNumber(self):
        testList = [(u"2,5",u"25"), # Notation error, comma is for thousand
                    (u"123,",u"123"), (u"123.",u"123"),
                    (u"50,000",u"50000"),(u"550,000,000",u"550000000"),(u"1,416,000",u"1416000")]

        for t, gt in testList:
            self.assertEquals(NumberFormula._normalizeNumber(t), gt, t.encode('utf-8'))

    def test_isCardinal(self):
        testList = [(u"2",True),(u"123",True), (u"123.",False)]

        for t, gt in testList:
            self.assertEquals(NumberFormula._isCardinalNumber(t), gt, t.encode('utf-8'))

    def test_isTransition(self):
        testList = [(u"1.",True),(u"10.",True), (u"11.",False)]

        for t, gt in testList:
          self.assertEquals(NumberFormula._isTransitionNumber(t), gt, t.encode('utf-8'))

    def test_isOrdinal(self):
        testList = [(u"1st",True),(u"2nd",True),(u"3rd",True),(u"4th",True)]
        for t, gt in testList:
            self.assertEquals(NumberFormula._isOrdinalNumber(t), gt, t.encode('utf-8'))

    def test_isDecimal(self):
        testList = [(u"2.5",True), (u"2,5",False),(u"2.5,3",False), (u"2-5",False)]

        for t, gt in testList:
            self.assertEquals(NumberFormula._isDecimalNumber(t), gt, t.encode('utf-8'))

    def test_isRoman(self):
        testList = [(u"LV",True), (u"XII",True), (u"La", False)]

        for t, gt in testList:
            self.assertEquals(NumberFormula._isRomanNumber(t), gt, t.encode('utf-8'))

    def test_hasNumber(self):
        testList = [(u"12",True), (u"1ab",True),(u"ab22",True), (u"Xab",True),
                    (u"xab",False), (u"a1ab",True), (u"he has 1'416'000 euro",True)]

        for t, gt in testList:
            self.assertEquals(hasNumber(NumberFormula,t), gt, t.encode('utf-8'))

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
            self.assertEquals(gt.encode('utf-8'), r.encode('utf-8'),
                              "%s is not %s" % (r.encode('utf-8'), gt.encode('utf-8')))

    def test_decimal2word(self):
        testList = self.testDict["decimal"]
        self.evaluateListValues(testList, NumberFormula._decimal2word)

    def test_roman2word(self):
        testList = self.testDict["roman"]
        self.evaluateListValues(testList, NumberFormula._roman2word)

    def test_apply(self):
        f = NumberFormula()

        for k in self.testDict.keys():
            #print "--> Testing %s " % k
            testList = self.testDict[k]
            self.evaluateListValues(testList, f.apply)
