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
__date__ = "Date: 2012/05/16"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging
from Classifier import LanguageClassifier

class WordClassifier(LanguageClassifier):
    """A text classifier using words features.
    """
    logger = logging.getLogger("Asrt.WordClassifier")

    FEATURE_NAME    = "words"
    FEATURE_NAME1   = "first3_char"
    FEATURE_NAME2   = "last3_char"
    FEATURE_NAME3   = "char_count"
            
    def __init__(self):
        LanguageClassifier.__init__(self)
        
    def getFeatures(self, wordsList, label, context = ""):
        """For every word in 'wordsList', get it associated
           features and return a list of dictionaries (features)        
          [
           ({'feature_name': 'feature 1 for word 1', 'feature_name': 'feature 2 for word 1', ...}, label 1),
           ({'feature_name': 'feature 1 for word 2', 'feature_name': 'feature 2 for word 2', ...}, label 1),
          ...
          ]
        """
        featuresList = []

        #Byte string        
        for strWord in wordsList:
            #Features
            first3, last3 = self._getTrigrams(strWord)
            charCount = len(strWord)
                                                                                
            featuresList.append(({WordClassifier.FEATURE_NAME : strWord, 
                                  WordClassifier.FEATURE_NAME1: first3,
                                  WordClassifier.FEATURE_NAME2: last3,
                                  WordClassifier.FEATURE_NAME3: charCount}, label))             
        return featuresList

    def getFeaturesStringRepresentation(self, featuresDict):
        """String representation for features.
        """
        return featuresDict[WordClassifier.FEATURE_NAME] + ";" + \
               featuresDict[WordClassifier.FEATURE_NAME1] + ";" + \
               featuresDict[WordClassifier.FEATURE_NAME2] + ";" + \
                str(featuresDict[WordClassifier.FEATURE_NAME3])

    ########################
    # Implementation
    #
    def _getTrigrams(self, strWord):
        """Get first three and last three letters
           of a word.
        """
        first3 = strWord
        last3  = strWord
                    
        if len(strWord) > 3:
            first3 = strWord[:3]
            last3 = strWord[-3:]
                        
        return first3, last3