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
__date__ = "Date: 2012/01"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging
from Cluster import Cluster


class LexiconCluster(Cluster):
    """Concrete type representing the possible pronunciations
       for a word. This include possible prefixes.
    """
    logger = logging.getLogger("Asrt.LexiconCluster")
    
    def __init__(self, parent, key):
        #Remove new line character from key
        Cluster.__init__(self, key.strip(), [])
        
        self.parent = parent
 
    def addPronunciation(self, pronunciation):
        """Add a pronunciation to the cluster elements list.
        """        
        if pronunciation not in self.elementList:
               self.addElement(pronunciation)
       
    def addPrefix(self, prefix, pronunciation = None):
        """Add a prefix with its pronunciation to
           the cluster attributes dictionary.
        """
        if prefix == None:
            return
        
        self.setAttribute(prefix, pronunciation)

    def getPrefixPronunciation(self, prefix):
        """Return the pronunciation for the given prefix.
        """
        return self.getAttribute(prefix)

    def getPronunciations(self):
        """Return a list of pronunciations for the 'key'
           of the cluster.
        """
        return self.elementList

    def getCombinedPronunciations(self, prefix):
        """Get the pronunciations for the given
           prefix.
           
           That is append all cluster pronunciations
           to the prefix pronunciation.
           
           return : a list of possible pronunciations
                    or an empty list if the prefix is 
                    not specified into the cluster           
        """
        if prefix not in self.attributesDictionary:
            return []
        
        resultPronunciations = []
        
        #Fetch the prefix pronunciation once
        prefixPronunciation = self.attributesDictionary[prefix]  
        for pronunciation in self.elementList:
            combinedPronunciation = "%s %s" % (prefixPronunciation, pronunciation)
            resultPronunciations.append(combinedPronunciation)            
                        
        return resultPronunciations
           
    def getPhonemesSet(self):
        """Get the phonemes set for the stored
           pronunciations.
        """
        phonemesSet = []
            
        for pronunciation in self.getAllPronunciations():                            
            phonemesList = pronunciation.split(" ")
            for phoneme in phonemesList:
                if phoneme not in phonemesSet:
                    phonemesSet.append(phoneme)
        
        return phonemesSet
    
    def getPhonemesHistogram(self):
        """Phoneme histogram for pronunciations.
        """
        phonemesHistogram = {}
        
        for pronunciation in self.getAllPronunciations():    
            phonemesList = pronunciation.split(" ")
            
            for phoneme in phonemesList:
                if phoneme not in phonemesHistogram:
                    phonemesHistogram[phoneme] = 1
                else:
                    phonemesHistogram[phoneme] += 1
                           
        return phonemesHistogram

    def getClusterInfo(self):
       """Return a map of prefixes and a list of 
          possible pronunciations.
       """
       return self.elementList, self.attributesDictionary
    
    
    def getAllPronunciations(self):
        """All the pronunciations for this cluster.
        """
        pronunciationsDict = {}
        pronunciationsList = []
        
        self.addAllPronunciationsToDictionary(pronunciationsDict)                    
        
        #Flatten list of lists
        for l in pronunciationsDict.values():
            pronunciationsList.extend(l)
            
        return pronunciationsList
    
    
    def addAllPronunciationsToDictionary(self, pronunciationsDict):
        """Get the full word pronunciations and
           the combined pronunciations for each
           prefix.
        """
        #Add full word pronunciations
        fullWordName = self.getKey()                
        fullWordList = self.getPronunciations()
                                
        #Full word pronunciations
        LexiconCluster.addPronunciationsToDictionary(fullWordName, fullWordList,\
                                                     pronunciationsDict)        
        
        #Add combined pronunciations
        prefixDictionary = self.getAttributes()
                        
        for prefix in prefixDictionary:                    
            combinedWord = "%s%s" % (prefix, fullWordName)      
            prefixPronunciations = self.getCombinedPronunciations(prefix)               
            LexiconCluster.addPronunciationsToDictionary(combinedWord, prefixPronunciations,\
                                                         pronunciationsDict)

        return pronunciationsDict


    ########################
    # Implementation
    #
    def __str__(self):
        """Override built in method."""
        prefixMap, pronunciationList = self.getClusterInfo()

        return "%s--> %s" % (self.getKey().encode("UTF-8"), self.getAttributes())


    ########################
    # Static methods
    #       
    @staticmethod
    def addPronunciationsToDictionary(word, pronunciationList, dictionary):
        """Append a pronunciation list to the 'word' dictionary
           entry list.
        """
        if len(pronunciationList) == 0:
            return
        
        if word not in dictionary:
            dictionary[word] = []            
        
        wordList = dictionary[word]
        
        for pronunciation in pronunciationList:
            #Do not append existing pronunciations    
            if pronunciation not in wordList:
                wordList.append(pronunciation)