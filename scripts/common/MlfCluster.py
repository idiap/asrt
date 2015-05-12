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
__date__ = "Date: 2012/02/24"
__copyright__ = "Copyright (c) 2011 Idiap Research Institute"
__license__ = "BSD 3-Clause"


"""Implementation module for the Master Label File cluster.
   Here are examples of such clusters:

    "003/2006_03_02_074F_001.lab"
    0 4300000 sil -55.822090
    4300000 4700000 d -80.356544
    4700000 6500000 E -72.444267
    .
    "007/2006_03_01_081F_003.lab"
    0 1800000 sil -54.283817
    1800000 3200000 Z -67.560226
    3200000 4300000 E -66.404358
    4300000 4300000 sp 0.000000
    .
"""

import sys 
import os, logging

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/.")

from Cluster import Cluster, DocumentException

class MlfCluster(Cluster):
    """Concrete type representing the phoneme MLF concept.
    """
    logger = logging.getLogger("Asrt.MlfCluster")

    FIELDSEPARATOR = " "
    ENDSYMBOL="." 
    SILENCES= ['<s>', '</s>']

    def __init__(self, key):
        attributesList = []

        #Key is mlf pattern
        Cluster.__init__(self, key.strip(), attributesList)

    ########################
    # Public methods
    #
    def readContent(self, fd):
        """Read all phonemes for a file pattern.
          
           fd: file descriptor pointing to first phoneme           
        """
        #Four elements list
        #start time, end time, utterance, score
        lineList = self._getPhonemeInformation(fd)
        
        #No more to read
        while len(lineList) != 0:
            self.addElement(lineList)
            lineList = self._getPhonemeInformation(fd)
                    
    def getScore(self):
        """Get the average phoneme score.
        """
        phonemesCount=len(self.elementList)        
        runningTotal = 0.0
                
        for phonemeList in self.elementList:
            if phonemeList[3] == None:
                raise DocumentException("Phonemes list is None!")
            runningTotal += float(phonemeList[3])
            
        return runningTotal / phonemesCount
            
    def getUtteranceText(self, bRemoveSilences=True):
        """Get the underlying uttered sounds."""
        
        utterancesList = []

        for lineList in self.elementList:
            if bRemoveSilences and self._isUtteranceSilence(lineList):
                continue                                  
            utterancesList.append(lineList[2])
        
        return " ".join(utterancesList)
                
    def getClusterInfo(self):
        """Return key."""
        return self.key

    ########################
    # Implementation
    #
    def _getPhonemeInformation(self, fd):
        """Get the start time and label text.
           The label text is checked for validity.
        """
        #Read a single line
        phonemeLine = Cluster.readLine(fd)
        
        #End of file
        #End of mlf        
        if phonemeLine == "" or phonemeLine == MlfCluster.ENDSYMBOL:
            return []
                
        phonemeLine.strip()
        lineList = phonemeLine.split(MlfCluster.FIELDSEPARATOR)
        
        #Start time, End time
        #Phoneme, Score
        if len(lineList) != 4:
            raise DocumentException("Document line should contain 4 columns!")

        return lineList

    def _isUtteranceSilence(self, lineList):
        """Check wether lineList is a silence.
        """
        bIsSilence = False
        utterance = lineList[2]
        
        for sil in MlfCluster.SILENCES:
            if sil in utterance:
                bIsSilence = True
                break
        
        return bIsSilence

    def __str__(self):
        """Override built in method.
        """
        key = self.getClusterInfo()
        return str(key)