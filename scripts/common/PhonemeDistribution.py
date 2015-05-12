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
__date__ = "Date: 2013/01"
__copyright__ = "Copyright (c) 2013 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import math
import logging

from Distribution import Distribution

class PhonemeDistribution(Distribution):
    """Concept of a phoneme distribution. The phoneme
       distribution has a set of known phonemes associated 
       with their occurrences.
    """
    logger = logging.getLogger("Asrt.PhonemeDistribution")

    def __init__(self, phonemesList):        
        Distribution.__init__(self) 
        
        self._initPhonemesDict(phonemesList)

    ########################
    # Public interface
    #
    def updateDistribution(self, phonemesDict):
        """Update the current distribution with
           the given phonemes histogram.
        """   
        #Check both distributions match
        self._checkPhonemesHistogram(phonemesDict)
        
        #Now update distribution
        Distribution.updateDistribution(self, phonemesDict)
    
    def getKLDivergence(self, refDistribution):
        """Compute the KL divergence between the reference
           distribution and the current distribution.

           parameters : refDistribution: the distribution to compare with
           
           return the KL divergence and the phoneme with lowest divergence
                       
        """
        normalisedRefDistribution = refDistribution.getNormalisedHistogram()
        normalisedDistribution = self.getNormalisedHistogram()
    
        #Check both distributions matches
        self._checkPhonemesHistogram(normalisedDistribution)    
    
        klmeasure = float(0)
        lowestDivergence = float("inf")
        lowestDivergencePhoneme = None
    
        #Loop over reference distribution
        #KL divergence is not symetric
        for phoneme, refProb in normalisedRefDistribution.items():
                        
            currentProb = normalisedDistribution[phoneme]
            if currentProb == 0:
                currentProb = 1.0 / 10000
            
            #print "ref: %s  current: %s " % (str(refProb), str(currentProb))
            
            #Entropy
            informationContent = math.log((refProb/currentProb),2)
            phonemeDivergence = refProb * informationContent
            
            if phonemeDivergence < lowestDivergence:
                lowestDivergence = phonemeDivergence
                lowestDivergencePhoneme = phoneme
            
            klmeasure += phonemeDivergence
        
        return klmeasure, lowestDivergencePhoneme
        
    def getTotalPhonemesCount(self):
        """Add the total count for each phoneme and
           return the result.
        """
        return Distribution.getTotalElementsCount(self)
    
    def deepCopy(self):
        """Make a deep copy of current distribution.
        """
        deepCopy = PhonemeDistribution(self.distribution.keys())
        deepCopy.updateDistribution(self.distribution)
        
        return deepCopy
        
    ########################
    # Implementation
    #
    def _initPhonemesDict(self, phonemesList):
        """Add initial phonemes with count
           of 0.
        """
        for phoneme in phonemesList:
            self.distribution[phoneme] = 0

    def _checkPhonemesHistogram(self, phonemesDict):
        """All phonemes in 'phonemesDict' should be
           in the current distribution. 
        """
        for phoneme in phonemesDict.keys():
            if phoneme not in self.distribution:
                raise Exception("%s not found in current phoneme distribution!" % phoneme) 