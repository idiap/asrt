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

import unittest, re, string

from formula.FormulaLMPreparation import LMPreparationFormula
from AsrtConstants import UTF8MAP, SPACEPATTERN, DOTCOMMAEXCLUDE, PUNCTUATIONEXCLUDE
from AsrtConstants import CONTRACTIONPREFIXELIST

class TestFormulaLMPreparation(unittest.TestCase):
    allPunctList = DOTCOMMAEXCLUDE + PUNCTUATIONEXCLUDE

    def setUp(self):
        print ""

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
