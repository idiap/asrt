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
__date__ = "Date: 2015/12"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

usage = """
    Apply a sequence of regular expressions in the given
    order to an utf-8 encoded text file.
"""

import sys, os
import argparse
import logging

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../../../")

from asrt.common.ioread import Ioread
from asrt.config.AsrtConfig import FRENCH
from asrt.common.formula.FormulaRegularExpression import RegularExpressionFormula
from asrt.common.LoggingSetup import setupLogging

################
#Implementation
#
def applyRegexes(inputFile, outputFile, regularFile):
    """Apply the regular expressions contained in 'regularFile'.

       params: - inputFile   : a text file in 'utf-8' encoding
               - outputFile  : the result text file in 'utf-8' encoding
               - regularFile : the file containing the regular expressions
                               to apply.
    """
    regexFormula = RegularExpressionFormula(rulesFile=regularFile)

    io = Ioread()
    fd = io.openFile(inputFile)

    count, linesList = 0, []

    #Read first line
    l = fd.readline()

    while l != "":
        l = l.rstrip().strip()

        #Remove punctuation using regular expressions
        linesList.append(regexFormula.apply(l, FRENCH))
        
        count += 1
        if count % 50000 == 0:
            print "Processed %d values" % count

        #Read next line
        l = fd.readline()

    io.closeFile(fd)

    strContent = u"\n".join(linesList)
    io.writeFileContent(outputFile, strContent)

################
# main
#
if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", "--input", help="input file", nargs=1, dest="inputFile", required=True)
    parser.add_argument("-o", "--output", help="output file", nargs=1, dest="outputFile", required=True)
    parser.add_argument("-r", "--regex", help="regular expression file", nargs=1, dest="regexFile", required=True)
    
    args = parser.parse_args()

    inputFile = os.path.abspath(args.inputFile[0])
    outputFile = os.path.abspath(args.outputFile[0])
    regexFile = os.path.abspath(args.regexFile[0])

    setupLogging(logging.INFO)

    applyRegexes(inputFile, outputFile, regexFile)
    