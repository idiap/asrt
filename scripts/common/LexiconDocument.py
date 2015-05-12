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

from DictionaryDocument import DictionaryDocument
from LexiconCluster import LexiconCluster
from PhonemeDistribution import PhonemeDistribution
from ioread import Ioread

class LexiconDocument(DictionaryDocument):
    """A lexicon document is a file in which each line 
       contains a couple of graphemes phonemes.

       The variable are:
           - word
           - pronunciation
           - prefix in word
           - prefix in pronunciation
        
        When reading a lexicon file, prefixes will
        be separated from words.
        
        This insures that all root words are present
        in the lexicon.
        
        Given a dictionary file, the lexicon will generate
        it's pronunciation:
        
        For each dictionary word, it will first try to 
        generate the pronunciation with the full word and on 
        failure it will try to combine the prefix and root word
        pronuncations to generate the full word pronunciation.        
    """
    logger = logging.getLogger("Asrt.LexiconDocument")

    def __init__(self, dictionaryLexiconFile, prefixDictionary,\
                 wordPronunciationSeparator="    "):
        """Initialize a lexicon document"""

        DictionaryDocument.__init__(self, dictionaryLexiconFile, prefixDictionary.keys())
        
        self.prefixDictionary = prefixDictionary
        self.wordPronunciationSeparator = wordPronunciationSeparator                
        self.lexiconPronunciations = {}
        

    ########################
    #Overidden method
    #
    def addCluster(self, lexiconEntryList):
        """Get a cluster for the current lexicon entry.
           Make sure to remove a prefix from the graphemes
           when there is one.           
        """
        assert len(lexiconEntryList) == 2
        
        #Utf-8 with no new line character
        pronunciation = lexiconEntryList[1]
                  
        #Check and setup cluster
        #Call addPrefix       
        cluster, prefix = DictionaryDocument.instantiateCluster(self, lexiconEntryList)
                
        #Add the prefix and its pronunciation        
        self.addPrefix(cluster, prefix)
                        
        #Remove prefix pronunciation
        if prefix != None:                        
            pronunciation = self._extractPrefix(pronunciation, prefix)
                                                                                                            
        #The prefix has been added, add the pronunciation            
        cluster.addPronunciation(pronunciation)

        return cluster        


    def addPrefix(self, cluster, prefix):
        """Add the given prefix with its 
           pronunciation.
        """
        if prefix == None:
            return
    
        cluster.addPrefix(prefix, self.prefixDictionary[prefix])
        
    def readLine(self, fd):
        """Read one Lexicon entry.

           return a list containing the word and
                  its phonetic representation
        """      
        lexiconEntry = None

        #Read first line
        line = fd.readline()

        if line != "":
            #Read second line
            lexiconEntry = line.split(self.wordPronunciationSeparator)
            
            #print str(lexiconEntry)

            #1 in case of a dictionary
            #2 in case of a lexicon
            assert(len(lexiconEntry) == 2)
            
            #Remove new line character
            lexiconEntry[1] = lexiconEntry[1].rstrip()

        return lexiconEntry

    def printClusters(self):
        for cluster in self.listContent:
            if len(cluster.getAttributes()) > 0:
                print cluster

    ########################
    #Public methods
    #
    def buildLexiconPronunciations(self):
        """Build all possible pronunciations for this 
           lexicon using prefixes.
           
           Each dictionary entry has a list of
           possible pronunciations.           
        """
        self.lexiconPronunciations = {}
        
        #Add prefixes pronunciations
        for prefix in self.prefixDictionary:
            LexiconCluster.addPronunciationsToDictionary(prefix,\
                                    [self.prefixDictionary[prefix]],
                                    self.lexiconPronunciations)        
        
        #Add all other pronunciations
        for cluster in self.listContent:
            cluster.addAllPronunciationsToDictionary(self.lexiconPronunciations)
                        
    def generatePronunciations(self, dictionaryDocument):
        """Given a dictionary document, generate pronunciations 
           for its words and keep an out of vocabulary list.
           
           For each prefixed word, it tries first with the full
           word and if the full word is not found try to combine
           prefix and root word pronunciations.           
           """
                                                 
        dictionaryPronunciations = {}
        oovList = []     
                
        clustersList = dictionaryDocument.getListContent()                
        
        #For each dictionary cluster
        for cluster in clustersList:
            rootWord = cluster.getKey()
            rootWordPronunciations = []         
                        
            #First the root word
            if rootWord in self.lexiconPronunciations:
                #Get root word pronunciations
                rootWordPronunciations = self.lexiconPronunciations[rootWord]
                                
                LexiconCluster.addPronunciationsToDictionary(rootWord, rootWordPronunciations,\
                                                             dictionaryPronunciations)                
            else:                                
                oovList.append(rootWord)                                
                                                                                     
            #Get combined pronunciations
            for prefix in cluster.getAttributes():                                
                combinedWord = "%s%s" % (prefix, rootWord)
                prefixPronunciationsList = []
                
                #The lexicon has an entry for the combined word,
                #so use it
                if combinedWord in self.lexiconPronunciations:
                    prefixPronunciationsList = self.lexiconPronunciations[combinedWord]
                                    
                #Instead we can generate the pronunciations
                #using the root word pronunciation
                elif prefix in self.lexiconPronunciations:                                                        
                    for prefixPronunciation in self.lexiconPronunciations[prefix]:                                        
                        for p in rootWordPronunciations:                                          
                            combinedPronunciation = "%s %s" % (prefixPronunciation, p)
                            #print rootWord + "--> '" + combinedPronunciation + "'      '" + prefixPronunciation + "'      '" + p + "'"
                            prefixPronunciationsList.append(combinedPronunciation)                                            
                else:
                    oovList.append(combinedWord)
                    continue
                                    
                #Add combined pronunciations
                LexiconCluster.addPronunciationsToDictionary(combinedWord, prefixPronunciationsList,
                                                             dictionaryPronunciations)                                                      
        return dictionaryPronunciations, oovList
                                       
    def outputPhonemesSet(self, fileName):
        """Output the set of phonemes used
           in the word pronunciations."""
        documentPhonemesSet = self.getPhonemesSet()
        strContent = "\n".join(documentPhonemesSet)
        
        file = Ioread()
        file.writeFileContent(fileName, strContent)

    ########################
    #Getters
    #    
    def getPhonemesSet(self):
        """Get the phonemes set for all pronunciations."""
        documentPhonemesSet = []        
        
        for cluster in self.listContent:
            phonemesSet = cluster.getPhonemesSet()
            
            for phoneme in phonemesSet:
                if phoneme not in documentPhonemesSet:
                    documentPhonemesSet.append(phoneme)
        
        return documentPhonemesSet
    
    def getPhonemesHistogram(self):
        """Get the phoneme histogram for the lexicon.
        """
        distribution = PhonemeDistribution(self.getPhonemesSet())
        
        for cluster in self.listContent: 
            clusterHistogram = cluster.getPhonemesHistogram()
            distribution.updateDistribution(clusterHistogram)
            
        return distribution.getHistogram()
        
    def getWordPronunciationSeparator(self):
        """The separator between vocabulary and pronunciation."""
        return self.wordPronunciationSeparator
    
    def getLexiconPronunciations(self):
        return self.lexiconPronunciations
    
    def getLexiconPronunciationList(self, word):
        if word in self.lexiconPronunciations:            
            return self.lexiconPronunciations[word]
        
        return []

    ########################
    #Implementation
    #    
    def _extractPrefix(self, pronunciation, prefix):
        """Remove the given prefix pronunciation from
           pronunciation.
        
           return the pronunciation without the prefix
        """
        return pronunciation.replace(self.prefixDictionary[prefix],"", 1).lstrip()