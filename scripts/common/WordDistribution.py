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

import logging
from Distribution import Distribution

class WordDistribution(Distribution):
    """Concept of a word distribution.
    """
    logger = logging.getLogger("Asrt.WordDistribution")

    def __init__(self):
        Distribution.__init__(self) 

    ########################
    # Public interface
    #
    def getTotalWordsCount(self):
        """Add the total count for each phoneme and
           return the result.
        """
        return Distribution.getTotalElementsCount(self)
    
    def deepCopy(self):
        """Make a deep copy of current distribution.
        """
        deepCopy = WordDistribution()
        deepCopy.updateDistribution(self.distribution)
        
        return deepCopy