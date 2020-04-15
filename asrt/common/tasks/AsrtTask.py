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
__date__ = "Date: 2012/04/03"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging, os

from asrt.common.MyFile import MyFile
from asrt.common.DataList import DataList
from asrt.common.DataMap import DataMap
from asrt.common.AsrtUtility import getErrorMessage

###############
# Helpers
#
class TaskException(Exception):
    """Exception raised for media parl tasks
       errors. The constructor takes an error 
       message.       
    """
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg


class TaskInfo(object):
    """Generic structure to hold task metadata.
    """
    
    #Parameters
    PARAMETERSEPARATOR      = ';'
    ATTRIBUTEVALUESEPARATOR = '='

    def __init__(self, parametersString, workingDirectory, targetDirectory):

        self.parametersString = parametersString
        self.workingDirectory = os.path.abspath(workingDirectory)
        self.targetDirectory = os.path.abspath(targetDirectory)

    def getParametersDict(self):
        """Return a dictionary of parameters. 
        """

        if len(self.parametersString) == 0:
            return {}

        parametersDict = {}
        parametersList = self.parametersString.split(TaskInfo.PARAMETERSEPARATOR)            
                
        for param in parametersList:            
            if TaskInfo.ATTRIBUTEVALUESEPARATOR not in param:
                raise Exception("Incorrect parameters string: %s" % self.parametersString)

            attr, value = param.split(TaskInfo.ATTRIBUTEVALUESEPARATOR)
            parametersDict[attr] = value

        return parametersDict

    def getParametersString(self):
        return self.parametersString

    def getWorkingDirectory(self):
        return self.workingDirectory
    
    def getTargetDirectory(self):
        return self.targetDirectory


###############
# Main class
#
class Task(object):
    """Abstract base class for various tasks.
    """    
    logger                          = logging.getLogger("Asrt.Task")
    
    taskNumber                      = 0

    INPUTDATAFOLDERNAME             = "input"
    OUTPUTDATAFOLDERNAME            = "output"
    TEMPDATAFOLDERNAME              = "temp"
    LOGFOLDERNAME                   = "log"
    INPUTMAPEXTENSION               = ".imap"
    OUTPUTMAPEXTENSION              = ".omap"
    INPUTLISTEXTENSION              = ".ilist"
    OUTPUTLISTEXTENSION             = ".olist"

    COMMON_PARAMETERS               = []
    
    def __init__(self, taskInfo):
        """Default constructor. Takes a task info as 
           argument.
        """
        self.taskUniqueId = Task._getNextTaskNumber()
        self.taskInfo = taskInfo
        self.taskParameters = {}
        self.taskInstanceName = "%s-%d" % (self.__class__.__name__, self.taskUniqueId)
        self.taskDirectory = None
        self.inputList = None
        self.mapLists = []
        self.resultErrorFlag = 0
        self.resultMessage = ""

    #####################
    #Interface
    #                            
    def execute(self):
        """Execute the task. A validation of the
           parameter is first done.
        """
        try:
            #Build from taskInfo
            self._buildParametersDictionary()

            #Call child implementation
            self.validateParameters()
            self.setParameters()                                          
            
            #Copy necessary data into task folder
            self.gatherInputData()

            #Actual work
            self.doWork()

            #Output data
            self.prepareOutputData()

        except Exception as e:
            errorMessage = "An error has occured"
            self._log(logging.CRITICAL, getErrorMessage(e, errorMessage))
            self.setResult(True, errorMessage)


    def validateParameters(self, parameters):
        """Check that all parameters are there.
           Overridden by implementation.
        """
        for param in Task.COMMON_PARAMETERS:
            if param not in list(self.taskParameters.keys()):
                raise Exception("Task parameter missing: '%s'!" % param)        
                                            
        #Task specific parameters
        for param in parameters:            
            if param not in list(self.taskParameters.keys()):
                raise Exception("Task parameter missing: '%s'!" % param)        

    def setParameters(self):
        """Abstract method to be implemented.
        """
        pass    

    def gatherInputData(self):
        """Prepare task directories and load data list
           and map lists.
        """
        workingDirectory = self.getWorkingDirectory()
        targetDirectory = self.getTargetDirectory()
        
        self.taskDirectory = "%s%s%s" % (workingDirectory, os.sep,
                                         self.taskInstanceName)

        #Don't want to keep old results
        MyFile.forceRemoveDir(self.taskDirectory)

        #Make task working directory
        MyFile.makeDir(self.taskDirectory)

        #Sub folders
        MyFile.makeDir(self.getInputDirectory())
        MyFile.makeDir(self.getTempDirectory())
        MyFile.makeDir(self.getOutputDirectory())

        #Read data list and data maps
        self._copyLists()
          
    def doWork(self):
        """Abstract method to be implemented.
           This method need to set the 'resultErrorFlag'
           and 'resultMessage' at the end of the work."""
        pass
    
    def prepareOutputData(self):
        """Abstract method to be implemented.
           Copy relevant output data, input list and
           input map(s) to the output folder.
        """
        pass
    
    #####################
    #Getter and setters
    #
    def getTaskInfo(self):  
        """Return the child type.
        """
        return self.taskInfo

    def getTaskInstanceName(self):
        """Return the unique name of this task.
        """
        return self.taskInstanceName

    def getWorkingDirectory(self):
        """Directory in which the task is executed.
        """
        return self.taskInfo.getWorkingDirectory()

    def getTargetDirectory(self):
        """Directory from which the task get its 
           input data.
        """
        return self.taskInfo.getTargetDirectory()

    def getTaskDirectory(self):
        """Task directory.
        """
        return self.taskDirectory

    def getInputDirectory(self):
        """Where the data, input list and maps for the
           task is stored.
        """
        return self._buildTaskPath(Task.INPUTDATAFOLDERNAME)

    def getTempDirectory(self):
        """Where the temporary data is stored.
        """
        return self._buildTaskPath(Task.TEMPDATAFOLDERNAME)

    def getLogDirectory(self):
        """Where the logs are stored.
        """
        return self._buildTaskPath(Task.LOGFOLDERNAME)

    def getOutputDirectory(self):
        """Where results are outputed.
        """
        return self._buildTaskPath(Task.OUTPUTDATAFOLDERNAME)

    def setResult(self, error, message):
        """Save error status and message."""
        self.resultErrorFlag = error
        self.resultMessage = message        
    
    #####################
    #Implementation
    #    
    def _buildParametersDictionary(self):
        """Get a dictionary from a parameter string.
        """
        self.taskParameters.clear()
        self._log(logging.INFO, "Task parameters: '%s'" %\
                  self.getTaskInfo().getParametersString())        
                
        for key, value in list(self.taskInfo.getParametersDict().items()):                 
            #Basic check
            if key == None or len(key) == 0:
                raise TaskException("Attribute None or of zero length")
            
            if value == None or len(value) == 0:
                raise TaskException("Value None or of zero length")
            
            self._log(logging.INFO, "Setting attribute: %s with %s" % (key, value))

            self.taskParameters[key] = value

    def _buildTaskPath(self, strFolder):
        """Helper to build various pathes.
        """
        if self.taskDirectory == None:
            raise Exception("Task directory is None!")

        return "%s%s%s" % (self.taskDirectory, os.sep, strFolder)

    def _copyLists(self):
        """Read input data list and all the
           representation map lists.
        """
        self._readDataList()
        self._readMapLists()

    def _readDataList(self):
        """Read the only data list from 'target directory'.
        """
        self._log(logging.INFO, "Gather input lists from %s" % self.getTargetDirectory())

        #Input list
        dataListFiles = MyFile.dirContent(self.getTargetDirectory(),
                                          "*" + Task.OUTPUTLISTEXTENSION)

        #Input data or representations
        if len(dataListFiles) == 0:
            raise Exception("No data list found in %s!" % self.getTargetDirectory())
        elif len(dataListFiles) > 1:
            raise Exception("One input list max, %d found!" % len(dataListFiles))

        self._log(logging.INFO, "Found data list: %s!" % dataListFiles[0])

        #Copy from target directory
        dataListSrcPath = self.getTargetDirectory() + os.sep + dataListFiles[0]
        dataListDestPath = self.getInputDirectory() + os.sep +\
                           MyFile.removeExtension(dataListFiles[0])[0] + Task.INPUTLISTEXTENSION

        MyFile.copyFile(dataListSrcPath, dataListDestPath)

        #Read content
        self.inputList = DataList()
        self.inputList.readFile(dataListDestPath)

    def _readMapLists(self):
        """Read the data maps from 'target directory'.
        """
        #Data maps
        dataMapFiles = MyFile.dirContent(self.getTargetDirectory(),
                                         "*" + Task.OUTPUTMAPEXTENSION)

        #Map of representations for data
        if len(dataMapFiles) == 0:
            raise Exception("No data map found in %s!" % self.getTargetDirectory())
    
        self._log(logging.INFO, "Found %d input map list(s)!" % len(dataMapFiles))

        for dataMapFile in dataMapFiles:
            self._log(logging.INFO, "Found map list: %s!" % dataMapFile)

            #Copy from target directory
            dataMapSrcPath = self.getTargetDirectory() + os.sep + dataMapFile
            dataMapDestPath = self.getInputDirectory() + os.sep +\
                              MyFile.removeExtension(dataMapFile)[0] + Task.INPUTMAPEXTENSION

            MyFile.copyFile(dataMapSrcPath, dataMapDestPath)

            #Read content
            tempDataMap = DataMap()
            tempDataMap.readFile(dataMapDestPath)
            self.mapLists.append(tempDataMap)

        self._log(logging.INFO, "Lists have been copied to %s" % self.getInputDirectory())

        #Debug information
        dataListFiles = MyFile.dirContent(self.getInputDirectory(), "*")
        self._log(logging.INFO, "Files in input directory: '%s'." %  ", ".join(dataListFiles))

    def _log(self, level, strMessage):
        """Log with task instance name.
        """
        strMessage = self.getTaskInstanceName() + ": " + strMessage
        Task.logger.log(level, strMessage)

    @staticmethod
    def _getNextTaskNumber():
        """Unique id for a task.
        """
        Task.taskNumber +=1
        return Task.taskNumber
