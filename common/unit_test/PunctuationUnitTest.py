#!/usr/bin/env python2
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

__author__ = "Frédéric Dubouchet, Alexandre Nanchen"
__version__ = "Revision: 1.0"
__date__ = "Date: 2014/08"
__copyright__ = "Copyright (c) 2014 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest
from asrt.common.Punctuation import Punctuation

class PunctuationUnitTest(unittest.TestCase):
	replace_text = {
		u"." : u"point",
		u"-" : u"tiret",
		u"" : u"",
		u"pouët   pouët  pouët" : u"pouët pouët pouët",
		u"(pouët)" : u"entre parenthèses pouët",
		u"(pouët pouët)" : u"ouvrez la parenthèse pouët pouët fermez la parenthèse",
		u"\"pouët\"" : u"entre guillemets pouët",
		u"\"pouët pouët\"" : u"ouvrez les guillemets pouët pouët fermez les guillemets",
		u"? , . : ;" : u"point d'interrogation virgule point deux points point virgule"}
		
	presence_text = {
		u"pouët pouët pouët" : 0,
		u"(pouët)" : 1,
		u"(pouët pouët)" : 2,
		u"\"pouët\"" : 1,
		u"\"pouët pouët\"" : 2,
		u"?.,;:" : 5}

	remove_text = { 
		u"point":u"",
		u"tiret":u"",
		u"" : u"",
		u"pouët pouët pouët":u"pouët pouët pouët",
		u"entre parenthèses pouët":u"pouët",
		u"ouvrez la parenthèse pouët pouët fermez la parenthèse":u"pouët pouët",
		u"entre guillemets pouët":u"pouët",
		u"ouvrez les guillemets pouët pouët fermez les guillemets":u"pouët pouët",
		u"point d'interrogation virgule point deux points point virgule":u""}

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_contructor(self):
		d = [ (r"\." , 1, u"a"), (r"-" , 1, u"b") ]
		r = [ (r"a" , 1, u"."), (r"b" , 1, u"-") ]
		p = Punctuation(d, r)
		res = p.replaceText(".-.-.-..--..--")
		self.assertEqual(res, "abababaabbaabb")
		res2 = p.symbolText(res)
		self.assertEqual(res2, u".-.-.-..--..--")

	def test_countPresenceText(self):
		p = Punctuation()
		# all the dictionary is detected at least once
		for key in self.presence_text :
			result = len(p.countPresenceText(key)) == self.presence_text[key]
			if not result :
				print key, '|', p.countPresenceText(key), '|', self.presence_text[key]
			self.assertTrue(result)
		
	def test_replaceText(self):
		p = Punctuation()
		# all dictionary is replaced correctly
		for key in self.replace_text :
			result = p.replaceText(key) == self.replace_text[key].strip()
			if not result :
				print key, '|', p.replaceText(key), '|', self.replace_text[key].strip()
			self.assertTrue(result)

	def test_symbolText(self):
		p = Punctuation()
		inv_map = {v:k for k, v in self.replace_text.items()}
		for key in inv_map :
			test = " ".join(inv_map[key].split())
			result = p.symbolText(key) == test
			if not result :
				print key, '|', p.symbolText(key), '|', test
			self.assertTrue(result)

	def test_removeText(self):
		p = Punctuation()
		for key, value in self.remove_text.items():
			result = p.removeVerbalized(key) == value
			if not result:
				print key, '|', p.removeVerbalized(key), '|', value
			self.assertTrue(result)