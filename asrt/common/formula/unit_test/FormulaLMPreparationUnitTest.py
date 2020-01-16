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

import unittest
import re
import string
import logging

from asrt.common.formula.FormulaLMPreparation import LMPreparationFormula
from asrt.common.AsrtConstants import UTF8MAP, SPACEPATTERN, DOTCOMMAEXCLUDE, PUNCTUATIONEXCLUDE
from asrt.common.AsrtConstants import ABBREVIATIONS
from asrt.common.LoggingSetup import setupLogging
from asrt.config.AsrtConfig import TEMPDIRUNITTEST

setupLogging(logging.INFO, TEMPDIRUNITTEST + "/output.log")


class TestFormulaLMPreparation(unittest.TestCase):
    allPunctList = DOTCOMMAEXCLUDE + PUNCTUATIONEXCLUDE

    def verifyEqual(self, testList, f, callback):
        for t, gt in testList:
            f.strText = t
            callback()
            self.assertEqual(gt.encode('utf-8'), f.strText.encode('utf-8'))

    ############
    # Tests
    #
    def testNormalizeUtf8(self):
        languages = ['0', '1', '2']
        testList = {}
        for lang in languages:
            testList[lang] = []
        for match, sub, comment, languageId in UTF8MAP:
            for lang in languages:
                if (lang == int(languageId)):
                    testList[lang].append(match)

        gtList = {}
        for lang in languages:
            gtList[lang] = []
        for match, sub, comment, languageId in UTF8MAP:
            for lang in languages:
                if (lang == int(languageId)):
                    gtList[lang].append(sub)

        for lang in languages:
            strGt = " ".join(gtList[lang])
            strGt = strGt.rstrip().strip()
            strGt = re.sub(SPACEPATTERN, " ",
                           strGt, flags=re.UNICODE)

            f = LMPreparationFormula()
            f.setText(" ".join(testList[lang]))
            f._normalizeUtf8()
            strResult = f.getText()

            self.assertEqual(strGt.encode('utf-8'), strResult.encode('utf-8'))

    def testNormalizePunctuation(self):
        f = LMPreparationFormula()
        f.setText("".join(string.punctuation + "‰"))
        f.setExpandNumberInWords(False)
        f._normalizePunctuation(self.allPunctList)
        strResult = f.getText()

        gt = "$%&'-/@‰"
        self.assertEqual(gt, strResult)

        f.setLanguageId(1)
        f._normalizePunctuation(self.allPunctList)
        strResult = f.getText()

        gt = "dollars pourcent et '-/ at pour mille"
        self.assertEqual(gt, strResult)

    def testNormalizePunctuationKeepInWords(self):
        f = LMPreparationFormula()
        f.setExpandNumberInWords(False)

        f.setText("".join("/ HES-SO und AdG/LA - auch im Winter / Sommer -"))
        f._normalizePunctuation(self.allPunctList)
        strResult = f.getText()

        gt = "HES-SO und AdG/LA auch im Winter Sommer"
        self.assertEqual(gt, strResult)

    def testNormalizeCharacters(self):
        strTest = r"a b c ； , % œ"
        strGt = r"a b c % oe"

        f = LMPreparationFormula()
        f.setText(strTest)
        f._normalizeUtf8()
        f._normalizePunctuation(self.allPunctList)
        self.assertEqual(strGt, f.getText())

    def testIsNoise(self):
        for p in list(string.punctuation):
            strTest = p * 4
            self.assertTrue(LMPreparationFormula._isNoise(strTest))

    def testFilterNoiseWords(self):
        strTest = "!-?- hello how !!!! are you *-+$"
        strGt = "hello how are you"

        f = LMPreparationFormula()
        f.setText(strTest)
        strTest = f._filterNoiseWords()

        self.assertEqual(strGt, strTest)

    def testExpandAcronyms(self):
        testList = [("PDCB.", "p. d. c. b."),
                    ("PDC:", "p. d. c.")]

        f = LMPreparationFormula()
        self.verifyEqual(testList, f, f._expandAcronyms)

    def testExpandNumberInWords(self):
        testList = [(r"A1", r"A. 1"), (r"P3B", r"P. 3 B."), (r"P5B4", r"P. 5 B. 4"),
                    (r"PPB5", r"PPB 5"), (r"10jährige", r"10 jährige")]

        f = LMPreparationFormula()
        self.verifyEqual(testList, f, f._expandNumberInWords)

        f.setExpandNumberInWords(False)
        testList = [(r"1er", r"1er")]
        f.setLanguageId(1)
        self.verifyEqual(testList, f, f._expandNumberInWords)

        testList = [(r"1st", r"1st")]
        f.setLanguageId(3)
        self.verifyEqual(testList, f, f._expandNumberInWords)

        testList = [(r"18-jähriger", r"18 -jähriger")]
        f.setLanguageId(2)
        self.verifyEqual(testList, f, f._expandNumberInWords)

    def testExpandAbbreviations(self):
        f = LMPreparationFormula()
        for languageId, v in list(ABBREVIATIONS.items()):
            f.setLanguageId(languageId)
            for abbr, gt in list(v.items()):
                f.strText = abbr
                f._expandAbbreviations()
                self.assertEqual(gt.encode('utf-8'),
                                 f.strText.encode('utf-8'))

    def testContractionPrefixes(self):
        testList = [(r"President' s", r"president's", 3),
                    (r"President' s of", r"president's of", 3)]

        f = LMPreparationFormula()
        f.setExpandNumberInWords(False)

        for t, gt, languageId in testList:
            f.setLanguageId(languageId)
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

    def testAll(self):
        testList = [("A dix heures", "à dix heures", False),
                    ("1. Election", "premièrement election", False),
                    ("R1", "r. un", False), (r"A1", r"a. un",
                                             False), (r"P3B", r"p. trois b.", False),
                    (r"P5B4", r"p. cinq b. quatre", False),
                    (r"PPB5", r"p. p. b. cinq", False),
                    (r"rte", r"route", False),
                    (r"Constantin, p. l. r., président de",
                     r"constantin p. l. r. président de", False),
                    (r"/ HES-SO und AdG/LA - auch im Winter / Sommer -", r"hes-so und adg/la auch im winter sommer", True)]

        f = LMPreparationFormula()
        f.setLanguageId(1)

        for t, gt, knw in testList:
            f.setText(t)
            f.setExpandNumberInWords(not knw)
            r = f.prepareText()
            self.assertEqual(gt, r)

    def testFrench(self):
        testList = [(r"à plus tard", r"à plus tard"),
                    (r"maîtres", r"maîtres"),
                    (r"maïs", r"maïs"),
                    (r"emmaüs", r"emmaüs"),
                    (r"mäman", r"mäman"),
                    (r"1er", r"premier"),
                    (r"20ème", r"vingtième"),
                    (r"18-age", r"dix huit age")]

        # No new words are kepts, hyphens are removed
        f = LMPreparationFormula()
        f.setExpandNumberInWords(True)
        f.setLanguageId(1)

        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

        # Keep new words implies keep hyphens in words
        f.setExpandNumberInWords(False)

        testList = [(r"18-age", r"18-age")]
        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

    def testGerman(self):
        testList = [(r"emmaüs", r"emmaüs"),
                    ("mein àrbeit", "mein àrbeit"),
                    (r"môchten", r"môchten"),
                    (r"mädchen", r"mädchen"),
                    (r"meîn", r"meîn"),
                    (r"meïn", r"meïn"),
                    (r"18-jähriger", r"achtzehn jähriger")]

        # No new words are kepts
        f = LMPreparationFormula()
        f.setExpandNumberInWords(True)
        f.setLanguageId(2)

        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

        # New words are kept
        testList = [(r"18-jähriger", r"18-jähriger")]
        f.setExpandNumberInWords(False)

        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

    def testEnglish(self):
        testList = [(r"object 5", r"object five"),
                    (r"1st", r"first")]

        f = LMPreparationFormula()
        f.setExpandNumberInWords(True)
        f.setLanguageId(3)

        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))

        testList = [(r"18-year-old", r"18-year-old")]
        f.setExpandNumberInWords(False)

        for t, gt in testList:
            f.setText(t)
            r = f.prepareText()
            self.assertEqual(gt.encode('utf-8'), r.encode('utf-8'))
