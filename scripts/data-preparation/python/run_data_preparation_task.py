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
__date__ = "Date: 2014/09"
__copyright__ = "Copyright (c) 2014 Idiap Research Institute"
__license__ = "BSD 3-Clause"

usage="""
    Normalise a set of text files in order to build
    a language model.
"""

import sys, os

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../../common")

import logging
import argparse

from tasks.Task import TaskInfo
from tasks.TaskImportDocument import ImportDocumentTask
from LoggingSetup import setupLogging


STRPARAMETERS = "regexfile=%s;debug=%s;removePunctuation=%s;verbalizePunctuation=%s;" + \
                "textFiltering=%s;lmModeling=%s"


####################
#Main
#
if __name__ == "__main__":
    #Setup parser
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-t", "--target", help="target directory containing the data.olist and data.omap", 
                         nargs=1, dest="targetDir", required=True)
    parser.add_argument("-o", "--output", help="output directory", nargs=1, dest="outputDir", required=True)
    parser.add_argument("-r", "--regex", help="regex file", nargs=1, dest="regexFile", required=True)
    parser.add_argument("-f", "--filter", help="filter sentences", dest="filter",action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug output", action="store_true")
    parser.add_argument("-n", "--rmpunctuation", help="remove punctuation", action="store_true")
    parser.add_argument("-p", "--vbpunctuation", help="verbalize punctuation", action="store_true")
    parser.add_argument("-m", "--lm", help="prepare for lm modeling", dest="lm",action="store_true")

    
    #Parse arguments
    args = parser.parse_args()
    targetDir = args.targetDir[0]
    outputDir = args.outputDir[0]
    regexFile = args.regexFile[0]

    setupLogging(logging.INFO, outputDir + "/task_log.txt")

    task = ImportDocumentTask(TaskInfo(STRPARAMETERS % (regexFile, str(args.debug), 
                                                        args.rmpunctuation, args.vbpunctuation,
                                                        args.filter, args.lm), 
                                       outputDir, targetDir))
    task.execute()
