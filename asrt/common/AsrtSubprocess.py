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
__date__ = "Date: 2015/01"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import subprocess, logging, traceback
from asrt.common.ioread import Ioread
from asrt.common.MyFile import MyFile

class AsrtSubprocess():
    """An utility class to group methods.
    """
    logger = logging.getLogger("Asrt.AsrtSubprocess")

    @staticmethod
    def execute(commandList, logPath, outFileName = None, errFileName = None):
        """Wrapper to execute a sub process.
        """
        #Make sure the directory exists
        MyFile.checkDirExists(logPath)

        stdout, stderr, retCode = None, None, 0

        try:
            #Default to one log
            p = subprocess.Popen(commandList, stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT)

            if errFileName is not None:
                p = subprocess.Popen(commandList, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
                
            #Run the subprocess
            stdout, stderr = p.communicate()
            retCode = p.poll()
        except Exception as e:
            AsrtSubprocess.logger.critical("Subprocess error: %s" % str(e))
            errorMessage = str(commandList) + "\n" + \
                           "------------ Begin stack ------------\n" + \
                           traceback.format_exc().rstrip() + "\n" + \
                           "------------ End stack --------------"
            print(errorMessage)
            
            #Make sure the trace is logged
            if stderr is None: 
                stderr = errorMessage
            else:
                stderr += errorMessage
            
            retCode = 1

        #Now log results
        #It is important to be ouside exception management as we
        #still want to log what happened
        io = Ioread()

        if stdout != None and len(stdout) > 0 and outFileName != None:
            io.writeFileContent("%s/%s" % (logPath, outFileName), str(stdout,'utf-8'))
        
        if stderr != None and len(stderr) > 0 and errFileName != None:
            io.writeFileContent("%s/%s" % (logPath, errFileName), str(stderr,'utf-8'))

        return retCode, stdout, stderr
