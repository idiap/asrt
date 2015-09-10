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
__date__ = "Date: 2015/04"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../config")

import logging
import logging.handlers

from MyFile import MyFile

########################
#Formatter that align output
#
class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = "%d: " % os.getpid()
        str += logging.Formatter.format(self, record)        
        header, footer = str.split(record.message)        
        str = str.replace('\n', '\n' + ' '*len(header))
    
        return str
    
def setupLogging(logLevel, fileName, logToStd = True):
    """Logging for the server module. Default
       level is INFO.
    """
    #Message queue
    taskLogger = logging.getLogger("Asrt")

    taskLogger.setLevel(logLevel)
       
    #Rendering engines
    mediaparlFormatter = MultiLineFormatter("%(lineno)-4d : %(levelname)-10s %(name)-30s %(asctime)-25s %(message)s")    
       
    #Check and make directory
    MyFile.checkDirExists(MyFile(fileName).getFileDir())
        
    fileHandler = logging.handlers.RotatingFileHandler(filename=fileName,maxBytes=1024000, backupCount=5)
    fileHandler.setLevel(logLevel)
    fileHandler.setFormatter(mediaparlFormatter)

    taskLogger.addHandler(fileHandler)
    
    if logToStd:        
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setLevel(logLevel)
        streamHandler.setFormatter(mediaparlFormatter)
        taskLogger.addHandler(streamHandler)
        
    return taskLogger
