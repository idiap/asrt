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

import os, sys
import string, logging

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../config")

import nltk
from nltk.corpus import europarl_raw
from nltk.probability import DictionaryProbDist
from config import NLTK_DATA

nltk.data.path.append(NLTK_DATA)

class LanguageClassifier():
    """An English/French/German/Italian classifier.
    """
    logger = logging.getLogger("Asrt.LanguageClassifier")

    FRENCH_LABEL        = 'french'
    GERMAN_LABEL        = 'german'
    ITALIAN_LABEL       = 'italian'
    ENGLISH_LABEL       = 'english'
    UNKNOWN_LABEL       = 'unknown'
    SCORE_THRESHOLD     = 0.03

    def __init__(self):
        self.classifier = None
        self.scoreDetail = ""

    def classify(self, textUtterance, context = "", removePunctuation = True):
        """Return the class of 'textUtterance'.

           Parameters:
               - textUtterance : utf8 string
               - context       : string to display on error
        """
        if self.classifier == None:
            raise Exception("Classifier not trained.")

        #Prepare the given text
        wordsList = self._prepareText(textUtterance, context, removePunctuation)

        #Store processing information for debugging
        self.scoreDetail = ""

        #Hold count results
        labelCountDict = {LanguageClassifier.FRENCH_LABEL:0,
                          LanguageClassifier.GERMAN_LABEL:0,
                          LanguageClassifier.ITALIAN_LABEL:0,
                          LanguageClassifier.ENGLISH_LABEL:0}

        #Label unknown
        for (featuresDict, noLabel) in self.getFeatures(wordsList, None, context):
            #Classify word features
            label = self.classifier.classify(featuresDict)
            self.scoreDetail += "%s:  %s\n" % (self.getFeaturesStringRepresentation(featuresDict), label)
            labelCountDict[label] += 1

        return self._getResult(labelCountDict)

    def train(self):
        """Train using europarl_raw corpus.
        """
        LanguageClassifier.logger.info("Getting features...")
        train_set = self.getLabelledFeaturesSet()

        LanguageClassifier.logger.info("Starting training...")
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

        #Override trained probabilities
        dist = DictionaryProbDist({LanguageClassifier.FRENCH_LABEL: 0.25,
                                   LanguageClassifier.GERMAN_LABEL: 0.25,
                                   LanguageClassifier.ITALIAN_LABEL: 0.25,
                                   LanguageClassifier.ENGLISH_LABEL: 0.25})

        self.classifier._label_probdist = dist
        LanguageClassifier.logger.info("Training done...")

    ########################
    # Getters and setters
    #
    def getFeatures(self, wordsList, label, context = ""):
        """Abstract method to be implemented"""
        pass

    def getFeaturesStringRepresentation(self, featuresDict):
        """String representation for features."""
        pass

    def getLabelledFeaturesSet(self):
        """A labelled features set is a set of tuples
           of the following form:

           ({'feature_name': 'feature 1', 'feature_name': 'feature 2', ...}, label 1),
           ({'feature_name': 'feature 1', 'feature_name': 'feature 2', ...}, label 2),
           ({'feature_name': 'feature 1', 'feature_name': 'feature 2', ...}, label 1),
           ...
        """
        return self._getLabelRawTextFeatures(europarl_raw.french, LanguageClassifier.FRENCH_LABEL) +\
               self._getLabelRawTextFeatures(europarl_raw.german, LanguageClassifier.GERMAN_LABEL) +\
               self._getLabelRawTextFeatures(europarl_raw.italian, LanguageClassifier.ITALIAN_LABEL) +\
               self._getLabelRawTextFeatures(europarl_raw.english, LanguageClassifier.ENGLISH_LABEL)

    def getScoreDetails(self):
        """Detailed information about the score.
        """
        return self.scoreDetail

    ########################
    # Implementation
    #
    def _getLabelRawTextFeatures(self, language, label):
        """Raw text with sentences separated by
           spaces.
        """
        LanguageClassifier.logger.info("Number of sentences: %d for label %s" % (len(language.sents()), label))

        allFeatures = []

        for wordsList in language.sents():
            #Get all features for the sentence
            features = self.getFeatures(wordsList, label)
            allFeatures.extend(features)

        return allFeatures

    def _prepareText(self, textUtterance, context="", removePunctuation = True):
        """Prepare the text to be normalized:

           - remove punctuation
           - remove new line character at the end
           - remove prepended and trailing spaces
           - decode the string from utf8 to bytes string
        """
        textUtterance = LanguageClassifier.normalizeText(textUtterance, context, removePunctuation)
        return textUtterance.split(' ')

    def _getResult(self, labelCountDict):
        """Return label or unknown.
        """
        #Get counts
        fCount = labelCountDict[LanguageClassifier.FRENCH_LABEL]
        gCount = labelCountDict[LanguageClassifier.GERMAN_LABEL]
        iCount = labelCountDict[LanguageClassifier.ITALIAN_LABEL]
        eCount = labelCountDict[LanguageClassifier.ENGLISH_LABEL]

        totalCount = fCount + gCount + iCount + eCount

        if totalCount == 0 :
            return (LanguageClassifier.UNKNOWN_LABEL, -1)

        #Compute scores
        fScore = fCount / float(totalCount)
        gScore = gCount / float(totalCount)
        iScore = iCount / float(totalCount)
        eScore = eCount / float(totalCount)

        strScore = "f:%f/g:%f/i:%f/e:%f" % (fScore, gScore, iScore, eScore)

        allScores = [(LanguageClassifier.FRENCH_LABEL,fScore),
                     (LanguageClassifier.GERMAN_LABEL,gScore),
                     (LanguageClassifier.ITALIAN_LABEL,iScore),
                     (LanguageClassifier.ENGLISH_LABEL,eScore)]

        #Get max score
        maxIndice, maxScore = -1, -1
        for i, (label, score) in enumerate(allScores):
            if score > maxScore:
                maxIndice = i
                maxScore = score

        #Validate max score
        noMax = False
        for i, (label, score) in enumerate(allScores):
            if i != maxIndice and\
                maxScore - score <= LanguageClassifier.SCORE_THRESHOLD:
                noMax=True
                break

        #Default to unknown
        result = (LanguageClassifier.UNKNOWN_LABEL, strScore)
        if not noMax:
            result = allScores[maxIndice]

        return result

    ########################
    # Statics
    #
    @staticmethod
    def normalizeText(textUtterance, context="", removePunctuation = True):
        """Normalize text:

           - remove punctuation
           - remove new line character at the end
           - remove prepended and trailing spaces
           - encode the string from utf8 to bytes string
        """
        if removePunctuation :
            textUtterance = LanguageClassifier.removePunctuation(textUtterance)
        textUtterance = textUtterance.lower()
        textUtterance = textUtterance.rstrip()
        textUtterance = textUtterance.strip()

        textUtterance = LanguageClassifier.encodeUtf8String(textUtterance, context)

        return textUtterance

    @staticmethod
    def removePunctuation(strText, removeHyphen=False,
                                   removeAppostrophy=False,
                                   removeDots=True):
        excludeString = string.punctuation

        if not removeHyphen:
            excludeString = excludeString.replace('-','')
        else:
            #Need to keep a space
            strText = strText.replace('-', ' ')

        if not removeAppostrophy:
            excludeString = excludeString.replace('\'','')

        if not removeDots:
            excludeString = excludeString.replace('.','')

        exclude = set(excludeString)

        return ''.join(ch for ch in strText if ch not in exclude)

    @staticmethod
    def decodeString(strText, context=""):
        decodedString = ""

        try:
            decodedString = strText.decode('utf-8')

        except Exception, e:
            LanguageClassifier.logger.critical("Decoding error: " + strText + context + str(e))
            raise e

        return decodedString

    @staticmethod
    def encodeUtf8String(strText, context=""):
        encodedString = ""

        try:
            encodedString = strText.encode('utf-8')

        except Exception, e:
            LanguageClassifier.logger.critical("Encoding error: " + context)
            raise e

        return encodedString