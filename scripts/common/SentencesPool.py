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
__date__ = "Date: 2013/02"
__copyright__ = "Copyright (c) 2013 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging

from ioread import Ioread
from SpeechSentence import SpeechSentence
from PhonemeDistribution import PhonemeDistribution
from WordDistribution import WordDistribution
from random import randint

class SentencesPool:
    """Concept of pool of sentences.
    """
    logger = logging.getLogger("Asrt.SentencesPool")

    def __init__(self, lexicon = None):
        """Default constructor.
        
           params: -lexicon: a LexiconDocument object 
        """
        self.sentencesList = []
        self.lexicon = lexicon
        
        #Map to sentencesList
        self.sentencesFilteredMap = []
        self.remaindingSentencesMap = []
        

    ########################
    # Public interface
    #
    def loadSentencesFile(self, sentencesFile):
        """Load a file containing sentences, one sentence
           per line.
        """
        
        ioread = Ioread()
        sentencesTextList = ioread.readFileContentList(sentencesFile)
        
        self.sentencesList = []
        
        for i, text in enumerate(sentencesTextList):
            if (i + 1) % 1000000 == 0:
                print "Processing sentence %d" % (i+1)
            
            #Build speech sentence object
            sentence = SpeechSentence(text, self.lexicon)
            
            if self.lexicon is not None:
                sentence.extractWordsPronunciation()
                     
            self.sentencesList.append(sentence)
        

    def filterSentenceByWordsLength(self, maxWordsLength, separator = " "):
        """Only keep sentence with a given words length.
        
           parameters: - maxWordsLength: max words length of a sentence
                       - separator     : words separator
        """
        self.sentencesFilteredMap = []
        
        for sentence in self.sentencesList:
            
            if sentence.getWordsCount() <= maxWordsLength:
                self.sentencesFilteredMap.append(sentence)
            
                
    def computeMultipleBalancedSet(self, maxNumberOfSentence, refHistogram, maxWordsLength,
                                         numberOfBalancedSets, kldivergenceThreshold):
        #All balanced sets
        balancedSetList = []
        count = 0
        
        while count < numberOfBalancedSets:
            
            #Select one set of sentences
            positiveSentencesMap, minKlDivergence = self.computeBalancedSet(maxNumberOfSentence, refHistogram,
                                                           maxWordsLength, kldivergenceThreshold ,count == 0)
                            
            balancedSetList.append((minKlDivergence, positiveSentencesMap))
            
            print "Found %d set ..." % (count+1)
            
            count = count + 1
            
        return balancedSetList
    
         
    def computeBalancedSet(self, maxNumberOfSentence, refHistogram, maxWordsLength, 
                                 kldivergenceThreshold, filterSentences=True):
        """Compute a 'balanced set' of sentences using KL divergence
           between 'refHistogram' and set histogram.
        
           params: - maxNumberOfSentence   : size of the balanced set
                   - refHistogram          : distribution we aim to achieve
                   - maxWordsLength        : max number of words for a sentence
                   - kldivergenceThreshold : what is the final threshold to reach
                   - filterSentences       : do we filter sentences first
        """
        
        if filterSentences == True:
            #Keep only a subset of pool of sentences
            self.filterSentenceByWordsLength(maxWordsLength)
        
        #What we aim for
        refDistribution = PhonemeDistribution(refHistogram.keys())
        refDistribution.updateDistribution(refHistogram)

        #Current status
        currentDistribution = PhonemeDistribution(refHistogram.keys())
        
        #Working maps
        positiveSentencesMap = []
        negativeSentencesMap = []
        
        minKlDivergence = float("inf")
        
        negativeCount = 0
        
        while len(self.sentencesFilteredMap) > 0 and\
                len(positiveSentencesMap) < maxNumberOfSentence:
            
            #Get random sentence
            indice = randint(0, len(self.sentencesFilteredMap)-1)
            sentence = self.sentencesFilteredMap[indice]
            
            #Get copy of current distribution
            testDistribution = currentDistribution.deepCopy()
            
            #Try to add sentence to balanced set
            testDistribution.updateDistribution(sentence.getPhonemesHistogram())
            
            #Get KL-divergence
            klDivergence, phoneme = testDistribution.getKLDivergence(refDistribution)
            
            if klDivergence <= minKlDivergence:
                
                positiveSentencesMap.append(sentence)
                minKlDivergence = klDivergence
                negativeCount = 0
                print "KLdivergence %f, number of sentences in set: %d" %\
                          (minKlDivergence,  len(positiveSentencesMap)) 
                
                #Check that threshold have been reached
                #Otherwise remove some sentences and continue
                if len(positiveSentencesMap) >= maxNumberOfSentence and\
                    minKlDivergence > kldivergenceThreshold:
                    print "Threshold of %f not reached (%f), removing 5 sentences." % (kldivergenceThreshold, minKlDivergence)
                    self.removeRandomSentences(positiveSentencesMap)
                
            else:
                negativeSentencesMap.append(sentence)
                
                #Fail safe mechanism
                negativeCount += 1
                
                #More than 50 sentences where refused
                #Increment minKlDivergence to be more
                #permissive
                if negativeCount > 20:
                    #print "Changing minKlDivergence from %f to %f " % (minKlDivergence, minKlDivergence + 0.05)
                    minKlDivergence+= 0.02
                    negativeCount = 0
            
            
            #In positive or negative map
            self.sentencesFilteredMap.remove(sentence)
        
        #Negative sentences are back into filtered list
        self.sentencesFilteredMap.extend(negativeSentencesMap)
        
        #Could have less sentence than asked
        return positiveSentencesMap, minKlDivergence


    def removeRandomSentences(self, positiveList):
        """ Remove randomly five elements in the
            given list and put them back into the
            filtered map.
            
            If the given list is lower than or equals
            to 5, remove one element only
        """
        
        maxIteration = 5
        
        #Five element, only remove one sentence
        if len(positiveList)<= 5:
            maxIteration = 1
            
        for indice in range(maxIteration):
            
            #Random sentence
            indice = randint(0, len(positiveList)-1)
            sentence = positiveList[indice]
            
            #Transfer from positive list to filtered map
            positiveList.remove(sentence)
            self.sentencesFilteredMap.append(sentence)
            

    def outputFilteredSentences(self):
        """Print to stdout filtered sentences.
        """
        
        for sentence in self.sentencesFilteredMap: 
            print sentence.getNormalisedText().encode("utf8")


    ########################
    # Getter and setters
    #
    
    def getFilteredSentencesCount(self):
        """Number of filtered sentences.
        """
        
        return len(self.sentencesFilteredMap)


    def getWordsHistogram(self):
        """Get an histogram of words with their
           associated count.
        """
        
        if len(self.sentencesFilteredMap) == 0:
            self._copySentencesToFiltered()
        
        #Structure to store distribution
        wordDistribution = WordDistribution()
        
        for sentence in self.sentencesFilteredMap:
            
            wordsMap = sentence.getWordsHistogram()
            wordDistribution.updateDistribution(wordsMap)
        
        return wordDistribution.distribution
    

    ########################
    # Implementation
    #

    def _copySentencesToFiltered(self):
        """Filtered set is the same as sentences
           set.
        """
        
        self.sentencesFilteredMap = []
        
        for sentence in self.sentencesList:
            self.sentencesFilteredMap.append(sentence)
    
    
    
        
