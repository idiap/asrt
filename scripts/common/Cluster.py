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
__date__ = "Date: 2011/06"
__copyright__ = "Copyright (c) 2011 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import re, logging
from ioread import Ioread

########################
# Exceptions
#
class DocumentException(Exception):
    """Exception raised when some document error
       happens.The constructor takes an error 
       message.       
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
        
########################
# Main class
#        
class Cluster:
    """Abstract type representing the concept of a Cluster.\n
       A cluster can have multiple attributes."""

    logger = logging.getLogger("Asrt.Cluster")

    REGEXPATTERN = """ 
        ^                           # beginning of string
        \d+                         # one or more digits
        [a-zA-Z]?                   # an optional letter
                                    # the end of the line
        """    

    def __init__(self, key, attributeList):
        """The key
        """
        self.elementList = []
        self.key = key
        self.attributesDictionary = {}
        self.setAttributes(attributeList)
        self.keyPattern = \
            re.compile(Cluster.REGEXPATTERN, re.VERBOSE)

    ########################
    #Abstract methods
    #
    def addTuple(self, tupleLine):
        """Abstract method for appending elements to list of\n
           elements.
        """
        pass
            
    def belongToCluster(self, tuple):
        """Abstract method for checking wether tuple belongs to cluster.
        """
        pass

    def isValid(self):
        """Abstract method for checking validity of cluster.\n
           Can be used to filter clusters.
        """
        pass

    def getClusterInfo(self):
        """Some information about the cluster.
        """
        pass

    ########################
    # Others
    #
    def getKey(self):
        """Return the cluster key.
        """
        return self.key

    def getAttribute(self, key):
        """Return the value of a key. None if not found.
        """
        if key in self.attributesDictionary:
            return self.attributesDictionary[key]
        
        return None        

    def getAttributes(self):
        """Return the attributes dictionary
        """
        return self.attributesDictionary    

    def setAttribute(self, key, value):
        """Set an attribute with a specific value.
           If the attribute does not exist, add it.
        """
        self.attributesDictionary[key] = value   
        
    def setAttributes(self, attributesList):
        """Build the dictionary of attributes.\n
           attributesList is a list of tuples.
        """
        for keyValue in attributesList:
            self.attributesDictionary[keyValue[0]] = keyValue[1]        

    def isEmpty(self):
        """Check if there is already some elements in the cluster.
        """
        return self.getLength() == 0

    def addElement(self, element):
        """Add an element to the cluster element list.
        """
        self.elementList.append(element)

    def getLength(self):
        """Return the length in seconds of the cluster.
        """
        return len(self.elementList)

    def getFormattedKey(self):
        """Return a key padded with 0 to be
           three digit long and with an optional letter.

           i.e. 3    -> 003
                30a  -> 030a    
                100  -> 100
                100a -> 100a
        """
        #Need to be self for to call the implemented
        #child method
        return self._getFormattedKey(self.key)        

    def dumpAttributeContent(self, attributeName, outputFileName):
        """Write to disk the content of 'attributeName'

           return True or False depending on something 
                  was written
        """
        attributeContent = self.getAttribute(attributeName)

        if attributeContent == None:
            return False

        file = Ioread()
        file.writeFileContent(outputFileName, attributeContent)
        return True

    ########################
    # Helpers
    #
    def _getFormattedKey(self, key):
        """Return a key padded with 0 to be
           three digit long and with an optional letter.

           i.e. 3    -> 003
                30a  -> 030a    
                100  -> 100
                100a -> 100a

           This is an abstract method.
        """
        formattedKey = ""

        #Key should be in standard pattern
        #Method can be overriden, specify Cluster
        #class method
        assert Cluster._checkKeyPattern(self, key)
       
        lastKeyCharacter = key[len(key) - 1]

        #Is last character alphanumeric
        if lastKeyCharacter.isalpha():
            formattedKey = "%03d%s" % (int(key[0 : len(key) - 1]), lastKeyCharacter)
        else:
            formattedKey = "%03d" % int(key)

        return formattedKey

    def _checkKeyPattern(self, key):
        """Check label text validity.
           i.e. 34
                33a
                35F

           This is an abstract method. 
        """
        return self.keyPattern.match(key) != None
 
    ########################
    #Static members
    #
    @staticmethod
    def readLine(fd):
        """Read a single line stripping end character."""
        line = fd.readline()                
        return line.strip()
