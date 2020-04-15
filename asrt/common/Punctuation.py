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



__author__      = "Frédéric Dubouchet, Alexandre Nanchen"
__version__     = "Revision: 1.0"
__date__        = "Date: 2014/08/11"
__copyright__   = "Copyright (c) 2014 Idiap Research Institute"
__license__     = "BSD 3-Clause"

import sys
import re, logging

from asrt.common.ioread import Ioread

SIMPLE_t = 0
SIMPLE_NS_t = 1
SIMPLE_NSL_t = 2
SIMPLE_NSR_t = 3
PREFIX_t = 4
POSTFIX_t = 5
MIDDLE_t = 6

class Punctuation(object):
    """A class reprensenting a punctuation model.
    """
    logger = logging.getLogger("Asrt.Punctuation")

    default_puncutation = [
        (r"\." , SIMPLE_t, "point"),
        (r"\," , SIMPLE_t, "virgule"),
        (r"\;" , SIMPLE_t, "point virgule"),
        (r"\:" , SIMPLE_t, "deux points"),
        (r"\n" , SIMPLE_t, "à la ligne"),
        (r"\r\n" , SIMPLE_t, "à la ligne"),
        (r"\((\S+)\)" , PREFIX_t, "entre parenthèses"),
        (r"\"(\S+)\"" , PREFIX_t, "entre guillemets"),
        (r"\?" , SIMPLE_t, "point d'interrogation"),
        (r"\!" , SIMPLE_t, "point d'exclamation"),
        (r"\((\S+)\s" , PREFIX_t, "ouvrez la parenthèse"),
        (r"\"(\S+)\s" , PREFIX_t, "ouvrez les guillemets"),
        (r"\s(\S+)\)" , POSTFIX_t, "fermez la parenthèse"),
        (r"\s(\S+)\"" , POSTFIX_t, "fermez les guillemets"),
        (r"(?:\s|^)-(?:\s|)" , SIMPLE_t, "tiret") ]

    default_reverse = [
        (r"(?:\s|^)point\svirgule(?:\s|)" , SIMPLE_t, ";"),
        (r"(?:\s|^)deux\spoints(?:\s|)" , SIMPLE_t, ":"),
        (r"(?:\s|^)double\spoints(?:\s|)", SIMPLE_t, ":"),
        (r"(?:\s|^)retour\sà\sla\sligne(?:\s|)", SIMPLE_t, "\n"),
        (r"(?:\s|^)à\sla\sligne(?:\s|)" , SIMPLE_t, "\n"),
        (r"(?:\s|^)entre\sparenthèses\s(\S+)(?:\s|)" , MIDDLE_t, "()"),
        (r"(?:\s|^)entre\sguillemets\s(\S+)(?:\s|)" , MIDDLE_t, "\"\""),
        (r"(?:\s|^)point\sd'interrogation(?:\s|)" , SIMPLE_t, "?"),
        (r"(?:\s|^)point\sd'exclamation(?:\s|)" , SIMPLE_t, "!"),
        (r"(?:\s|^)ouvrez\sla\sparenthèse(?:\s|)" , SIMPLE_NSR_t, "("),
        (r"(?:\s|^)ouvrez\sles\sguillemets(?:\s|)" , SIMPLE_NSR_t, "\""),
        (r"(?:\s|^)fermez\sla\sparenthèse(?:\s|)" , SIMPLE_NSL_t, ")"),
        (r"(?:\s|^)fermez\sles\sguillemets(?:\s|)" , SIMPLE_NSL_t, "\""),
        (r"(?:\s|^)point(?:\s|)" , SIMPLE_t, "."),
        (r"(?:\s|^)virgule(?:\s|)" , SIMPLE_t, ","),
        (r"(?:\s|^)tiret(?:\s|)" , SIMPLE_t, "-") ]

    default_remove = [
        (r"(?:\s|^)point\svirgule(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)deux\spoints(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)double\spoints(?:\s|)", SIMPLE_t, " "),
        (r"(?:\s|^)retour\sà\sla\sligne(?:\s|)", SIMPLE_t, " "),
        (r"(?:\s|^)à\sla\sligne(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)entre\sparenthèses\s(\S+)(?:\s|)" , MIDDLE_t, "  "),
        (r"(?:\s|^)entre\sguillemets\s(\S+)(?:\s|)" , MIDDLE_t, "  "),
        (r"(?:\s|^)point\sd'interrogation(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)point\sd'exclamation(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)ouvrez\sla\sparenthèse(?:\s|)" , SIMPLE_NSR_t, " "),
        (r"(?:\s|^)ouvrez\sles\sguillemets(?:\s|)" , SIMPLE_NSR_t, " "),
        (r"(?:\s|^)fermez\sla\sparenthèse(?:\s|)" , SIMPLE_NSL_t, " "),
        (r"(?:\s|^)fermez\sles\sguillemets(?:\s|)" , SIMPLE_NSL_t, " "),
        (r"(?:\s|^)point(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)virgule(?:\s|)" , SIMPLE_t, " "),
        (r"(?:\s|^)tiret(?:\s|)" , SIMPLE_t, " ") ]

    def __init__(self, punctuation_model = None, reverse_model = None):
        """Constructor
                punctuation_model       take a list containing the
                                            punctuation if not provided will take
                                            the default (default_punctuation)
        """
        if punctuation_model :
            self.punctuation = punctuation_model
        else:
            self.punctuation = self.default_puncutation
        if reverse_model :
            self.reverse = reverse_model
        else:
            self.reverse = self.default_reverse

    ########################
    # Private interface
    #
    def __simpleRepl(self, match):
        """ just replace with the text no word associated with it
        """
        return ' ' + self.replace_temp + ' '

    def __simpleNSRepl(self, match):
        """ replace with the text and remove all space
        """
        return self.replace_temp

    def __simpleNSRRepl(self, match):
        """ replace with no space on the right
        """
        return ' ' + self.replace_temp

    def __simpleNSLRepl(self, match):
        """ replace with no space on the left
        """
        return self.replace_temp + ' '

    def __prefixRepl(self, match):
        """ replace a value prefixed with some text
        """
        return ' ' + self.replace_temp + ' ' + match.group(1) + ' '

    def __postfixRepl(self, match):
        """ replace a valus postfixed with some text
        """
        return ' ' + match.group(1) + ' ' + self.replace_temp + ' '

    def __middleRepl(self, match):
        """ replace a value in the middle of a text
        """
        return ' ' + self.replace_temp[0] + match.group(1).strip() + self.replace_temp[1] + ' '

    def __replaceList(self, list_word, input_text):
        """ replace a list of word by another using regexp
        """
        output_text = input_text
        for elem in list_word :
            key = elem[0]
            kind = elem[1]
            value = elem[2]
            # cheat to pass value to the repl
            self.replace_temp = value
            if kind == SIMPLE_t :
                output_text = re.sub(key, self.__simpleRepl, output_text)
            elif kind == SIMPLE_NS_t :
                output_text = re.sub(key, self.__simpleNSRepl, output_text)
            elif kind == SIMPLE_NSR_t :
                output_text = re.sub(key, self.__simpleNSRRepl, output_text)
            elif kind == SIMPLE_NSL_t :
                output_text = re.sub(key, self.__simpleNSLRepl, output_text)
            elif kind == MIDDLE_t :
                output_text = re.sub(key, self.__middleRepl, output_text)
            elif kind == PREFIX_t :
                output_text = re.sub(key, self.__prefixRepl, output_text)
            elif kind == POSTFIX_t :
                output_text = re.sub(key, self.__postfixRepl, output_text)
        split_text = output_text.split()
        return " ".join(split_text)

    ########################
    # Public interface
    #
    def countPresenceText(self, input_text):
        """Count the presence of all the punctuation in the punctuation model
            present in the [input_text]
                return                  dictionary containing key and count
        """
        count_dict = {}
        for elem in self.punctuation :
            key = elem[0]
            value = elem[2]
            count = len(re.findall(key, input_text))
            if count :
                count_dict[value] = count
        return count_dict

    def countPresentFile(self, input_file):
        """Count the presence of all the punctuation in the punctuation model
            present in the file named [input_file]
                input_file              Input file to be used as source
                return                  dictionary containing key and count
        """
        try:
            io = Ioread()
            file_content = io.readFileContent(input_file)
            return self.countPresenceText(file_content)
        except Exception as e :
            print(("exception<" + input_file + "> : " + str(e)))
            return {}

    def symbolText(self, input_text):
        """check for verbalisation of punctuation and replace it with apropriate
            symbol.
                return                  the modified text.
        """
        return self.__replaceList(self.reverse, input_text)

    def replaceText(self, input_text):
        """Replace the punctuation in the text by the one in the punctuation
            model
                return                  the modified text.
        """
        return self.__replaceList(self.punctuation, input_text)

    def removeVerbalized(self, input_text):
        """Remove verbalized punctuation.

           return the text without punctuation
        """
        output_text = self.__replaceList(self.default_remove, input_text)
        return " ".join(output_text.split())

    def replaceFile(self, input_file, output_file = None):
        """Replace the punctuation in the file named [input_file] and return the
            result in the file named [output_file]
                input_file              Input file to be used as source
                output_file             Output file (if None return Text
                return                  True if success False is failure in case
                                            output_file is present output_text if
                                            not present
        """
        try:
            io = Ioread()
            input_text = io.readFileContent(input_file)
            if output_file :
                f = open(output_file, "w")
                f.write(self.replaceText(input_text))
                return True
            else:
                return self.replaceText(input_text)
        except Exception as e :
            print(("exception<" + input_file + "> : " + str(e)))
            if output_file :
                return False
            else :
                return None
