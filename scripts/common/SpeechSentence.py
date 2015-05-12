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

class SpeechSentence:
    """A normalised text sentence with the
       associated pronunciations for the words.
    """
    logger = logging.getLogger("Asrt.SpeechSentence")

    def __init__(self, normalisedText, lexicon, separator = " "):
        """Default constructor.
        
           parameters: normalisedText : a list of normalised words
                       lexicon        : a LexiconDocument containing words 
                                        pronunciations
                       separator      : separator used between words
        """
 
        self.normalisedTextList = [t for t in normalisedText.split(separator) if len(t) > 0]
        self.pronunciationsList = []
        self.lexicon = lexicon
        self.separator = separator

    ########################
    # Public interface
    #
    def extractWordsPronunciation(self):
        """Extract words pronunciation using the lexicon given 
           into the constructor.
          
           Raise an error if no pronunciation is found.
        """
        self.pronunciationsList = []
        
        for word in self.normalisedTextList:
            pronunciationsList = self.lexicon.getLexiconPronunciationList(word)
            
            if len(pronunciationsList) == 0:
                raise Exception("'%s' does not have a pronunciation! (%s)" % (word, self.normalisedTextList))
            
            self.pronunciationsList.append(pronunciationsList[0])
    
    def getPhonemesHistogram(self):
        """Get an histogram of phonemes count.
        """
        phonemesHistogram = {} 
        
        #All words pronunciations
        for pronunciation in self.pronunciationsList:

            #Individual phonemes
            phonemesSet = pronunciation.split(" ")
            
            for phoneme in phonemesSet:
                if phoneme not in phonemesHistogram:
                    phonemesHistogram[phoneme] = 1
                else:
                    phonemesHistogram[phoneme] += 1
        
        return phonemesHistogram
        
    def getWordsHistogram(self):
        """Return an histogram of words count in
           the sentence.
        """
        wordsHistogram = {}
        
        for word in self.normalisedTextList:
            if word not in wordsHistogram:
                wordsHistogram[word] = 1 
            else:
                wordsHistogram[word] += 1

        return wordsHistogram
    
    def getWordsCount(self):
        """Number of words in the sentence.
        """
        return len(self.normalisedTextList)

    def getNormalisedText(self):
        return self.separator.join(self.normalisedTextList)

    def getPronunciation(self):
        return self.separator.join(self.pronunciationsList)