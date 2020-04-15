#!/usr/bin/env python3
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
__date__ = "Date: 2011/04"
__copyright__ = "Copyright (c) 2011 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
import logging
import codecs
import csv
from os.path import isdir
from os import listdir


class Ioread:
    """Basic input output operations.
    """
    logger = logging.getLogger("Asrt.Ioread")

    #######################################
    # Public members
    #
    def readDirContent(self, fullDirPath):
        """Read the content of a directory and return a list of file names
        """
        fileList = []

        if isdir(fullDirPath):
            fileList = listdir(fullDirPath)

        return fileList

    def openFile(self, fullFilePath, mode='r', encoding='utf8'):
        """Get a file descriptor.

           Can raise an IOError
        """
        return open(fullFilePath, encoding="utf-8", errors="surrogateescape")

    def closeFile(self, fd):
        """Close the file using file descriptor."""
        fd.close()

    def readFileContent(self, fullFilePath):
        """Take the path of the file to read and return its content.
        """
        fileContent = ""  # Immutable

        try:
            f = open(fullFilePath, encoding="utf-8", errors="surrogateescape")
            fileContent = f.read()
            f.close()
        except IOError as ex:
            try:
                f.close()
            except Exception:
                pass
            raise ex

        return fileContent

    def readFileContentList(self, fullFilePath):
        """Take the path of the file to read and return its content.
        """
        fileContent = []

        try:
            f = open(fullFilePath, encoding="utf-8", errors="surrogateescape")
            fileContent = f.readlines()
            f.close()
        except IOError as ex:
            try:
                f.close()
            except Exception:
                pass
            raise ex

        return self.removeNewLine(fileContent)

    def readCSV(self, filePath, delim=';', quote='"'):
        """Read a csv file.
        """
        fileContent = []

        with open(filePath, newline='') as csvfile:
            csv_reader = csv.reader(
                csvfile, dialect=csv.excel, delimiter=delim, quotechar=quote)
            for row in csv_reader:
                fileContent.append(row)

        return fileContent

    def writeFileContent(self, fullFilePath, fileContent, openMode='w'):
        """Write a string to a file.
        """
        try:
            f = codecs.open(fullFilePath, openMode, 'utf-8')
            f.write(fileContent)
            f.close()
        except IOError as ex:
            try:
                f.close()
            except Exception:
                pass
            raise ex

    def removeNewLine(self, fileContent):
        """Remove trailing \n"""

        return ["%s" % line[:-1] for line in fileContent]

    def getAllFilesPathes(self, startPrefix, startingDirectory):
        """Get all files starting with 'startPrefix'. The file
           name is first converted to lowercase.

           startPrefix: the starting string a file should contain.
        """
        fileList = []

        for dirname, dirnames, filenames in os.walk(startingDirectory):
            for filename in filenames:
                if filename.lower().startswith(startPrefix):
                    fileList.append(os.path.join(dirname, filename))

        return fileList

    def getLastLine(self, filePath):
        """Get the last line of a file."""
        fileContent = self.readFileContentList(filePath)
        lastLine = ""

        if len(fileContent) > 0:
            lastLine = fileContent[-1]

        return lastLine

    def nltkRead(self, fullFilePath):
        """Read text file as one string.

           return a string representation of the file.
        """
        fp = codecs.open(fullFilePath, 'r', 'utf-8')
        data = fp.read()
        fp.close()

        return data

    #######################################
    # Implementation
    #
    def _unicode_csv_reader(self, unicode_csv_data, dialect=csv.excel, **kwargs):
        """Unicode wrapper to read unicode csv.
        """
        # csv.py doesn't do Unicode; encode temporarily as UTF-8:
        csv_reader = csv.reader(unicode_csv_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            # decode UTF-8 back to Unicode, cell by cell:
            yield [cell for cell in row]

    def _utf_8_encoder(self, unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf8')
