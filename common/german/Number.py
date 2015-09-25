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

__author__ = "Christine Marcel"
__version__ = "Revision: 1.0"
__date__ = "Date: 2015/09"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import logging
import re

from asrt.common.AsrtConstants import UNITD2W, DECADED2W

class Number():
    """A number written with digits.
    """
    logger  = logging.getLogger("Asrt.german.Number")

    ##################
    #Public interface
    #
    @staticmethod
    def convertNumberIntoLetters(number, bUndInUnits=False, ordinal=False):
        """Convert the given number into German primitives.
        """
        number = int(number)

        # Case 0
        if number >= 1: letters = ""
        else: letters = "null"

        varlet = ''

        # Case millions
        varnum = int(number / 1000000)
        if varnum > 0:
            varlet = Number.hundred_decade(varnum, bUndInUnits, ordinal)
            if varlet == "eins":
                varlet = "ein"
            letters = varlet + " million"
            if varlet != "ein": letters = letters + "en "
        else: letters = letters + " "

        # Case Tausends
        varnum = int(number) % 1000000
        varnum = int(varnum / 1000)
        if varnum > 0:
            varlet = Number.hundred_decade(varnum, bUndInUnits, ordinal)
            if varlet != "eins": letters = letters + ' ' + varlet
            letters = letters + " tausend "

        # Case hundreds and decades
        varnum = int(number) % 1000
        if varnum > 0:
            varlet = Number.hundred_decade(varnum, bUndInUnits, ordinal)
            letters = letters + ' ' + varlet

        if ordinal: letters = Number.applyOrdinalEndings(letters)

        #Normalize spaces
        lettersList = re.split(' +', letters.rstrip().strip())
        letters = " ".join(lettersList)

        if bUndInUnits:
            letters = re.sub("^ *und *", "", letters)

        return  letters.decode('utf-8')

    @staticmethod
    def applyOrdinalEndings(letters):
        splitLetters = letters.strip().split(' ')
        firstletters = " ".join(splitLetters[:-1])
        lastLetters = splitLetters[-1]
        if lastLetters.strip() in UNITD2W.values() or lastLetters.strip() == 'eins':
            if lastLetters.strip() == 'ein' or lastLetters.strip() == 'eins': letters = firstletters + ' ' + 'erste'
            elif lastLetters.strip() == 'drei': letters = firstletters + ' ' + 'dritte'
            elif lastLetters.strip() == 'acht': letters = firstletters + ' ' + 'achte'
            else: letters = letters.strip() + 'te'
        else: letters = letters.strip() + 'ste'

        return letters

    @staticmethod
    def hundred_decade(varnum, bUndInUnits,ordinal):
        varlet = ''

        # Case hundreds
        if varnum >= 100:
            varlet = UNITD2W[int(varnum / 100)] # quotient
            varnum = varnum % 100 # reste
            if varlet == "ein":
                varlet = "hundert " # einhundert = hundert
            else:
                varlet = varlet + " hundert " # ex: zweihundert

        # Case decades
        if varnum <= 19:
            if varnum > 0:
                if bUndInUnits:
                    varlet = varlet + ' und ' + UNITD2W[varnum]
                else:
                    if varnum == 1:
                        varlet = varlet + ' ' + UNITD2W[varnum] + 's' # ex:eins or hunderteins
                    else:
                        varlet = varlet + ' ' + UNITD2W[varnum] # ex:dreizehn or hundertdreizehn
        else:
            varnumD = int(varnum / 10) # quotient
            varnumU = varnum % 10 # reste
            if varnumU != 0:
                # ex: zweiundachtzig or hundertzweiundachtzig
                varlet = varlet + UNITD2W[varnumU] + " und " + DECADED2W[varnumD]
            else:
                # ex: achtzig or hundertachtzig
                varlet = varlet + ' ' + DECADED2W[varnumD]

        return varlet.strip()

    @staticmethod
    def convertDecimalNumberIntoLetters(decnumber):
        """Convert the given decimal number into
           German primitives.
        """
        decnumber = decnumber.strip().split(',')
        num = int(decnumber[0].strip())
        dec = int(decnumber[1].strip())

        return '%s komma %s' % (Number.convertNumberIntoLetters(num),Number.convertNumberIntoLetters(dec))

    