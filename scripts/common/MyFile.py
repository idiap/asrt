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
__date__ = "Date: 2012/04"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
import shutil
import logging
import glob
import re

class MyFile:
    """Concrete type representing the file concept.
    """
    logger = logging.getLogger("Asrt.MyFile")

    def __init__(self, filePath):
        """Constructor"""
        self.filePath= filePath

    ########################
    # Implementation
    #
    def getCurrentFileName(self):
        """Get the current file name.
        """
        return os.path.basename(self.filePath)

    def getCurrentFilePath(self):
        """Get the absolute path of the current
           file path.
        """
        return os.path.abspath(self.filePath)

    def getFileDir(self):
        """The name of the enclosing file.
        """
        return os.path.dirname(self.filePath)

    ########################
    # Static methods
    #        
    @staticmethod
    def removeExtension(filePath):
        
        return os.path.splitext(filePath)
    
    @staticmethod
    def checkFileExists(filePath):
        """Check file existence."""
        
        return os.path.exists(filePath)
    
    @staticmethod
    def checkDirExists(dirPath):
        """Check directory existence, create
           if not there.
        """
        if not MyFile.checkFileExists(dirPath):
            MyFile.makeDir(dirPath)

    @staticmethod
    def makeDir(dirPath):
        """Check directory existence, create
           if not there.
        """
        os.makedirs(dirPath)

    @staticmethod
    def copyDir(srcPath, destPath):
        """Check directory existence, create
           if not there.
        """
        shutil.copytree(srcPath, destPath)

    @staticmethod
    def copyFile(srcPath, destPath):
        """Check directory existence, create
           if not there.
        """
        shutil.copy(srcPath, destPath)

    @staticmethod
    def removeFile(filePath):
        """Remove 'filePath'. Check first its
           existence Directories are removed
           as well.
        """
        if MyFile.checkFileExists(filePath):
            
            try:                            
                if os.path.isdir(filePath):
                    os.rmdir(filePath)
                else:
                    os.remove(filePath)
            except Exception, e:
                MyFile.logger.info("Could not remove file: " + str(filePath) + " " + str(e))
            
    @staticmethod
    def forceRemoveDir(dirPath):
        """Remove directory even if not empty.
        """
        if os.path.isdir(dirPath):
            shutil.rmtree(dirPath)
    
    @staticmethod
    def dirContent(dirPath, globPattern):
        """Return a list of matching files
           from 'dirPath'
        """
        globExpression = dirPath + os.sep + globPattern
        return [os.path.basename(f) for f in glob.glob(globExpression)]
    
    @staticmethod
    def listDir(dirPath, regexPattern):
        """All the directory from a folder.
        """
        dirList = os.listdir(dirPath)
        return [d for d in dirList if re.search(regexPattern, d)]
