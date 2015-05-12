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
__date__ = "Date: 2012/05/31"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import re

class CompiledRegexList:
    """A list of compiled patterns.
    """
    logger = logging.getLogger("Asrt.CompliledRegexList")
    
    def __init__(self, regexList):
        self.regexList = regexList
        self.patternsList = []
        self._compileRegexList()
    
    ########################
    #Public methods
    #
    def substitute(self, text, substitutionString):
        """Substitute regex matches by
           'substitutionString'.
        """
        #print ""
        for p in self.patternsList:
            #print "Pattern: " + p.pattern + " text: " + text + " sub: " + substitutionString
            text = p.sub(substitutionString, text)
            #print "Result: " + text
        
        return text.rstrip().strip()
        
    def findAll(self, text):
        """Find all matches in the regex list.
        """
        matchList = []
        for p in self.patternsList:
            matchList.extend(p.findall(text))
        return matchList

    def findAllByDecreasingOrder(self, text):
        """Find all matches in the regex list.
        """
        matchList = []
        for p in self.patternsList:
            #Find all for pattern
            strList = p.findall(text)            
            
            #Remove matching patterns from
            #original string
            for (s,p,e) in strList:
                text = text.replace(p, ' ')
            matchList.extend(strList)            

        return matchList

    def getPattern(self, patternIndex):
        """The pattern. 
        """
        return self.patternsList[patternIndex].pattern

    def getNumberPatterns(self):
        """Number of patterns int the list. 
        """
        return len(self.patternsList)
    
    ########################
    # Static members
    #
    def _compileRegexList(self):
        """Compile all the regexes.
        """
        for regex in self.regexList:
            self.patternsList.append(re.compile(regex, re.MULTILINE))
        

