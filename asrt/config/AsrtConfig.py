#!/usr/bin/env python3
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
__date__ = "Date: 2015/04"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os, sys

configDir = os.path.abspath(os.path.dirname(__file__))

TEMPDIR                 = configDir + "/../../temp"
TEMPDIRUNITTEST         = "%s/unit-test/" % TEMPDIR
LOGDIR                  = configDir + "/../../log"

NLTK_DATA               = os.environ.get("NLTK_DATA", '/usr/share/nltk_data')
FRENCH_PICKLE_FOLDER    = "file:%s/tokenizers/punkt/french.pickle" % NLTK_DATA
GERMAN_PICKLE_FOLDER    = "file:%s/tokenizers/punkt/german.pickle" % NLTK_DATA
ITALIAN_PICKLE_FOLDER   = "file:%s/tokenizers/punkt/italian.pickle" % NLTK_DATA

# print( NLTK_DATA + "/corpora/europarl_raw" );   quit();
if not os.path.exists(NLTK_DATA + "/corpora/europarl_raw"):
    print("No europarl_raw corpora found!")
    sys.exit(1)

if not os.path.exists(FRENCH_PICKLE_FOLDER.split(':')[1]):
    print(("Could not find %s !" % FRENCH_PICKLE_FOLDER.split(':')[1]))
    sys.exit(1)

#Language
UNKNOWN_LABEL       	= 'unknown'
FRENCH_LABEL        	= 'french'
GERMAN_LABEL        	= 'german'
ITALIAN_LABEL       	= 'italian'
ENGLISH_LABEL       	= 'english'

UNKNOWN             	= 0
FRENCH              	= 1
GERMAN              	= 2
ENGLISH             	= 3
ITALIAN             	= 4

LANGUAGEID2LABELS   	= {UNKNOWN:UNKNOWN_LABEL, FRENCH:FRENCH_LABEL, GERMAN:GERMAN_LABEL, 
                           ENGLISH:ENGLISH_LABEL, ITALIAN:ITALIAN_LABEL}

LANGUAGE2ID         	= {UNKNOWN_LABEL:UNKNOWN,FRENCH_LABEL:FRENCH,GERMAN_LABEL:GERMAN,
                           ENGLISH_LABEL:ENGLISH, ITALIAN_LABEL:ITALIAN}

#Filtering rules
MAX_SENTENCE_LENGTH 	= 1000 #Number of characters
MIN_SENTENCE_LENGTH 	= 5    #Number of characters
MAX_WORD_LENGTH         = 50   # Max length of word, added by Yang Wang
MIN_WORDS_COUNT     	= 1
MAX_WORDS_COUNT     	= 100
MAX_DIGITS_GROUPS   	= 5    #Filter lines with too many groups of digits

#Pattern types
VALIDATION_TYPE     	= -1
