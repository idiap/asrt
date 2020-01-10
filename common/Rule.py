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
__date__ = "Date: 2015/02"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import re
import logging

# Allow for exception filtering and
# traceback output


class RuleException(Exception):

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(RuleException, self).__init__(message)


# Atomic implementation of a rule
class Pattern():
    """An Pattern is a word within a context.
         The context can be positive or negative.

         This class is a leaf node in a 'Rule'
         decision tree.
    """
    logger = logging.getLogger("recomed.Pattern")

    def __init__(self, center, prevContext, nextContext,
                 prevOffset=-1, nextOffset=1, matchNegative=False):
        """- center        : a string in utf-8 format
             - prevContext   : a regular expression in utf-8 format
             - nextContext   : a regular expression int utf-8 format
             - prevOffset    : previous word offset
             - nextOffset    : next word offset
             - matchNegative : matching the context make it 'False'
        """
        self.center = center
        self.prevContext = prevContext
        self.nextContext = nextContext
        self.prevOffset = prevOffset
        self.nextOffset = nextOffset
        self.matchNegative = matchNegative

    def match(self, wordsList, indice, debug=False):
        """Check the word at 'indice' with previous
             and next words.

             Match presence or absence of a pattern.
             Does not take any decision.

             return True or False
        """
        # This should not happen normally as
        # One context has to be not None
        if self.prevContext == None and self.nextContext == None:
            raise RuleException('Both context should not be null!')

        # Make sure test word is in utf-8 format
        strCurrent = Pattern.getWord(wordsList, indice)

        # The center context does not apply
        if not re.match(self.getCenter(), strCurrent, flags=re.UNICODE):
            raise RuleException('Bad center %s, should be %s' % (strCurrent.encode('utf-8'),
                                                                 self.getCenter()))

        # Get contexts
        strPrevious = Pattern.getWord(wordsList, indice + self.prevOffset)
        strNext = Pattern.getWord(wordsList, indice + self.nextOffset)

        matchPrevious, matchNext = True, True

        # Previous context need checking
        if self.prevContext != None:
            matchPrevious = bool(re.match(self.prevContext, strPrevious,
                                          flags=re.UNICODE))
            if debug:
                print(("  >", matchPrevious, self.prevContext, strPrevious))
            if self.matchNegative:
                matchPrevious = not matchPrevious

        # Next context need checking
        if self.nextContext != None:
            matchNext = bool(re.match(self.nextContext, strNext,
                                      flags=re.UNICODE))
            if debug:
                print(("  >", matchNext, self.nextContext, strNext))
            if self.matchNegative:
                matchNext = not matchNext

        return matchPrevious and matchNext

    def isValid(self, testCenter):
        """Check validity of the rule given
             the 'testCenter'.
        """
        if not re.match(self.getCenter(), testCenter, flags=re.UNICODE):
            raise RuleException('Non matching center %s, should be %s!' % (
                testCenter, self.getCenter()))
        if self.getPrevContext() == None or self.getNextContext() == None:
            raise RuleException('Both context should not be null!')

    def display(self, sep=''):
        """Display the Pattern detail.
        """
        strDisplay = "Pattern (%s,%s,%s,%d,%d,%s)" % (self.getCenter(), self.getPrevContext(),
                                                      self.getNextContext(), self.prevOffset, self.nextOffset,
                                                      str(self.matchNegative))
        return strDisplay

    def getCenter(self):
        """Return center in utf-8 encoded string.
        """
        return self.center

    def getPrevContext(self):
        """The previous context in utf-8 encoded string.
        """
        if self.prevContext == None:
            return None
        return self.prevContext

    def getNextContext(self):
        """The next context in utf-8 encoded string.
        """
        if self.nextContext == None:
            return None
        return self.nextContext

    ##################
    # Static members
    #
    @staticmethod
    def getWord(wordsList, indice):
        """Get the word at 'indice' making sure
             it is in utf-8 format.
        """
        # Out of bound. Allow matchin of start,
        # end sentences.
        if indice < 0 or indice >= len(wordsList):
            return ''

        strWord = wordsList[indice]
        return strWord

# High level implementation


class Rule():
    """A rule is a set of patterns combined with
         the not, and, or logical operators.

         The patterns form the leaf of a binary
         decision tree.

         All patterns should have the same 'center'
         value.
    """

    def __init__(self, rule1, rule2=None, operator='and'):
        """Constructor.
             rule1 and rule2 can be either Pattern or
             Rule objects as both implements 'isValid'.
        """
        self.rule1 = rule1
        self.rule2 = rule2
        self.center = None
        self.bAnd = (True if operator == "and" else False)

    def match(self, wordsList, indice, debug=False):
        """Combine pattern instances and return
             True or False.

             Match presence or absence of a pattern.
             Does not take any decision.

             Raise an 'RuleException' if word at 'indice' does
             not match a 'Pattern' center.
        """
        if self.rule2 == None:
            return self.rule1.match(wordsList, indice, debug)

        ret1 = self.rule1.match(wordsList, indice, debug)
        ret2 = self.rule2.match(wordsList, indice, debug)

        # And both results
        if self.bAnd:
            return ret1 and ret2

        # Or both results
        return ret1 or ret2

    def doesApply(self, wordsList, indice):
        """The center context does not apply.

             Check is only done on the first Pattern found.

             Other pattern are assumed to have the
             same center.
        """
        # Get the first 'center' pattern
        if self.center == None:
            self.center = self.getCenter()

        # Get the test pattern
        strCurrent = Pattern.getWord(wordsList, indice)

        return re.match(self.getCenter(), strCurrent,
                        flags=re.UNICODE)

    def validate(self):
        """Check that all context's centers are the
             same and that at least one context is not
             'None'.

             raise an 'RuleException' on error.
        """
        if self.center == None:
            self.center = self.getCenter()

        if isinstance(self.rule1, Pattern):
            self.rule1.isValid(self.center)
        else:
            # Recursive call
            self.rule1.validate()

        if self.rule2 != None:
            if isinstance(self.rule2, Pattern):
                self.rule2.isValid(self.center)
            else:
                # Recursive call
                self.rule2.validate()

    def getCenter(self):
        """The first context center obtained
             by depth first recursion.
        """
        # Recursive call until Pattern type is
        # reached. Both types implement the
        #'getCenter()' method.
        return self.rule1.getCenter()

    def getOperator(self):
        """Operator of the rule: or, and
        """
        return "and" if self.bAnd else "or"

    def display(self, sep=''):
        """Recursive call to display all rules and
             pattern structure.
        """
        prefix = "Rule "

        # Not first recursion
        if len(sep) > 0:
            prefix = ""

        prefix += "%s:\n" % self.getOperator()

        # Depth first recursion on rule1
        strDisplay = prefix + sep + \
            "  --> Rule 1 %s\n" % self.rule1.display(sep + "  ")

        # Depth recursion on rule2
        if self.rule2 != None:
            strDisplay += sep + \
                "  --> Rule 2 %s" % self.rule2.display(sep + "  ")

        return strDisplay

    ##################
    # Static members
    #
    @staticmethod
    def matchRules(rulesList, wordsList, indice, debug=False):
        """Test all rules in 'rulesList'.

             The following strategy apply:

                 - Positive rules: necessary conditions but not sufficient,
                                   no negative rules should happen
                 - Negative rules: sufficient condition

             Return True, False or none if none of the rules apply.
        """
        bPositive, bNegative = None, None

        for r in rulesList:
            if not hasattr(r, 'doesApply'):
                raise RuleException(
                    "A rule cannot be a pattern. Wrap the pattern instead!")

            # Discard rules when necessary
            if not r.doesApply(wordsList, indice):
                continue

            if debug:
                print(("\nApplying set of rules for %s --------------\n" %
                       wordsList[indice].encode('utf-8')))
            # Word at 'indice' matches rule center
            retValue = r.match(wordsList, indice, debug)

            if retValue:
                bPositive = True
                if debug:
                    print(("\nPositive " + Rule.displayList(wordsList) + " (indice, " + str(indice) +
                           "): \n  Selected: " + Rule.displayList(wordsList, indice) + ", matched by " + r.display()))
            else:
                bNegative = True
                if debug:
                    print(("\nNegative " + Rule.displayList(wordsList) + " (indice, " + str(indice) +
                           "): \n  Selected: " + Rule.displayList(wordsList, indice) + ", matched by " + r.display()))

        if debug:
            print("Done applying rules ------------------")

        # None of the rules did apply
        if bPositive == None and bNegative == None:
            return None

        #'bPositive' can only be true
        if bPositive != None and bNegative == None:
            return True

        #'bNegative' can only be true --> convert to
        # false for not match
        if bPositive == None and bNegative != None:
            return False

        return bPositive and not bNegative

    @staticmethod
    def displayList(wordsList, indice=-1):
        """Display the content of a list.
        """
        if indice != -1:
            return Pattern.getWord(wordsList, indice).encode('utf-8')

        strList = "["
        for indice in range(len(wordsList)):
            strList += Pattern.getWord(wordsList,
                                       indice).encode('utf-8') + ", "
        strList += "]"

        return strList
