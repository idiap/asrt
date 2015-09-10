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
__date__ = "Date: 2011/05/21"
__copyright__ = "Copyright (c) 2008 Alexandre Nanchen"
__license__ = "BSD 3-Clause"

import os, re
import logging

from MyFile import MyFile
from ioread import Ioread
from AsrtSubprocess import AsrtSubprocess

class TextRepresentation(object):
    """A text representation of a file of any type.

       This is a list of 'utf8' sentences
    """

    logger = logging.getLogger("Asrt.TextRepresentation")    
    
    PDFTYPE             = 'pdf'
    TEXTTYPE            = 'txt'
    KNOWNTYPES          = { PDFTYPE  : 'pdf2text',
                            TEXTTYPE : 'text2text'}
    PUNCTUATION         = {'\.':' <POINT> ','[^ ](\.) [^ ]':' <POINT> ',
                           ',':' <VIRGULE> ',';':' <POINT-VIRGULE> ',
                           ':':' <2 POINTS> ',
                           '\(':' <OPARENTHESE> ','\)':' <FPARENTHESE> ',
                           '\?': ' <POINT-INTER> ','!':' <POINT-EXC> ',
                           '"':' <QUIEMET> '}

    #############################
    # Default constructor
    #                                
    def __init__(self, source, tempDir, logDir):

        self.sourceFileName = source
        self.tempDir = tempDir
        self.logDir = logDir
        self.sentencesList = []
        self.tempFilePath = None
        
    #############################
    # Interface
    #
    def convertToText(self):
        """Convert the underlying to text and load the
           file as sentences.
        """
        documentType = self._getDocumentType()
        self.tempFilePath = self.getTempFilePath()

        callback = getattr(self, TextRepresentation.KNOWNTYPES[documentType])

        #Call function to convert
        callback(self.sourceFileName, self.tempFilePath, self.logDir)

        return self.tempFilePath
        
    def loadTextFile(self):
        """Load converted text file.
        """
        if self.tempFilePath is None or not MyFile.checkFileExists(self.tempFilePath):
            raise Exception("Temporary text file does not exist!")

        io = Ioread()
        self.sentencesList = io.readFileContentList(self.tempFilePath)

    def verbalisePunctuation(self):
        """Verbalise punctuation in 'textFilePath'.
        """
        for i, strText in enumerate(self.sentencesList):
            #For all punctuation marks
            for regex, value in TextRepresentation.PUNCTUATION.items():
                strText = re.sub(regex, value, strText)
                self.sentencesList[i] = strText                        
    

    def getTempFilePath(self):
        """Temporary version of the source file.
        """
        return self.tempDir + os.sep + MyFile(self.sourceFileName).getCurrentFileName() + ".tmp"


    #############################
    # Implementation
    #                            
    def _getDocumentType(self):
        """Return the type of the underlying document.
           Raise an exception when unknown.
        """

        fileName, fileExtension = os.path.splitext(self.sourceFileName)
        documentType = None

        for knownType in TextRepresentation.KNOWNTYPES.keys():
            if knownType == fileExtension[1:]:
                documentType = knownType

        if documentType is None:
            raise Exception("Unknown document type: %s" % fileExtension[1:])
        
        return documentType


    #############################
    # Static members
    #                                
    @staticmethod
    def pdf2text(sourcePath, destinationPath, logDir):
        """Convert pdf to utf8 text.
        """
        TextRepresentation.logger.info("Converting pdf document %s" % sourcePath)

        cmdList = ['pdftotext', '-raw', '-layout', '-enc', 'UTF-8', '-eol', 'unix', '-nopgbrk']
        convertString = "Converting pdf: " + sourcePath + " into text."
                                  
        TextRepresentation.logger.info(str(cmdList) + "\n" + sourcePath + "\n" + destinationPath)

        retCode, stdout, stderr = AsrtSubprocess.execute(cmdList + [sourcePath, destinationPath], logDir)
        
        if retCode == 0:
            TextRepresentation.logger.info("Success: " + convertString)
        else: 
            TextRepresentation.logger.critical("Failure: " + convertString)
            raise Exception("Error converting pdf: " + sourcePath)


    @staticmethod
    def text2text(sourcePath, destinationPath, logDir):
        """Make a copy of 'destinationPath'.
        """
        TextRepresentation.logger.info("Copying txt file: " + sourcePath + " into text.")
        
        io = Ioread()
        strContent = io.readFileContent(sourcePath)

        #Write utf8
        io.writeFileContent(destinationPath, strContent)
