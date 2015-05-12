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
__version__ = "Revision: 1.0 "
__date__ = "Date: 2012/01"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging

from Document import Document
from LexiconCluster import LexiconCluster
from ioread import Ioread

class DictionaryDocument(Document):
    """A Dictionary document. Each line contains a word 
       without any pronunciation on the contrary of
       a lexicon document.
       
       The variable are:
           - word
           - prefix
    """
    logger = logging.getLogger("Asrt.DictionaryDocument")

    def __init__(self, dictionaryFile, prefixList):
        """Initialize the dictionary document."""
        Document.__init__(self, dictionaryFile) 
        
        self.prefixList = prefixList
        self.key_cluster_dictionary = {}
                

    ########################
    #Public members
    #
    def addDocumentLine(self, strLine):
        """Add a line to the line list."""
        if self.getCluster(strLine.getKey()) != None :
            return

        Document.addDocumentLine(self, strLine)                                         
        self.key_cluster_dictionary[strLine.getKey()] = strLine
        
        #print "Cluster added: %s" % str(strLine)

    def readFile(self):
        """Read an dictionary file (without 
           pronunciation).
                                
           The Dictionary words are stored in 
           lexicon clusters. 
        """
        if self.sourceFileName == None:
            return

        file = Ioread()

        #Get a file descriptor
        fd = file.openFile(self.sourceFileName)

        assert fd != None
        
        dictionaryEntryList = self.readLine(fd)    

        #Read all the lines of the dictionary/dictionary file
        while dictionaryEntryList != None:            
            #Get some data under the form of a cluster
            self.addCluster(dictionaryEntryList)                    
            dictionaryEntryList = self.readLine(fd)    
        
        #All clusters have been fetched
        #close dictionary file
        file.closeFile(fd)
 
    def readLine(self, fd):
        """Read one dictionary line entry.

           return a list containing the word and
                  its phonetic representation
        """      
        lexiconEntry = None

        #Read first line
        line = fd.readline()

        if line != "":
            #Read second line
            lexiconEntry = [line]
        
        return lexiconEntry

    def addCluster(self, lexiconEntryList):
        """Add or update existing cluster.
           (each cluster key is unique)
           Add possible prefix.
                   
           return the updated - added cluster                   
        """
        #Add - update existing cluster
        cluster, prefix = self.instantiateCluster(lexiconEntryList)
                    
        #Add the prefix and its pronunciation        
        self._addPrefix(cluster, prefix)
        
        return cluster

    def instantiateCluster(self, lexiconEntryList):
        """Get a cluster for the current lexicon entry.
           Make sure to remove a prefix from the graphemes
           when there is one.
           
           Return the updated - added cluster           
        """
        graphemes = lexiconEntryList[0]
        
        #Extract prefix if any
        (prefix, key) = self._getPrefixAndWord(graphemes)                        
                
        #Fetch existing
        cluster = self.getCluster(key)                            
            
        #New pronunciation cluster    
        if cluster == None:                                                  
            cluster = LexiconCluster(self, key)

            #Here a document line is a cluster
            self.addDocumentLine(cluster)                        
                    
        return cluster, prefix

    def getCluster(self, key):
        """Return the cluster associated with the key.
        """                
        if key in self.key_cluster_dictionary:
                        
            return self.key_cluster_dictionary[key]
        
        return None
                                                             
    def getClusterIds(self):
        """Get a list of clusters ids.
        """
        return [cluster.getKey() for cluster in self.listContent]

    def outputWordsList(self, fileName):
        """Output a list of unique keys into fileName
        """
        ids = self.getClusterIds()
        
        strContent= "\n".join(ids)
                
        file = Ioread()

        file.writeFileContent(fileName, strContent)
                            
    ########################
    #Protected members
    #
    def _getPrefixAndWord(self, vocabulary):
        """From a word, extract the potential prefix and
           return a tuple: (prefix, word). 
           Prefix is none if no prefix is found. The extraction
           of the prefix works only for dictionaries and not
           lexicons (with pronunciation)
        """
        prefix = None

        #In utf8, remove new line character                
        vocabulary = vocabulary.rstrip()
                
        word = vocabulary
           
        for p in self.prefixList:                        
            #Cannot have an empty word
            if vocabulary.startswith(p) and\
                len(vocabulary) != len(p) :
       
                prefix = p
                word = vocabulary[len(p):]
                break
                            
        assert word != ""
        return (prefix, word)
                    
    def _addPrefix(self, cluster, prefix):
        """Add the given prefix
        """
        if prefix == None:
            return;
    
        cluster.addPrefix(prefix)