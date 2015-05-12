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
__date__ = "Date: 2012/05/31"
__copyright__ = "Copyright (c) 2012 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging

from CompiledRegexList import CompiledRegexList 

class MyAcronym:
    """A sequence of pronounced letters.
       The universal representation is a sequence of 
       capital letters separated by dots.
       
       i.e. : P.D.C., PDC, PDC., P.D.C ... 
    """
    logger = logging.getLogger("Asrt.MyAcronym")    
    
    DEFAULT_MATCHING_REGEX_LIST =(u"(^| |'|’|-|/)(",
                                  "[%c%c][.]?",
                                  ")( |-|/|)")
        
    NEW_ACRONYM_REGEX_LIST =\
        CompiledRegexList(["(^| |'|’|-|/)([a-zA-Z][.])( |-|/|)",
                           "(^| |'|’|-|/)([a-zA-Z][.][a-zA-Z][.]?)( |-|/|)",
                           "(^| |'|’|-|/)([a-zA-Z][.][a-zA-Z][.][a-zA-Z][.]?)( |-|/|)",
                           "(^| |'|’|-|/)([a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.]?)( |-|/|)",
                           "(^| |'|’|-|/)([a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.]?)( |-|/|)",
                           "(^| |'|’|-|/)([a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.][a-zA-Z][.]?)( |-|/|)"])
    
    OVERLAP_CHARACTERS_LIST = [('./','. / '), ('.-', '. - ')]

    ACRONYM_REGEX_LIST =\
        CompiledRegexList(["(^| )([a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.])( |)",
                           "(^| )([a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.])( |)",
                           "(^| )([a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.])( |)",
                           "(^| )([a-zA-Z][.] [a-zA-Z][.] [a-zA-Z][.])( |)",
                           "(^| )([a-zA-Z][.] [a-zA-Z][.])( |)",
                           "(^| )([a-zA-Z][.])( |)"])


    DEFAULT_UPPERCASE_REGEX_LIST =(u"(^| |'|-|\.)(",
                                  "[A-Z][A-Z]+",
                                  ")( |'|-|\.|)")

    def __init__(self, lettersList):

        self.lettersList = [ l.upper() for l in lettersList ]        
        self.normalizingRegex = None
        self.substitutionString = ""
        self._buildNormalizingPatterns()
        self._buildSubstitutionString()
    
    def getUniversalRepresentation(self):
        """All in uppercase.
        """
        return "".join(self.lettersList)

    def getLowerCaseRepresentation(self):
        """All in lower case.
        """
        return "".join([ l.lower() for l in self.lettersList ])

    def getNormalizedRepresentation(self):
        """How the acronym should be in a normalized text.
        """
        return ".".join([ l.lower() for l in self.lettersList ]) + "."
    
    def getNormalizedRepresentationWithSpaces(self):
        """How the acronym should be in a normalized text.
        """
        return ". ".join([ l.lower() for l in self.lettersList ]) + ". "
    
    def normalizeSentence(self, sentence):
        """Normalize sentence using regex list.                  
        """
        #For overlap (PDC-PDC)                                            
        sentence = self.normalizingRegex.substitute(sentence, self.substitutionString)
        
        #p.d.c.-PDC ==> p.d.c. - PDC
        for c1, c2 in MyAcronym.OVERLAP_CHARACTERS_LIST:
            sentence = sentence.replace(c1, c2)
        
        return self.normalizingRegex.substitute(sentence, self.substitutionString) 
                                                
    ########################
    # Implementation
    #
    def _buildNormalizingPatterns(self):
        """Acronym dependent.
        """
        regexString = self._getNormalizingRegexString()
        
        #Final list                
        self.normalizingRegex = CompiledRegexList([regexString])
    
    def _getNormalizingRegexString(self):
        """Normalizing string.
        """
        if len(self.lettersList) == 1:
            l = self.lettersList[0]            
            str = "[%c%c][.]" % (l.lower(),l)
            
            return MyAcronym.DEFAULT_MATCHING_REGEX_LIST[0] + str +\
                   MyAcronym.DEFAULT_MATCHING_REGEX_LIST[2]
        
        #More than one letter
        regexString = MyAcronym.DEFAULT_MATCHING_REGEX_LIST[0]
                        
        for i,l in enumerate(self.lettersList):
            regexString += MyAcronym.DEFAULT_MATCHING_REGEX_LIST[1] % (l.lower(), l)            
            
        regexString += MyAcronym.DEFAULT_MATCHING_REGEX_LIST[2]    
        
        return regexString
           
    def _buildSubstitutionString(self):
        """What to substitute into when normalizing.
        """
        self.substitutionString = "\g<1>" + self.getNormalizedRepresentation() + "\g<3>" 
    
    
    ########################
    # Static members
    #
    @staticmethod
    def getAcronyms(textUtterance):
        """Get new acronyms as a list.            
        """
        textUtterance = textUtterance.replace(' ', '  ')
        matchList = MyAcronym.NEW_ACRONYM_REGEX_LIST.findAll(textUtterance)
        aList = [ MyAcronym(p.replace('.','').upper()) 
                    for (s,p,e) in matchList]
        
        return MyAcronym._getUniqueAcronyms(aList)        
    
    
    @staticmethod
    def getAcronymsFromNormalizedText(textUtterance):
        """Get acronyms as a list.            
        """                
        #Text list
        matchList = MyAcronym.ACRONYM_REGEX_LIST.findAllByDecreasingOrder(textUtterance)
                        
        aList = [ MyAcronym(p.replace('. ','').replace('.','').upper()) 
                    for (s,p,e) in matchList]
                                
        return MyAcronym._getUniqueAcronyms(aList)
            

    @staticmethod
    def _getUniqueAcronyms(acronymsList):
        """Get acronyms using 'regexList'
        """
        checked = []
        uList   = []
       
        for a in acronymsList:
            #print a.getUniversalRepresentation()
            if a.getUniversalRepresentation() not in checked:                
                checked.append(a.getUniversalRepresentation())
                uList.append(a)
        
        return uList        

    @staticmethod
    def getUpperCaseWords(textUtterance):
        all_uppercase_regex_list =\
            CompiledRegexList([MyAcronym.DEFAULT_UPPERCASE_REGEX_LIST[0] +
                               MyAcronym.DEFAULT_UPPERCASE_REGEX_LIST[1] +
                               MyAcronym.DEFAULT_UPPERCASE_REGEX_LIST[2]])
        
        textUtterance = textUtterance.replace(' ', '  ')
        matchList = all_uppercase_regex_list.findAll(textUtterance)                
        uList   = []
       
        for s,a,e in matchList:
            if a not in uList:                
                uList.append(a.strip())
        
        return uList
    
    @staticmethod
    def normalizeOneSentenceWord(oldText, newText, sentenceText):
        """Normalize sentence using regex list.                  
        """
        substitute_uppercase_regex_list =\
            CompiledRegexList([MyAcronym.DEFAULT_UPPERCASE_REGEX_LIST[0] + oldText +\
                              MyAcronym.DEFAULT_UPPERCASE_REGEX_LIST[2]])
        substitutionString = u"\g<1>" + newText + u"\g<3>"
        sentenceText = substitute_uppercase_regex_list.substitute(sentenceText, substitutionString)
        
        #p.d.c.-PDC ==> p.d.c. - PDC
        for c1, c2 in MyAcronym.OVERLAP_CHARACTERS_LIST:
            sentenceText = sentenceText.replace(c1, c2)
        
        return substitute_uppercase_regex_list.substitute(sentenceText, substitutionString) 
    
    @staticmethod
    def hasUpperCaseWords(textUtterance):
        """Return true if the sentence has upper case words. 
        """
        return len(MyAcronym.getUpperCaseWords(textUtterance))>0