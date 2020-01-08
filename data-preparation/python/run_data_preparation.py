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
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

usage = """
    Prepare a single document.
"""

import sys
import os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../../../")

import logging
import argparse

from asrt.common.DataPreparationAPI import DataPreparationAPI
from asrt.common.LoggingSetup import setupLogging

####################
# Main
#
if __name__ == "__main__":
    # Setup parser
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", "--input", help="input file",
                        nargs=1, dest="inputFile", required=True)
    parser.add_argument("-o", "--output", help="output directory",
                        nargs=1, dest="outputDir", required=True)
    parser.add_argument("-l", "--language", help="language (0=unk,1=fr,2=ge,3=en,4=it)", nargs=1,
                        dest="language", default=[0])
    parser.add_argument("-r", "--regex", help="regex file",
                        nargs=1, dest="regexFile", default=[None])
    parser.add_argument("-f", "--filter", help="filter sentences",
                        dest="filter", action="store_true")
    parser.add_argument("--filter2ndStage", help="enable filter sentence checking for second stage",
                        dest="filter2ndStage", action="store_true")
    parser.add_argument("-n", "--rmpunct", help="remove punctuation",
                        dest="rmpunct", action="store_true")
    parser.add_argument("-p", "--vbpunct", help="verbalize punctuation",
                        dest="vbpunct", action="store_true")
    parser.add_argument("-s", "--rawseg", help="do not segment sentences with NLTK",
                        dest="rawseg", action="store_true")
    parser.add_argument(
        "-m", "--lm", help="prepare for lm modeling", dest="lm", action="store_true")
    parser.add_argument(
        "-t", "--split", help="Split words with numbers", dest="split", action="store_true")
    parser.add_argument(
        "-d", "--debug", help="enable debug output", dest="debug", action="store_true")

    # Parse arguments
    args = parser.parse_args()
    inputFile = args.inputFile[0]
    outputDir = args.outputDir[0]
    language = int(args.language[0])
    regexFile = args.regexFile[0]

    # Flags
    debug = bool(args.debug)
    filterSentences = bool(args.filter)
    filterSentences2ndStage = bool(args.filter2ndStage)
    removePunctuation = bool(args.rmpunct)
    verbalizePunctuation = bool(args.vbpunct)
    rawSeg = bool(args.rawseg)
    lmModeling = bool(args.lm)
    expandNumberInWords = bool(args.split)

    setupLogging(logging.INFO, outputDir + "/task_log.txt")

    # Api setup
    api = DataPreparationAPI(inputFile, outputDir)
    api.setRegexFile(regexFile)
    api.setFilterSentences(filterSentences)
    api.setFilterSentences2ndStage(filterSentences2ndStage)
    api.setLMModeling(lmModeling)
    api.setRemovePunctuation(removePunctuation)
    api.setVerbalizePunctuation(verbalizePunctuation)
    api.setSegmentWithNLTK(not rawSeg)

    api.setExpandNumberInWords(expandNumberInWords)

    if language == 0:
        api.trainClassifier()

    # Main processing
    api.prepareDocument(language)
    api.outputSentencesToFiles(outputDir)
