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

import os, sys

scriptsDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptsDir + "/../config")

from config import FRENCH

SPACEPATTERN      	= u"[ ]+"

UNITD2W             = {1:'ein', 2:'zwei', 3:'drei', 4:'vier', 5:'fünf', 6:'sechs', 7:'sieben', 8:'acht', 9:'neun',
                       10:'zehn', 11:'elf', 12:'zwölf', 13:'dreizehn', 14:'vierzehn', 15:'fünfzehn', 16:'sechszehn',
                       17:'siebzehn', 18:'achtzehn', 19:'neunzehn'}

DECADED2W           = {1:'zehn', 2:'zwanzig', 3:'dreissig', 4:'vierzig', 5:'fünfzig', 6:'sechzig', 7:'siebzig',
                       8:'achtzig', 9:'neunzig'}

#See https://en.wikipedia.org/wiki/List_of_Unicode_characters
#http://www.cloford.com/resources/charcodes/utf-8_punctuation.htm
#http://xahlee.info/comp/unicode_matching_brackets.html
#Format is matching pattern, substitution, comment, language id
UTF8MAP         	= [
(ur"\u00A0",u" ",u"Spaces: non-breaking space",u"0"),
(ur"\ufeff",u" ",u"Spaces: invisible",u"0"),
(ur"\u200B",u" ",u"Spaces: zero-width space",u"0"),
(ur"\u200c",u" ",u"Spaces: zero-width non-joiner",u"0"),
(ur"\u200d",u" ",u"Spaces: zero-width joiner",u"0"),
(ur"\u2002",u" ",u"Spaces: en space",u"0"),
(ur"\u2003",u" ",u"Spaces: em space",u"0"),
(ur"\u2000",u" ",u"Spaces: en quad",u"0"),
(ur"\u2001",u" ",u"Spaces: em quad",u"0"),
(ur"\u2004",u" ",u"Spaces: three-per-em space",u"0"),
(ur"\u2005",u" ",u"Spaces: four-per-em space",u"0"),
(ur"\u2006",u" ",u"Spaces: six-per-em space",u"0"),
(ur"\u2007",u" ",u"Spaces: figure space",u"0"),
(ur"\u2008",u" ",u"Spaces: punctuation space",u"0"),
(ur"\u2009",u" ",u"Spaces: thin space",u"0"),
(ur"\u200A",u" ",u"Spaces: hair space",u"0"),
(ur"\u200e",u" ",u"Spaces: left to right mark, narrow no-break space",u"0"),
(ur"\u200f",u" ",u"Spaces: right to left mark, narrow no-break space",u"0"),
(ur"\u205f",u" ",u"Spaces: math space",u"0"),
(ur"\u3000",u" ",u"Spaces: ideographic space",u"0"),
(ur"\u060c",u",",u"Comma: arabic comma",u"0"),
(ur"\u066b",u",",u"Comma: arabic decimal separator",u"0"),
(ur"\u066c",u",",u"Comma: arabic thousands separator",u"0"),
(ur"\u3001",u",",u"Comma: ideographic comma",u"0"),
(ur"\ufe50",u",",u"Comma: small comma",u"0"),
(ur"\uff0c",u",",u"Comma: fullwidth comma",u"0"),
(ur"\u06d4",u".",u"Full stop: arabic full stop",u"0"),
(ur"\u2024",u".",u"Full stop: one dot leader",u"0"),
(ur"\ufe52",u".",u"Full stop: small full stop",u"0"),
(ur"\uff0e",u".",u"Full stop: fullwidth full stop",u"0"),
(ur"\u3002",u".",u"Full stop: ideographic full stop",u"0"),
(ur"\ufe55",u":",u"Colon: small colon",u"0"),
(ur"\uff1a",u":",u"Colon: fullwidth colon",u"0"),
(ur"\u0387",u";",u"Semi colon: greek ano teleia",u"0"),
(ur"\u061B",u";",u"Semi colon: arabic semicolon",u"0"),
(ur"\ufe54",u";",u"Semi colon: small semicolon",u"0"),
(ur"\uff1b",u";",u"Semi colon: fullwidth semicolon",u"0"),
(ur"\u2010",u"-",u"Hyphen: hyphen",u"0"),
(ur"\u2011",u"-",u"Hyphen: non-breaking hyphen",u"0"),
(ur"\u2012",u"-",u"Hyphen: figure dash",u"0"),
(ur"\u2013",u"-",u"Hyphen: en dash",u"0"),
(ur"\uff0d",u"-",u"Hyphen: fullwidth hyphen minus",u"0"),
(ur"\u2014",u"-",u"Hyphen: em dash",u"0"),
(ur"\u2015",u"-",u"Hyphen: horizontal bar ",u"0"),
(ur"\u2018",u"'",u"Quotation mark: left single quotation mark",u"0"),
(ur"\u2019",u"'",u"Quotation mark: right single quotation mark",u"0"),
(ur"\u201a",u"'",u"Quotation mark: single low-9 quotation mark",u"0"),
(ur"\u201b",u"'",u"Quotation mark: single reversed-9 quotation mark",u"0"),
(ur"\u201c",u"'",u"Quotation mark: left double quotation mark",u"0"),
(ur"\u201d",u"'",u"Quotation mark: right double quotation mark",u"0"),
(ur"\u201e",u"'",u"Quotation mark: double low-9 quotation mark",u"0"),
(ur"\u2032",u"'",u"Quotation mark: prime",u"0"),
(ur"\u2033",u"'",u"Quotation mark: double prime",u"0"),
(ur"\u2034",u"'",u"Quotation mark: triple prime",u"0"),
(ur"\u2035",u"'",u"Quotation mark: reversed prime",u"0"),
(ur"\u2036",u"'",u"Quotation mark: reversed double prime",u"0"),
(ur"\u2037",u"'",u"Quotation mark: reversed triple prime",u"0"),
(ur"\u2039",u"'",u"Quotation mark: single left-pointing angle quotation mark",u"0"),
(ur"\u203A",u"'",u"Quotation mark: single right-pointing angle quotation mark",u"0"),
(ur"\u00b4",u"'",u"Quotation mark: acute accent",u"0"),
(ur"\uff07",u"'",u"Quotation mark: fullwidth apostrophe",u"0"),
(ur"\u00ab",u"\"",u"Quotation mark: left-pointing double angle quotation mark",u"0"),
(ur"\u00bb",u"\"",u"Quotation mark: right-pointing double angle quotation mark",u"0"),
(ur"\u037e",u"?",u"Question mark: greek question mark",u"0"),
(ur"\u00bf",u"?",u"Question mark: inverted question mark",u"0"),
(ur"\u061f",u"?",u"Question mark: arabic question mark",u"0"),
(ur"\u203d",u"?",u"Question mark: interrobang combined question and exclamation marks",u"0"),
(ur"\ufe56",u"?",u"Question mark: small question mark",u"0"),
(ur"\uff1f",u"?",u"Question mark: fullwidth question mark",u"0"),
(ur"\uff01",u"!",u"Exclamation mark: fullwidth exclamation mark",u"0"),
(ur"\ufe6b",u"@",u"Commercial at: small commercial at",u"0"),
(ur"\uff20",u"@",u"Commercial at: fullwidth commercial at",u"0"),
(ur"\u2022",u" ",u"Bullet: bullet",u"0"),
(ur"\u2023",u" ",u"Bullet: triangular bullet",u"0"),
(ur"\u2025",u" ",u"Dot leader: two dot leader",u"0"),
(ur"\u2026",u" ",u"Horizontal ellipsis:horizontal ellipsis",u"0"),
(ur"\u2027",u" ",u"Hyphenation: hyphenation point",u"0"),
(ur"\u2028",ur"",u"Separator: line separator",u"0"),
(ur"\u2029",ur"",u"Separator: paragraph separator",u"0"),
(ur"\u00BC",u"1/4",u"Number forms: un quart",u"0"),
(ur"\u00BD",u"1/2",u"Number forms: un demi",u"0"),
(ur"\u00BE",u"3/4",u"Number forms: trois quarts",u"0"),
(ur"\u2150",u"1/7",u"Number forms: un septieme",u"0"),
(ur"\u2151",u"1/9",u"Number forms: un neuvieme",u"0"),
(ur"\u2152",u"1/10",u"Number forms: un dixieme",u"0"),
(ur"\u2153",u"1/3",u"Number forms: un tiers",u"0"),
(ur"\u2154",u"2/3",u"Number forms: deux tiers",u"0"),
(ur"\u2155",u"1/5",u"Number forms: un cinqieme",u"0"),
(ur"\u2156",u"2/5",u"Number forms: deux cinqieme",u"0"),
(ur"\u2157",u"3/5",u"Number forms: trois cinqieme",u"0"),
(ur"\u2158",u"4/5",u"Number forms: quatre cinqieme",u"0"),
(ur"\u2159",u"1/6",u"Number forms: un sixieme",u"0"),
(ur"\u215A",u"5/6",u"Number forms: cinq sixieme",u"0"),
(ur"\u215B",u"1/8",u"Number forms: un huitieme",u"0"),
(ur"\u215C",u"3/8",u"Number forms: trois huitieme",u"0"),
(ur"\u215D",u"5/8",u"Number forms: cinq huitieme",u"0"),
(ur"\u215E",u"7/8",u"Number forms: sept huitieme",u"0"),
(ur"\u0152",u"oe",u"Ligatures: lattin small ligature oe",u"0"),
(ur"\u0153",u"oe",u"Ligatures: lattin small ligature oe",u"0")]

#Do not exclude single quote
PUNCTUATIONEXCLUDE 	= ['!', '"', '#', '(', ')', '*', '+', '-',
                      '/', ':', ';', '<', '=', '>', '?', '[', '\\',
                      ']', '^', '_', '`', '{', '|', '}', '~']
DOTCOMMAEXCLUDE 	= ['.',',']
PUNCTUATIONMAP  	= {
    "%": (r"%",r"pourcent", u"Prozent", u"percent", u"per cento"),
    "&": (r"&",r"et", u"und", u"and", u"e"),
    "@": (r"@",r"at", u"at", u"at", u"at"),
    '$': (r'$',r"dollars", u"Dollar", u"dollars", u"dollari"),
}

PUNCTUATIONPATTERN 	= ur"(\!|\"|#|\$|%|&|'|\(|\)|\*|\+|,|-|\.|/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|`|\{|\}|~|\|){4,}"

ACRONYMREGEXLIST = [(ur"( |^)([A-Z])([A-Z])([A-Z])([A-Z])([A-Z])( |$)",
		              ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'. '+p.group(5).lower()+'. '+p.group(6).lower()+'.'+p.group(7)",ur"1",ur"Acronyms"),
		            (ur"( |^)([A-Z])([A-Z])([A-Z])([A-Z])( |$)",
		              ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'. '+p.group(5).lower()+'.'+p.group(6)",ur"1",ur"Acronyms"),
		            (ur"( |^)([A-Z])([A-Z])([A-Z])( |$)",
		              ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'.'+p.group(5)",ur"1",ur"Acronyms"),
		            (ur"( |^)([A-Z])([A-Z])( |$)",
		              ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'.'+p.group(4)",ur"1",ur"Acronyms"),
		            (ur"( |^)([A-Z])( |$)",
		              ur"lambda p: p.group(1)+p.group(2).lower()+'.'+p.group(3)",ur"1",ur"Acronyms")]

DATEREGEXLIST = [(ur"([0-9][0-9])[./]([0-9][0-9])[./]([0-9][0-9][0-9]?[0-9]?)", 
                  ur"\g<1> \g<2> \g<3>",ur"1",ur"Dates")]

APOSTHROPHELIST = [(ur"[']", ur"' ",ur"1",ur"Spaces after apostrophes")]

CONTRACTIONPREFIXELIST = [
	(ur"á",ur"à",u"2",u""),
	(ur"-á-",ur"-à-",u"2",u""),
	(ur"^a",ur"à",u"1",u""),
	(ur"quelqu' un",ur"quelqu'un",u"2",u""),
	(ur"c' qu",ur"ce qu",u"2",u""),
	(ur"c' ",ur"c'",u"2",u""),
	(ur"s' est",ur"s'est",u"2",u""),
	(ur"s' agit ",ur"s'agit",u"2",u""),
	(ur"s' agir",ur"s'agir",u"2",u""),
	(ur"s' agiss",ur"s'agiss",u"2",u""),
	(ur"s' il",ur"s'il",u"2",u""),
	(ur"s' ils",ur"s'ils",u"2",u""),
	(ur"d' abord",ur"d'abord",u"2",u""),
	(ur"d un(?P<gr1>e?)",ur"d'un\g<gr1>",u"2",u""),
	(ur"(?P<gr1>[jl])' ai",ur"\g<gr1>'ai",u"2",u""),
	(ur"(?P<gr1>[jl])' y",ur"\g<gr1>'y",u"2",u""),
	(ur"(?P<gr1>[ltm])' a",ur"\g<gr1>'a",u"2",u""),
	(ur"n' est",ur"n'est",u"2",u""),
	(ur"n' a",ur"n'a",u"2",u""),
	(ur"(?P<gr1>[djlmnst])' y",ur"\g<gr1>'y",u"2",u""),
	(ur"(?P<gr1>[cdjlmnst])' en",ur"\g<gr1>'en",u"2",u""),
	(ur"(?P<gr1>qu)' y",ur"\g<gr1>'y",u"2",u""),
	(ur"(?P<gr1>qu)' en",ur"\g<gr1>'en",u"2",u""),
	(ur"-t-(?P<gr1>il|elle|on)",ur" -t-\g<gr1>",u"2",u"")]

ABBREVIATIONS = {
	FRENCH:{ u'A/R':u'accusé de réception',u'A. R.':u'avis de réception',u'adj.':u'adjectif',u'admin':u'administration',u'ann.':u'annexe',u'art.':u'article',
	u'assoc.':u'association',u'av.':u'avenue',u'bibliogr.':u'bibliographie',u'bibl.':u'bibliothèque',u'biogr.':u'biographie',u'bd.':u'boulevard ',
	u'cad':u'c’est-à-dire',u'cap.':u'capitale',u'C.Q.F.D.':u'ce qu’il fallait démontrer',u'chap.':u'chapitre',u'ch.':u'chemin',u'circ.':u'circonscription',
	u'col.':u'colonne',u'Cie':u'compagnie',u'c/c':u'compte courant',u'concl.':u'conclusion',u'cf.':u'confer',u'conj.':u'conjonction',u'coop.':u'coopération',
	u'c.c.':u'copie conforme',u'c':u'copyright',u'©':u'copyright',u'c.v.':u'curriculum vitae',u'dest.':u'destinataire',u'disp.':u'disponible',
	u'Dr.':u'docteur',u'Drs.':u'docteurs',u'Dre.':u'doctoresse',u'Dres.':u'doctoresses',u'doc.':u'document',u'env.':u'environ',u'err.':u'erratum, errata',
	u'et al.':u'et alii',u'etc.':u'et cetera',u'ex.':u'exemple',u'e.g.':u'exempli gratia',u'ext.':u'externe',u'féd.':u'fédéral',u'fém.':u'féminin',
	u'fig.':u'figure',u'id.':u'idem',u'i. e.':u'c’est-à-dire',u'in ext.':u'in extenso',u'intro':u'introduction',u'M.':u'monsieur',u'MM.':u'messieurs',
	u'maj.':u'majuscule',u'Me':u'maître',u'Mes':u'maîtres',u'méd.':u'médecine',u'mer.':u'mercredi',u'Mgr':u'monseigneur',u'Mgrs':u'messeigneurs ',
	u'Mlle':u'mademoiselle ',u'Mlles':u'mesdemoiselles',u'Mme':u'madame',u'Mmes':u'mesdames',u'Mo':u'mégaoctet',u'N.B.':u'nota bene',u'nbre':u'nombre',
	u'nbx':u'nombreux',u'N/Réf.':u'notre référence',u'obs.':u'observation',u'P.-D. G.':u'président-directeur général',u'pcq':u'parce que',u'pers.':u'personne',
	u'p. ex.':u'par exemple',u'p. ext.':u'par extension',u'plur.':u'pluriel',u'Prof.':u'professeur',u'P.-S.':u'post-scriptum',u'qté':u'quantité',
	u'qqn':u'quelqu’un',u'tps':u'temps',u'qqch':u'quelque chose',u'qqf.':u'quelquefois',u'qqn':u'quelqu’un',u'quant.':u'quantité',u'RDV':u'rendez-vous',
	u'réf.':u'référence',u'rte':u'route',u'sing.':u'singulier',u'St':u'saint',u'stat.':u'statistique',u'Ste':u'sainte',u'Sté':u'société',u'Stes':u'saintes',
	u'Sts':u'saints',u'suiv.':u'suivant',u'sup.':u'supra',u'suppl.':u'supplément',u'S.V.P.':u's’il vous plaît',u'tél.':u'téléphone',u'téléc.':u'télécopieur',
	u'temp.':u'température',u'trad.':u'traducteur',u'tjrs':u'toujours',u'univ.':u'université',u'us.':u'usage',u'UV':u'ultraviolet',u'vol.':u'volume',
	u'V/Réf.':u'votre référence'}
}
