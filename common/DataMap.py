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
__date__ = "Date: 2014/04/17"
__copyright__ = "Copyright (c) 2014 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os 
import logging
import csv, copy, StringIO
from pprint import pprint
import unicodecsv

class DataMap(object):
    """A tabular structure using the 'join' concept
       of relational databases.

       A map file has the following file format:

        Data1;Representation 1;Representation 11
        Data1;Representation 1;Representation 12
        Data1;Representation 2;Representation 21
        Data2;Representation 1;Representation 11
    """
    logger = logging.getLogger("Asrt.DataMap")

    FIELDSEPARATOR = ";"
    QUOTECHAR      = '"'

    def __init__(self):
        self.dataMapFile = None
        #Dictionary representation
        self.dataMap = {}

    ########################
    # Public members
    #
    def readFile(self, mapListFile):
        """Read a map list and store results as a 
             dictionary of dictionaries.
        """
        self.dataMapFile = mapListFile
        self.dataMap = {}

        with open(mapListFile,'rb') as csvFile:
            dataMapReader = unicodecsv.reader(
                csvFile, 
                delimiter=DataMap.FIELDSEPARATOR,
                quotechar=DataMap.QUOTECHAR,
                encoding='utf-8')
            for row in dataMapReader:
                self._addMapEntry(self.dataMap, row, 0)


    def writeFile(self, mapListFile):
        """Output the dictionary map to a file.
        """
        #List representation
        dataList = self.getDictionaryMapAsList()
        dataList = sorted(dataList,key= lambda l: ";".join(l))

        with open(mapListFile,'wb') as csvFile:
            dataMapWriter = unicodecsv.writer(
                csvFile, 
                delimiter=DataMap.FIELDSEPARATOR,
                quotechar=DataMap.QUOTECHAR,
                quoting=csv.QUOTE_MINIMAL,
                encoding='utf-8')

            for row in dataList:
                dataMapWriter.writerow(row)

            csvFile.seek(-2, os.SEEK_END) # len('\r\n')
            csvFile.truncate()

    ########################
    # Getters and setters
    #
    def getDataMapFile(self):
        return self.dataMapFile

    def getDictionaryMap(self):
        """Get underlying dictionary representation.
        """
        return self.dataMap

    def getDictionaryMapAsList(self):
        """Get the dictionary map as a list representation.
        """
        dataList = []
        self._addListEntry(self.dataMap, [], dataList)
        return dataList

    def getCount(self):
        """Number of input data.
        """
        return len(self.dataMap.keys())

    def setDictionaryMap(self, dataMap):
        """Set the new structure of data and
             its representation.
        """
        self.dataMap = dataMap

    def setDictionaryMapFromList(self, dataList):
        """Set the new structure of data and
             its representation.
        """
        self.dataMap = {}

        #Convert from one representation to
        #another one
        for row in dataList:
            self._addMapEntry(self.dataMap, row)

    ########################
    # Implementation
    # 
    def _addMapEntry(self, dataDict, inputRow, offset = int(0)):
        """Convert a row list to a dictionary
             structure. 
        """
        #Stop condition
        if offset == len(inputRow):
            return

        entry = inputRow[offset]
        if entry not in dataDict:
            dataDict[entry] = {}

        #Recursive call
        self._addMapEntry(dataDict[entry], inputRow, offset + 1)

    def _addListEntry(self, dataDict, rowList, dataList):
        """Recursively got trough dictionaries
             an output a row at the leaf level.

             The result is stored in 'dataList'
        """
        for key, value in dataDict.items():
            rowList.append(key)
            #Stop condition
            if len(value.keys()) == 0:
                dataList.append(copy.deepcopy(rowList))
            else:
                #Recursive call
                self._addListEntry(value, rowList, dataList)
            #Pop child entry
            rowList.pop()

    def __str__(self):
        rep = StringIO.StringIO()
        pprint(self.dataMap,rep)
        return rep.getvalue().rstrip()
