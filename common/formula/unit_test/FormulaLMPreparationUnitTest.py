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

import unittest, re, string, logging

from asrt.common.formula.FormulaLMPreparation import LMPreparationFormula
from asrt.common.AsrtConstants import UTF8MAP, SPACEPATTERN, DOTCOMMAEXCLUDE, PUNCTUATIONEXCLUDE
from asrt.common.AsrtConstants import ABBREVIATIONS
from asrt.common.LoggingSetup import setupLogging

setupLogging(logging.INFO, "./output.log")

class TestFormulaLMPreparation(unittest.TestCase):
    allPunctList = DOTCOMMAEXCLUDE + PUNCTUATIONEXCLUDE

    def verifyEqual(self, testList, f, callback):
        for t, gt in testList:
            f.strText = t
            callback()
            self.assertEquals(gt.encode('utf-8'), f.strText.encode('utf-8'))

    ############
    #Tests
    #
    def testNormalizeUtf8(self):
        testList = []
        for match, sub, comment, languageId in UTF8MAP:
            testList.append(match)

        gtList = []
        for match, sub, comment, languageId in UTF8MAP:
            gtList.append(sub)

        strGt = u" ".join(gtList)
        strGt = strGt.encode('utf-8').rstrip().strip()
        strGt = re.sub(SPACEPATTERN, u" ", 
                        strGt, flags=re.UNICODE)

        f = LMPreparationFormula()
        f.setText(u" ".join(testList))
        f._normalizeUtf8()
        strResult = f.getText()

        self.assertEquals(strGt, strResult.encode('utf-8'))

    def testNormalizePunctuation(self):
        f = LMPreparationFormula()
        f.setText(u"".join(string.punctuation))
        f._normalizePunctuation(self.allPunctList)
        strResult = f.getText()

        gt = "$%&' @"
        self.assertEquals(gt, strResult)

        f.setLanguageId(1)
        f._normalizePunctuation(self.allPunctList)
        strResult = f.getText()

        gt = "dollars pourcent et ' at"
        self.assertEquals(gt, strResult)

    def testNormalizeCharacters(self):
        strTest = ur"a b c \uff1b , % œ"
        strGt = ur"a b c % oe"

        f = LMPreparationFormula()
        f.setText(strTest)
        f._normalizeUtf8()
        f._normalizePunctuation(self.allPunctList)
        self.assertEquals(strGt, f.getText())

    def testIsNoise(self):
        for p in list(string.punctuation):
            strTest = p*4
            self.assertTrue(LMPreparationFormula._isNoise(strTest))

    def testFilterNoiseWords(self):
        strTest = u"!-?- hello how !!!! are you *-+$"
        strGt = u"hello how are you"

        f = LMPreparationFormula()
        f.setText(strTest)
        strTest = f._filterNoiseWords()

        self.assertEquals(strGt, strTest)

    def testExpandAcronyms(self):
        testList = [(u"PDCB.",u"p. d. c. b."),
                    (u"PDC:",u"p. d. c.")]

        f = LMPreparationFormula()
        self.verifyEqual(testList, f, f._expandAcronyms)

    def testExpandNumberInWords(self):
        testList = [(ur"A1", ur"A. 1"),(ur"P3B", ur"P. 3 B."), (ur"P5B4", ur"P. 5 B. 4"),
                     (ur"PPB5",ur"PPB 5")]
        
        f = LMPreparationFormula()
        self.verifyEqual(testList, f, f._expandNumberInWords)

    def testExpandAbbreviations(self):
        f = LMPreparationFormula()
        for languageId, v in ABBREVIATIONS.items():
            f.setLanguageId(languageId)
            for abbr, gt in v.items():
                f.strText = abbr
                f._expandAbbreviations()
                self.assertEquals(gt.encode('utf-8'), f.strText.encode('utf-8'))

    def testAll(self):
        testList =[(u"A dix heures", u"à dix heures"),
                   (u"1. Election",u"premièrement election"),
                   (u"R1",u"r. un"), (ur"A1", ur"a. un"),(ur"P3B", ur"p. trois b."),
                   (ur"P5B4", ur"p. cinq b. quatre"), 
                   (ur"PPB5",ur"p. p. b.  cinq"),
                   (ur"rte",ur"route"),
                   (ur"Constantin, p. l. r., président de",ur"constantin p. l. r. président de")]

        f = LMPreparationFormula()
        f.setLanguageId(1)
        
        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEquals(gt.encode('utf-8'), r.encode('utf-8'))
