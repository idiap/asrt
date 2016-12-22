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
from asrt.common.english.FormulaNumber import NumberFormula
from asrt.common.AsrtUtility import hasNumber

class FormulaNumberUnitTest(unittest.TestCase):

    testDict = { "cardinal"   : [],
                 "transition" : [],
                 "ordinal"    : [],
                 "decimal"    : [],
                 "roman"      : [],
                 "all"        : []
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
        pass

    def test_isTransition(self):
        pass

    def test_isOrdinal(self):
        pass

    def test_isDecimal(self):
        pass

    def test_isRoman(self):
    	pass

    def test_hasNumber(self):
        pass

    def test_normalizeNumber(self):
        pass

    def test_cardinal2word(self):
        pass

    def test_transition2word(self):
        pass

    def test_ordinal2word(self):
        pass

    def test_decimal2word(self):
        pass

    def test_roman2word(self):
        pass

    def test_apply(self):
        pass
