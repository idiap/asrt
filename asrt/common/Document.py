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
__date__ = "Date: 2011/05/17"
__copyright__ = "Copyright (c) 2011 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import codecs
import types, logging

class Document:
    """Base document class
    """
    logger = logging.getLogger("Asrt.Document")

    ########################
    #Default constructor
    #
    def __init__(self, source):

        self.sourceFileName = source
        self.listContent = []
        self.listError = []

    ########################
    #Public members
    #
    def find(self, text, findFunction = None):
        """Find listContent using text and findFunction.
        """
        result = None
        if findFunction != None:
            result = findFunction(text, self.listContent)

        return result

    def printContent(self):
        """Output the file content in a tabular format.
        """
        strContent = self._getStrContent(self.listContent) 
        utf8 = str(strContent, "utf-8")
        print(utf8)

    def writeToFile(self, fullFileName, lineSeparator = " "):
        """Write the given string to the given file name.
        """
        strContent = self._getStrContent(self.listContent, lineSeparator) 

        resultFile = codecs.open(fullFileName,'w', 'utf-8')
        resultFile.write(str(strContent, "utf-8"))
        resultFile.close

    def reset(self):
        """Reset document.
        """
        self.listContent = []
        self.listError = []

    def addError(self, errorMessage):
        """Add an error to the error list.
        """
        self.listError.append(errorMessage)

    def addDocumentLine(self, strLine):
        """Add a line to the line list.
        """
        self.listContent.append(strLine)                
                                        
    def getListContent(self):
        """Return the content of the file as a list.
        """
        return self.listContent
        
    def getClusterIds(self):
        """Get a list of clusters ids using
           the getKey method of the cluster.

           It is safe to call this method even
           if the underlying data representation is
           not clustered based.          
        """
        clusterIds = []

        for cluster in self.listContent:
            if getattr(cluster, "getKey"):
                clusterIds.append(cluster.getKey())

        return clusterIds

    def getDocumentSize(self):
        """Return the number of clusters.
        """
        return len(self.listContent)
    
    def setNumericCompare(self, numeric_compare):
        """Set comparator function.
        """

        self.numeric_compare = numeric_compare

    def sortLines(self, numeric_compare):
        """Sort lines of file.
        """

        if numeric_compare != None:
            self.listContent.sort(numeric_compare)
        else :
            self.listContent.sort()

    def min(self, x, y):
        """Minimum of two numbers.
        """        
        if(x < y):
            return x

        return y

    ########################
    #Implementation
    #
    def _getStrContent(self, myList, lineSeparator):
        """Get the content of the document as a string.
        """
        strContent = ""

        for line in myList:        
            #Can be anything so long
            #that the __str__ method is
            #implemented
            strLine = str(line)

            #Line is a list
            if isinstance(line, list):
                strLine = ""       
                #Convert to strings
                for i in range(0, len(line)):
                    strLine += (str(line[i]) + lineSeparator)
                
            #Remove white space at end of line
            strContent+= (strLine.strip() + "\n")

        return strContent
