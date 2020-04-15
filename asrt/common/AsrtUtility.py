#!/usr/bin/env python3
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
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
import sys
import traceback
import unittest
import logging
import re
from asrt.common.AsrtConstants import SPACEPATTERN

logger = logging.getLogger("Asrt.AsrtUtility")

##################
# Debug
#


def getByteString(message):
    """Get a byte encoded exception message.
    """
    if type(message) == str:
        return message.encode('utf-8')

    return message


def getErrorMessage(e, prefix):
    """Get full error message with stack trace.
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    stackMessage = "\n------------ Begin stack ------------\n" + \
                   getByteString(traceback.format_exc().rstrip()) + "\n" + \
                   "------------ End stack --------------"
    strError = "%s: %s (line: %d), %s\n%s" % \
        (prefix, fname, exc_tb.tb_lineno, getByteString(e.message), stackMessage)

    return strError

##################
# Test
#


def getTestSuite(pGetSuite, unitTestList):
    """Given a list of test, return the
       corresponding test suite.
    """
    suiteList = None

    if unitTestList[0] == 'all':
        suiteList = pGetSuite('all')
    else:
        # Specific unit tests
        if unitTestList[0] != 'all':
            suiteList = []
            for m in unitTestList:
                suiteList.extend(pGetSuite(m))

    # No test suites found
    if len(suiteList) == 0:
        return None

    return unittest.TestSuite(suiteList)

##################
# Number expansion
#


def convertNumber(cls, strText):
    """Multilingual algorithm to convert a number
       into a written form.
    """
    wordsList = re.split(SPACEPATTERN, strText, flags=re.UNICODE)

    newWordsList = []
    for i, w in enumerate(wordsList):
        if not hasNumber(cls, w):
            newWordsList.append(w)
            continue
        try:
            # Now check number type
            if cls._isTransitionNumber(w):
                wNorm = cls._transition2word(w)
            else:
                # Numbers may contain alphanumeric
                # characters
                wNorm = cls._normalizeNumber(w)
                if cls._isCardinalNumber(wNorm):
                    wNorm = cls._cardinal2word(wNorm)
                elif cls._isOrdinalNumber(wNorm):
                    wNorm = cls._ordinal2word(wordsList, i)
                elif cls._isDecimalNumber(wNorm):
                    wNorm = cls._decimal2word(wNorm)
                elif cls._isRomanNumber(wNorm):
                    wNorm = cls._roman2word(wNorm)
                else:
                    wNorm = w
            newWordsList.append(wNorm)

        except Exception as e:
            prefix = "Error formatting number (%s): %s" % \
                (w, str(e))
            #errorMessage = getErrorMessage(e, prefix)
            logger.warning(prefix)

            # Split into digits
            for n in list(w):
                newWordsList.append(cls._cardinal2word(n))

    return " ".join(newWordsList)


def hasNumber(cls, strWord):
    """Check if 'strWord' contains numbers.

       param strWord: an utf-8 encoded words
       return True or False
    """
    # Use search instead of match
    return cls.HASNUMBERREGEX.search(strWord) != None
