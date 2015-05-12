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
__date__ = "Date: 2013/06"
__copyright__ = "Copyright (c) 2013 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import copy
import logging

class Distribution:
    """Concept of a distribution. A distribution is
       a map of elements with associated counts. 
    """
    logger = logging.getLogger("Asrt.Distribution")
    
    def __init__(self):
        self.distribution = {}
        
    ########################
    # Public interface
    #
    def updateDistribution(self, elementsDict):
        """Update the current distribution with
           the given elements histogram.
        """     
        for element, count in elementsDict.items():
            if element not in self.distribution:
                self.distribution[element] = 1
            else:
                self.distribution[element] += count

    def getHistogram(self):
        """Return a deep copy of the underlying histogram.
        """
        return copy.deepcopy(self.distribution)
    
    def getNormalisedHistogram(self):
        """Return a deep copy of the histogram of phonemes count
           normalised by the total count of phonemes. 
        """
        totalElementsCount = self.getTotalElementsCount()
        normalisedDistribution = copy.deepcopy(self.distribution)
        
        if totalElementsCount == 0:
            return normalisedDistribution
        
        for element, count in normalisedDistribution.items():
            normalisedDistribution[element] = float(count) / totalElementsCount    
        
        return normalisedDistribution
        
    def getTotalElementsCount(self):
        """Add the total count for each elements and
           return the result.
        """
        totalCount = 0
        
        for element in self.distribution.keys():
            elementCount = self.distribution[element]
            totalCount += elementCount

        return totalCount
    
    def deepCopy(self):
        """Abstract method to be implemented.
           Make a deep copy of current distribution.
        """
        
        pass