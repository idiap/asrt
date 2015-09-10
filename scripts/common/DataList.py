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
__date__ = "Date: 2014/04/16"
__copyright__ = "Copyright (c) 2014 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os 
import pprint, logging
import csv, StringIO
import unicodecsv

class DataList(object):
    """A map between a base name and a file path.

       A data list file has the following file
       format:

          audio1;/path/to/audio1.wav
          audio2;/path/to/audio2.wav

       Base names are assumed to be unique in the
       data list scope.
    """
    logger = logging.getLogger("Asrt.DataList")

    FIELDSEPARATOR = ";"
    QUOTECHAR      = '"'
    COUNT          = 0

    def __init__(self):
        self.dataListFile = None
        self.dataDictionary = {}

    ########################
    # Public members
    #
    def readFile(self, dataListFile):
        """Read a data list and store
           results.
        """
        self.dataListFile = dataListFile
        self.dataDictionary = {}

        with open(dataListFile,'rb') as csvFile:
            dataListReader = unicodecsv.reader(
                csvFile, 
                delimiter=DataList.FIELDSEPARATOR,
                quotechar=DataList.QUOTECHAR,
                encoding='utf-8')

            for row in dataListReader:
                if row[0] in self.dataDictionary:
                    raise Exception(row[0] + u" is not a unique name!")

                self.dataDictionary[row[0]] = row[1]

    def writeFile(self, dataListFile):
        """Output the data list to a file.
        """
        dataList = []
        for key, value in self.dataDictionary.items():
                dataList.append([key, value])

        dataList = sorted(dataList,key= lambda l: "%s %s" % ([0], l[1]))

        with open(dataListFile,'wb') as csvFile:
            dataListWriter = unicodecsv.writer(
                csvFile, 
                delimiter=DataList.FIELDSEPARATOR,
                quotechar=DataList.QUOTECHAR,
                quoting=csv.QUOTE_MINIMAL,
                encoding='utf-8')

            for key, value in dataList:
                dataListWriter.writerow([key, value])

            csvFile.seek(-2, os.SEEK_END) # len('\r\n')
            csvFile.truncate()

    def getDataListFile(self):
        return self.dataListFile
        
    def getPath(self, baseName):
        """Return the full path of 'baseName'
           or None.
        """
        if baseName in self.dataDictionary:
            return os.path.abspath(self.dataDictionary[baseName])

        return None

    def getCount(self):
        """Number of input data.
        """
        return len(self.dataDictionary.keys())

    ########################
    # Implementation
    #
    def __str__(self):
        rep = StringIO.StringIO()
        pprint(self.dataDictionary, rep)
        return rep.getvalue().rstrip()
