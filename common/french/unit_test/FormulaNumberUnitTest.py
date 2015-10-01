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

    testDict = { "cardinal"   : [(u"10",u"dix"),(u"25",u"vingt cinq")],
                 "transition" : [(u"1.",u"premièrement"),(u"10.",u"dixièmement")],
                 "ordinal"    : [(u"1er",u"premier"),(u"1ère",u"première"),(u"2ème",u"deuxième"),
                                 (u"80ème",u"quatre-vingtième"),(u"400ème",u"quatre centième"),
                                 (u"380ème",u"trois cent quatre-vingtième"),(u"4000000ème",u"quatre millionième"),
                                 (u"XXVème",u"vingt-cinquième"), (u"XXème",u"vingtième"),
                                 (u"XXIIIe",u"vingt-troisième")],
                 "decimal"    : [(u"2,5",u"deux virgule cinq"), (u"2.5,3",u"deux point cinq virgule trois")],
                 "roman"      : [(u"XXIII",u"vingt trois"), (u"XX",u"vingt")],
                 "all"        : [(u"1ab",u"1ab"),(u"ab",u"ab"),
                                 (u"le 25 mars 2015 2.5 XXème",u"le vingt cinq mars deux mille quinze deux point cinq vingtième"),
                                 (u"le 25.",u"le vingt cinq"),
                                 (u"le 25.5.",u"le vingt cinq point cinq"),
                                 (u"14 alinéa 1, some text",u"quatorze alinéa un some text"),
                                 (u"l'article 12,",u"l'article douze"),
                                 (u"dans le XXIIIe siècle", u"dans le vingt-troisième siècle"),
                                 (u"Ce matin", u"Ce matin"),
                                 (u"Le matin", u"Le matin")]
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
    def test_isCardinal(self):
        testList = [(u"2",True),(u"123",True), (u"123.",False)]

        for t, gt in testList:
        	self.assertEquals(NumberFormula._isCardinalNumber(t), gt, t.encode('utf-8'))

    def test_isTransition(self):
        testList = [(u"1.",True),(u"10.",True), (u"11.",False)]

        for t, gt in testList:
          self.assertEquals(NumberFormula._isTransitionNumber(t), gt, t.encode('utf-8'))
    
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
    	testList = [(u"V",False), (u"XII",True), (u"La", False)]

    	for t, gt in testList:
        	self.assertEquals(NumberFormula._isRomanNumber(t), gt, t.encode('utf-8'))

    def test_hasNumber(self):
        testList = [(u"12",True), (u"1ab",True),(u"ab22",True), (u"Xab",True),
                    (u"xab",False), (u"a1ab",True)]

        for t, gt in testList:
            self.assertEquals(hasNumber(NumberFormula,t), gt, t.encode('utf-8'))

    def test_normalizeNumber(self):
        testList = [(u"50'000",u"50000"),(u"550'000'000",u"550000000")]
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
            #print "Testing %s " % k
            testList = self.testDict[k]
            self.evaluateListValues(testList, f.apply)
    
