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
__date__ = "Date: 2015/09"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import sys, logging, re
from asrt.common.RegularExpressionList import RegexList

class RegexType():
    """A namespace for known types of regular
         expressions.

         Type 1: anywhere string: no context provided
         Type 2: raw format. User is responsible of context
         Type 3: ( |^) before or ( |$) after
         Type 4: ([.,;:()”?!-]) before and same after
         Type 5: ([0-9] +) and nothing specified after
    """
    TYPE1 = [(None,None)]
    TYPE2 = [(u'( |^)',u'( |$)')]                      # Before converting punctuation
    TYPE3 = [(u'([.,;:()”?!-])',u'([.,;:()”?!-])')]    # After converting punctuation
    TYPE4 = [(u'([0-9] +|[a-z] +|[A-Z] +)',u'( |$)')]
    TYPE5 = [(u'([0-9] +)',u'( |$)')]
    TYPE6 = [(u'([ \"\']|^)',u'([ \"\',\.\?\!;:]|$)')]

    ###############################
    # Static methods
    #
    @staticmethod
    def typeToRegularExpressions(matchingRegex, subPattern, type):
        """Return the list of regular expressions
             relevant to the type.

             Known type values are 1,2
        """
        contextsList = []

        if type == 1:
            contextsList = RegexType.TYPE1
        elif type == 2:
            contextsList = RegexType.TYPE2
        elif type == 3:
            contextsList = RegexType.TYPE3
        elif type == 4:
            contextsList = RegexType.TYPE4
        elif type == 5:
            contextsList = RegexType.TYPE5
        elif type == 6:
            contextsList = RegexType.TYPE6
        else:
            raise Exception("Unknown type %d" % type)

        typeRegexList = []

        #Before parsing text, spaces are converted to double
        #spaces. We need to match that in the regular
        #expressions
        matchingRegex = \
                RegularExpressionFormula.normalizeSpaces(matchingRegex, True) 
        nbGroups = RegexType.getNumGroups(matchingRegex)

        #Context is a tuple with the before and after
        #context. A type can have multiple context
        for context in contextsList:
            strMatch = matchingRegex
            #Left context
            if context[0] is not None:
                strMatch = context[0] + strMatch
                subPattern = "\g<1>" + subPattern
                nbGroups += 1
            #Right context
            if context[1] is not None:
                strMatch =  strMatch + context[1]
                subPattern = subPattern + "\g<%d>" % (nbGroups + 1)

            typeRegexList.append((strMatch, subPattern))

        return typeRegexList

    @staticmethod
    def getNumGroups(regex):
        return re.compile(regex).groups

class RegularExpressionFormula():
    """Formula that applies regular expressions.
    """
    logger        = logging.getLogger("Asrt.RegexFormula")

    def __init__(self, rulesFile=None, substitutionPatternList=[]):
        self.rulesFile = rulesFile
        self.substitutionPatternList = substitutionPatternList

    ####################
    #Getters and setters
    #
    def setSubstitutionPatternList(self, substitutionPatternList):
        """Set the underlying substitution regex list.

           The code assume the following format:
           [(regex, alternate, regexType),...]

           'regexType' is an integer between 1-5.
           see the RegexType class for more information.
        """
        self.logger.info("Set patterns list")
        self.substitutionPatternList = substitutionPatternList

    def getSubstitutionPatterns(self):
        return self.substitutionPatternList

    ####################
    #Public methods
    #
    def apply(self, strText, languageId, debug=False):
        """Apply regular expressions to 'strText'.

             return an utf-8 formatted string.
        """
        if len(self.substitutionPatternList) == 0:
            if self.rulesFile == None:
                return strText
            else:
                self.logger.info("Loading regexes from %s" % str(self.rulesFile))
                self.substitutionPatternList = \
                    RegexList.loadFromFile(self.rulesFile)
        
        return RegularExpressionFormula.applyRegularExpressions(strText,
                        self.substitutionPatternList, languageId, debug)

    def hasPatterns(self):
        return len(self.substitutionPatternList) != 0

    def displayPatterns(self, languageId):
        """Display the final patterns.
        """
        if len(self.substitutionPatternList) == 0:
            return
        for regex, alternate, regexType, regexLanguageId in self.substitutionPatternList:
            #Does it match the text language
            if int(regexLanguageId) != languageId:
                continue

            regexListForType = \
                RegexType.typeToRegularExpressions(regex, alternate, int(regexType))
            for regexForType in regexListForType:
                regexPattern = regexForType[0]       #What to match
                regexSubstitution = regexForType[1]  #What to substitute
                print "'" + regexPattern + "'", "-->", "'" + regexSubstitution + "'"
        print "\n"

    @staticmethod
    def applyRegularExpressions(strText, substitutionPatternList, languageId, debug=False):
        """Apply the regular expressions in function of there type.
             Type is related to the specificity of the context.

             The order of application is the file order.
        """
        #print substitutionPatternList
        if debug:
            RegularExpressionFormula.logger.info("Applying regular expressions to transcript ...")

        #For successive regular expressions
        strText = RegularExpressionFormula.normalizeSpaces(strText, True)
        
        if debug:
            RegularExpressionFormula.logger.info("Initial transcript: " + strText.encode('utf-8'))

        #For each known regular expression
        for regex, alternate, regexType, regexLanguageId in substitutionPatternList:
            regexLanguageId = int(regexLanguageId)

            #Does it match the text language
            if regexLanguageId != languageId and \
               regexLanguageId != 0:
                continue

            #Convert from type
            regexListForType = \
                RegexType.typeToRegularExpressions(regex, alternate, int(regexType))
            
            #Get regular expressions for the given type
            for regexForType in regexListForType:
                regexPattern = regexForType[0]       #What to match
                regexSubstitution = regexForType[1]  #What to substitute
                
                strLineOriginal = strText        

                #Is it some python code
                if alternate.startswith("lambda"):
                    #Use alternate version
                    strText = re.sub(regexPattern, eval(alternate), strText, flags=re.UNICODE | re.MULTILINE)
                else:
                    #print regexPattern, regexSubstitution
                    #No ignore case available
                    #print regexPattern, " --> ", strText.encode('utf-8')
                    strText = re.sub(regexPattern, regexSubstitution, strText, flags=re.UNICODE | re.MULTILINE)

                if debug:
                    if strText.encode('utf-8') != strLineOriginal.encode('utf-8'):
                        sys.stdout.write("  --> Original string: >" + strLineOriginal.encode('utf-8')+"<\n")
                        sys.stdout.write("      Match pattern: >" + regexPattern.encode('utf-8') + "<"\
                                                     "\n      Substitution: >" + regexSubstitution.encode('utf-8') + "<")
                        sys.stdout.write("\n      >" + strText.encode('utf-8') + "<\n")

        strText = RegularExpressionFormula.normalizeSpaces(strText)

        if debug:
                sys.stdout.flush()
                RegularExpressionFormula.logger.info("Final transcript: " + strText.encode('utf-8') + "\n")

        return strText

    @staticmethod
    def normalizeSpaces(strText, bDouble=False):
        """Normalize spaces in 'strText'.

             'strText' is assumed to be in utf-8 format.
        """
        if bDouble:
            strText = re.sub(ur"[ ]+", ur"  ", strText, flags = re.UNICODE)
            #Remove double spaces from groups
            return re.sub(ur"([(|])  ([|)])", ur"\g<1> \g<2>", strText, flags=re.UNICODE)

        return re.sub(ur"[ ]+", ur" ", strText, flags = re.UNICODE)

    @staticmethod
    def normalizeApostrophe(strText, oneSpace=False):
        """Normalize spaces in 'strText'.

             'strText' is assumed to be in utf-8 format.
        """
        if oneSpace:
            return re.sub(ur"'", ur"' ", strText, flags = re.UNICODE) 

        return re.sub(ur"'[ ]+", ur"'", strText, flags = re.UNICODE)
