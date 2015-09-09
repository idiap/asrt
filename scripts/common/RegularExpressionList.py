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

import logging, re
from ioread import Ioread

class RegexList():
    """ Wrapper to load regular expressions from a file
        or to get other normalization regular expressions.
    """
    logger            = logging.getLogger("Asrt.RegexList") 

    MATCHINGINDICE    = 0
    SUBINDICE         = 1
    TYPEINDICE        = 2

    @staticmethod
    def loadFromFile(regexFile):
        """Load regular expressions from a csv file.

           The file is assumed to be in CSV file format
           with tabs as fields separators and no quotes
           around fields.

           File format is:
                matching pattern, substitution pattern, 
                    regex type (substitution = 0, deletion = 1), comments

           param regexFile: a csv file
           return a compiled regular expression list with their
                  matching patterns 
        """
        RegexList.logger.info("Load regular expression from %s" % regexFile)
        
        io = Ioread()
        regexList = io.readCSV(regexFile,'\t')
        substitutionPatternList = RegexList.removeComments(regexList[1:])
        RegexList.logger.info("Done loading regular expressions")

        return substitutionPatternList
       
    @staticmethod
    def removeComments(regexList, bCompile=False):
        """Remove the comments part.
        """
        substitutionPatternList = []

        for row in regexList:
            matchPattern = row[RegexList.MATCHINGINDICE]
            if bCompile:
                matchPattern = re.compile(row[RegexList.MATCHINGINDICE], flags=re.UNICODE)

            substitutionPatternList.append((matchPattern,
                row[RegexList.SUBINDICE],row[RegexList.TYPEINDICE]))

        return substitutionPatternList
