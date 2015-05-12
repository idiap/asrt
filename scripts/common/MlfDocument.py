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
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging

from Document import Document
from ioread import Ioread

from Cluster import Cluster, DocumentException
from MlfCluster import MlfCluster


class MlfDocument(Document):
    """A document holding the content of a Master Label File
       (MLF) file.
    """

    logger = logging.getLogger("Asrt.MlfDocument")

    HEADER="#!MLF!#"

    def __init__(self, mlfSourceFile):
        Document.__init__(self, mlfSourceFile)

    ########################
    #Public members
    #
    def readMlfPatterns(self):
        """Read all MLF entries.
           Here is an example of such entry:

           "007/2006_03_01_072F_009.lab"
           0 5500000 sil -48.240128
           5500000 6300000 s -69.158203                
        
           The entries are stored as MlfClusters.
           
           Can raise an IOError
        """
        file = Ioread()

        #Get a file descriptor
        fd = file.openFile(self.sourceFileName)
        
        #Header of the file
        self._readMlfHeader(fd)
        
        #First pattern
        mlfPattern = self._readMlfPattern(fd)
        
        #End of file not reached
        while mlfPattern != "":
            cluster = self._getMlfCluster(mlfPattern)
            
            #Read phonemes
            cluster.readContent(fd)
            
            #Here a document line is a cluster
            self.addDocumentLine(cluster)
            
            #Next pattern
            mlfPattern = self._readMlfPattern(fd)

        #All clusters have been fetched
        #close transcription file
        file.closeFile(fd)

    def getClusterIds(self):
        """Get a list of clusters ids.
        """
        return [cluster.getKey() for cluster in self.listContent]

    def getMlfUtterances(self, bRemoveSilences=True):
        """Get the associated utterance for each
           mlf cluster.
        """
        utteredText = []
        
        for cluster in self.listContent:
            strUtterance = cluster.getUtteranceText(bRemoveSilences)
                        
            #Do not append empty string
            if bRemoveSilences and (strUtterance == None or len(strUtterance) == 0):
                continue
            utteredText.append(strUtterance + " ")
                
        return utteredText

    def getScoresList(self):
        for cluster in self.listContent:
            print cluster.getScore()
        
    def getScores(self, threshold=-500, direction="greaterthan"):
        """Output to standard output all clusters scores
        """                    
        print threshold
        
        for cluster in self.listContent:
            score = cluster.getScore() 
            if direction == "greaterthan":
                if score > threshold :
                    print "%s: %s" % (cluster.getKey(), score)  
            else:
                if score < threshold :
                    print "%s: %s" % (cluster.getKey(), score)

            
    ########################
    #Protected members
    #        
    def _getMlfCluster(self, mlfPattern):
        """Get a cluster for a mlf pattern..

           mlfPattern: the key for the cluster
           
        """
        return MlfCluster(mlfPattern)

    def _readMlfHeader(self, fd):
        """Read the #!MLF!# from file descriptor.
        """      
        #Read first line
        header = Cluster.readLine(fd)

        if MlfDocument.HEADER != header:
            raise DocumentException("Wrong header for Mlf document!")
            
    def _readMlfPattern(self, fd):
        """Read the file name from file descriptor.
          
           The file name line starts and ends with
           double quotes.
        """      
        fileName = Cluster.readLine(fd)
        
        #End of file
        if fileName == "":
            return fileName
        
        if not (fileName.startswith("\"") and fileName.endswith("\"")):
            raise DocumentException("Incorrect pattern: '%s'" % fileName)
                            
        return fileName[1:-1]             