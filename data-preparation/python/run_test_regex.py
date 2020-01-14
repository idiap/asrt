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

usage = """
    Format the given text using the regular expression file.
"""

import os
import sys
import logging
import argparse

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../../../")
sys.path.append(scriptsDir + "/../../lib/num2words")

from asrt.common.LoggingSetup import setupLogging
from asrt.common.formula.FormulaRegularExpression import RegexList, RegularExpressionFormula

#######################################
# main
#
if __name__ == "__main__":
    # Setup parser
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-r", "--regex", help="regex file",
                        nargs=1, dest="regexFile", required=True)
    parser.add_argument("-i", "--input", help="input text",
                        nargs=1, dest="inputText", default=[""])
    parser.add_argument("-l", "--language", help="language (0=unk,1=fr,2=ge,3=en,4=it)",
                        nargs=1, dest="language", default=[0])
    parser.add_argument("-s", "--display", help="display regular expressions",
                        dest="display", action="store_true")
    parser.add_argument(
        "-d", "--debug", help="enable debug output", dest="debug", action="store_true")

    # Parse arguments
    args = parser.parse_args()
    regexFile = args.regexFile[0]
    inputText = args.inputText[0]
    languageId = int(args.language[0])

    # Flags
    display = args.display
    debug = args.debug

    setupLogging(logging.INFO)

    substitutionPatternList = []
    for line in RegexList.loadFromFile(regexFile):
        if int(line[RegexList.TYPEINDICE]) != -1:
            substitutionPatternList.append(line)

    f = RegularExpressionFormula(None, substitutionPatternList)

    if display:
        f.displayPatterns(languageId)

    result = f.apply(inputText, languageId, debug)

    print(("Result --------------\n", result.encode('utf-8'), "\n---------------------"))
