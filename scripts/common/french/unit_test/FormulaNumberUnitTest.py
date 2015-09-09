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
from french.FormulaNumber import NumberFormula

class FormulaNumberUnitTest(unittest.TestCase):

    testDict = { "cardinal": [(u"10",u"dix"),(u"25",u"vingt cinq")],
                 "ordinal" : [(u"1er",u"premier"),(u"1ère",u"première"),(u"2ème",u"deuxième"),
                              (u"Vème",u"cinquième"), (u"Xème",u"dixième")],
                 "decimal" : [(u"2,5",u"deux virgule cinq"), (u"2.5,3",u"deux point cinq virgule trois")],
                 "roman"   : [(u"V",u"cinq"), (u"X",u"dix")],
                 "all"     : [(u"1ab",u"1ab"),(u"ab",u"ab"),
                              (u"le 25 mars 2015 2.5 Xème",u"le vingt cinq mars deux mille quinze deux point cinq dixième"),
                              (u"le 25.",u"le vingt cinq"),
                              (u"le 25.5.",u"le vingt cinq point cinq"),
                              (u"14 alinéa 1, some text",u"quatorze alinéa un some text")]
    }

    #################
    # Implementation
    #
    def evaluateListValues(self, testList, callback):
        for t, gt in testList:
            r = callback(t).encode('utf-8')
            self.assertEquals(gt.encode('utf-8'), r, r)

    #################
    # Unit tests
    #
    def test_isCardinal(self):
        testList = [(u"2",True),(u"123",True), (u"123.",False)]

        for t, gt in testList:
        	self.assertEquals(NumberFormula._isCardinalNumber(t), gt, t.encode('utf-8'))
    
    def test_isOrdinal(self):
        testList = [(u"1er",True), (u"1re",True), (u"1ère",True), (u"2e",True), (u"2ème",True), 
                    (u"Ier",True), (u"XIIème",True)]

        for t, gt in testList:
        	self.assertEquals(NumberFormula._isOrdinalNumber(t), gt, t.encode('utf-8'))
 
    def test_isDecimal(self):
        testList = [(u"2.5",True), (u"2,5",True),(u"2,5,3",True), (u"2-5",False)]

        for t, gt in testList:
        	self.assertEquals(NumberFormula._isDecimalNumber(t), gt, t.encode('utf-8'))

    def test_isRoman(self):
    	testList = [(u"V",True), (u"XII",True), (u"La", False)]

    	for t, gt in testList:
        	self.assertEquals(NumberFormula._isRomanNumber(t), gt, t.encode('utf-8'))

    def test_hasNumber(self):
        testList = [(u"12",True), (u"1ab",True),(u"ab22",True), (u"Xab",True),
                    (u"xab",False), (u"a1ab",True)]

        for t, gt in testList:
            self.assertEquals(NumberFormula._hasNumber(t), gt, t.encode('utf-8'))

    def test_normalizeNumber(self):
        testList = [(u"50'000",u"50000"),(u"550'000'000",u"550000000")]
        self.evaluateListValues(testList, NumberFormula._normalizeNumber)
        
    def test_cardinal2word(self):
        testList = self.testDict["cardinal"]
        self.evaluateListValues(testList, NumberFormula._cardinal2word)
        
    def test_ordinal2word(self):
        testList = self.testDict["ordinal"]
        self.evaluateListValues(testList, NumberFormula._ordinal2word)
        
    def test_decimal2word(self):
        testList = self.testDict["decimal"]
        self.evaluateListValues(testList, NumberFormula._decimal2word)

    def test_roman2word(self):
        testList = self.testDict["roman"]
        self.evaluateListValues(testList, NumberFormula._roman2word)

    def test_apply(self):
        f = NumberFormula()

        for k in self.testDict.keys():
            #print "Testing %s " % k
            testList = self.testDict[k]
            self.evaluateListValues(testList, f.apply)
    