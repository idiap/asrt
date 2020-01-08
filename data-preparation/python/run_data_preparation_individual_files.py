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
__date__ = "Date: 2017/09"
__copyright__ = "Copyright (c) 2017 Idiap Research Institute"
__license__ = "BSD 3-Clause"

usage="""
    Prepare a given list of documents.
"""

import sys, os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../../../")

import logging
import argparse

from asrt.common.DataPreparationAPI import DataPreparationAPI
from asrt.common.LoggingSetup import setupLogging
from asrt.common.ioread import Ioread
from asrt.common.MyFile import MyFile

####################
#Main
#
if __name__ == "__main__":
    #Setup parser
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", "--inputlist", help="input list", nargs=1, dest="inputList", required=True)
    parser.add_argument("-o", "--output", help="output directory", nargs=1, dest="outputDir", required=True)
    parser.add_argument("-l", "--language", help="language (0=unk,1=fr,2=ge,3=en,4=it)", nargs=1,
                                       dest="language", default=[0])
    parser.add_argument("-r", "--regex", help="regex file", nargs=1, dest="regexFile", default=[None])
    parser.add_argument("-f", "--filter", help="filter sentences", dest="filter",action="store_true")
    parser.add_argument(      "--filter2ndStage", help="enable filter sentence checking for second stage", dest="filter2ndStage", action="store_true")
    parser.add_argument("-n", "--rmpunct", help="remove punctuation", dest="rmpunct",action="store_true")
    parser.add_argument("-p", "--vbpunct", help="verbalize punctuation", dest="vbpunct",action="store_true")
    parser.add_argument("-s", "--rawseg", help="do not segment sentences with NLTK", dest="rawseg",action="store_true")
    parser.add_argument("-m", "--lm", help="prepare for lm modeling", dest="lm",action="store_true")
    parser.add_argument("-t", "--trim", help="remove special characters in words", dest="trim",action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug output", dest="debug",action="store_true")


    #Parse arguments
    args = parser.parse_args()
    inputList = args.inputList[0]
    outputDir = args.outputDir[0]
    language = int(args.language[0])
    regexFile = args.regexFile[0]

    #Flags
    debug = bool(args.debug)
    filterSentences = bool(args.filter)
    filterSentences2ndStage  = bool( args.filter2ndStage )
    removePunctuation = bool(args.rmpunct)
    verbalizePunctuation = bool(args.vbpunct)
    rawSeg = bool(args.rawseg)
    lmModeling = bool(args.lm)
    expandNumberInWords = bool(not args.trim)

    setupLogging(logging.INFO, outputDir + "/data_preparation_log.txt")

    #Api setup
    api = DataPreparationAPI(None, outputDir)
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

    #Main processing
    MyFile.checkDirExists(outputDir)

    io = Ioread()
    inputList = io.readFileContentList(inputList)

    for i, f in enumerate(inputList):
        api.setInputFile(f)
        api.prepareDocument(language)
        strUnformatted = api.getCleanedText()

        outputFile = "%s/%s.lab" % (outputDir, os.path.splitext(os.path.basename(f))[0])
        io.writeFileContent(outputFile, strUnformatted + u"\n")
