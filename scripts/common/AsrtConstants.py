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

from config import FRENCH, GERMAN

SPACEPATTERN                = u"[ ]+"
CAPTURINGDIGITPATTERN		= u"([0-9\.,]+)"
GROUPINGDOTCOMMAPATTERN		= u"( |$)([.,])( |$)"
EXPANDEXCEPTIONS			= (u"er", u"re", u"ère", u"e", u"ème")

UNITD2W                     = {1:'ein', 2:'zwei', 3:'drei', 4:'vier', 5:'fünf', 6:'sechs', 7:'sieben', 8:'acht', 9:'neun',
                               10:'zehn', 11:'elf', 12:'zwölf', 13:'dreizehn', 14:'vierzehn', 15:'fünfzehn', 16:'sechszehn',
                               17:'siebzehn', 18:'achtzehn', 19:'neunzehn'}

DECADED2W                   = {1:'zehn', 2:'zwanzig', 3:'dreissig', 4:'vierzig', 5:'fünfzig', 6:'sechzig', 7:'siebzig',
                               8:'achtzig', 9:'neunzig'}
GERMANMONTHESREGEX			= u"(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)"

#See https://en.wikipedia.org/wiki/List_of_Unicode_characters
#http://www.cloford.com/resources/charcodes/utf-8_punctuation.htm
#http://xahlee.info/comp/unicode_matching_brackets.html
#Format is matching pattern, substitution, comment, language id
UTF8MAP                     = [
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
PUNCTUATIONEXCLUDE              = ['!', '"', '#', '(', ')', '*', '+', '-',
                                   '/', ':', ';', '<', '=', '>', '?', '[', '\\',
                                   ']', '^', '_', '`', '{', '|', '}', '~']
DOTCOMMAEXCLUDE                 = ['.',',']
PUNCTUATIONMAP                  = {
    "%": (r"%",r"pourcent", u"Prozent", u"percent", u"per cento"),
    "&": (r"&",r"et", u"und", u"and", u"e"),
    "@": (r"@",r"at", u"at", u"at", u"at"),
    '$': (r'$',r"dollars", u"Dollar", u"dollars", u"dollari"),
}

PUNCTUATIONPATTERN              = ur"(\!|\"|#|\$|%|&|'|\(|\)|\*|\+|,|-|\.|/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|`|\{|\}|~|\|){4,}"

ACRONYMREGEXLIST                = [(ur"( |^)([A-Z])([A-Z])([A-Z])([A-Z])([A-Z])[.,:;]?( |$)",
                                    ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'. '+p.group(5).lower()+'. '+p.group(6).lower()+'.'+p.group(7)",ur"1",ur"0",ur"Acronyms"),
                                   (ur"( |^)([A-Z])([A-Z])([A-Z])([A-Z])[.,:;]?( |$)",
                                    ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'. '+p.group(5).lower()+'.'+p.group(6)",ur"1",ur"0",ur"Acronyms"),
                                   (ur"( |^)([A-Z])([A-Z])([A-Z])[.,:;]?( |$)",
                                    ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'. '+p.group(4).lower()+'.'+p.group(5)",ur"1",ur"0",ur"Acronyms"),
                                   (ur"( |^)([A-Z])([A-Z])[.,:;]?( |$)",
                                    ur"lambda p: p.group(1)+p.group(2).lower()+'. '+p.group(3).lower()+'.'+p.group(4)",ur"1",ur"0",ur"Acronyms")]

DATEREGEXLIST                   = [(ur"([0-9][0-9])[./]([0-9][0-9])[./]([0-9][0-9][0-9]?[0-9]?)",
                                    ur"\g<1> \g<2> \g<3>",ur"1",ur"0",ur"Dates")]

APOSTHROPHELIST                 = [(ur"[']", ur"' ",ur"1",ur"0",ur"Spaces after apostrophes")]

CONTRACTIONPREFIXELIST          = [
	(ur"á",ur"à",u"2",ur"1",u""),
	(ur"-á-",ur"-à-",u"2",ur"1",u""),
	(ur"^[aA] ",ur"à ",u"1",ur"1",u""),
	#(ur"quelqu' un",ur"quelqu'un",u"2",ur"1",u""),
	#(ur"c' qu",ur"ce qu",u"2",ur"1",u""),
	#(ur"c' ",ur"c'",u"2",ur"1",u""),
	#(ur"s' est",ur"s'est",u"2",ur"1",u""),
	#(ur"s' agit ",ur"s'agit",u"2",ur"1",u""),
	#(ur"s' agir",ur"s'agir",u"2",ur"1",u""),
	#(ur"s' agiss",ur"s'agiss",u"2",ur"1",u""),
	#(ur"s' il",ur"s'il",u"2",ur"1",u""),
	#(ur"s' ils",ur"s'ils",u"2",ur"1",u""),
	#(ur"d' abord",ur"d'abord",u"2",ur"1",u""),
	(ur"d un(?P<gr1>e?)",ur"d' un\g<gr1>",u"2",ur"1",u""),
	#(ur"(?P<gr1>[jl])' ai",ur"\g<gr1>'ai",u"2",ur"1",u""),
	#(ur"(?P<gr1>[jl])' y",ur"\g<gr1>'y",u"2",ur"1",u""),
	#(ur"(?P<gr1>[ltm])' a",ur"\g<gr1>'a",u"2",ur"1",u""),
	#(ur"n' est",ur"n'est",u"2",ur"1",u""),
	#(ur"n' a",ur"n'a",u"2",ur"1",u""),
	#(ur"(?P<gr1>[djlmnst])' y",ur"\g<gr1>'y",u"2",ur"1",u""),
	#(ur"(?P<gr1>[cdjlmnst])' en",ur"\g<gr1>'en",u"2",ur"1",u""),
	#(ur"(?P<gr1>qu)' y",ur"\g<gr1>'y",u"2",ur"1",u""),
	#(ur"(?P<gr1>qu)' en",ur"\g<gr1>'en",u"2",ur"1",u""),
	(ur"[ -]t[ -](?P<gr1>il|elle|on)",ur" -t-\g<gr1>",u"1",ur"1",u"")]


TRANSITIONNUMBERS					= {
	FRENCH:{'1.':u'premièrement','2.':u'deuxièmement','3.':u'troisièmement','4.':u'quatrièmement',
            '5.':u'cinquièmement','6.':u'sixièmement', '7.':u'septièmement','8.':u'huitièmement',
            '9.':u'neuvièmement', '10.':u'dixièmement'}
}

ABBREVIATIONS                       = {
	FRENCH:{ u'A/R':u'accusé de réception',u'adj.':u'adjectif',u'admin':u'administration',u'ann.':u'annexe',u'art.':u'article',
	u'assoc.':u'association',u'av.':u'avenue',u'bibliogr.':u'bibliographie',u'bibl.':u'bibliothèque',u'biogr.':u'biographie',u'bd.':u'boulevard ',
	u'cad':u'c’est-à-dire',u'cap.':u'capitale',u'C.Q.F.D.':u'ce qu’il fallait démontrer',u'chap.':u'chapitre',u'ch.':u'chemin',u'circ.':u'circonscription',
	u'col.':u'colonne',u'Cie':u'compagnie',u'c/c':u'compte courant',u'concl.':u'conclusion',u'cf.':u'confer',u'conj.':u'conjonction',u'coop.':u'coopération',
	u'c.v.':u'curriculum vitae',u'dest.':u'destinataire',u'disp.':u'disponible',u'Dr.':u'docteur',u'Drs.':u'docteurs',u'Dre.':u'doctoresse',
    u'Dres.':u'doctoresses',u'doc.':u'document',u'env.':u'environ',u'etc.':u'et cetera',u'ex.':u'exemple',u'e.g.':u'exempli gratia',u'ext.':u'externe',
    u'féd.':u'fédéral',u'fém.':u'féminin',u'fig.':u'figure',u'id.':u'idem',u'intro':u'introduction',u'MM.':u'messieurs',u'maj.':u'majuscule',
    u'méd.':u'médecine',u'Mgr':u'monseigneur',u'Mgrs':u'messeigneurs ',u'Mlle':u'mademoiselle ',u'Mlles':u'mesdemoiselles',u'Mme':u'madame',
    u'Mmes':u'mesdames',u'Mo':u'mégaoctet',u'N.B.':u'nota bene',u'nbre':u'nombre',u'nbx':u'nombreux',u'N/Réf.':u'notre référence',u'obs.':u'observation',
    u'pcq':u'parce que',u'pers.':u'personne',u'plur.':u'pluriel',u'Prof.':u'professeur',u'P.-S.':u'post-scriptum',u'qté':u'quantité',u'qqn':u'quelqu’un',
    u'tps':u'temps',u'qqch':u'quelque chose',u'qqf.':u'quelquefois',u'qqn':u'quelqu’un',u'RDV':u'rendez-vous',u'réf.':u'référence',u'rte':u'route',
    u'sing.':u'singulier',u'St':u'saint',u'stat.':u'statistique',u'Ste':u'sainte',u'Sté':u'société',u'Stes':u'saintes',u'Sts':u'saints',u'suiv.':u'suivant',
    u'sup.':u'supra',u'suppl.':u'supplément',u'S.V.P.':u's’il vous plaît',u'tél.':u'téléphone',u'téléc.':u'télécopieur',u'temp.':u'température',
    u'trad.':u'traducteur',u'tjrs':u'toujours',u'univ.':u'université',u'us.':u'usage',u'UV':u'ultraviolet',u'V/Réf.':u'votre référence'},
    GERMAN:{u'a.A.':u'auf Anfrage',u'Abb.':u'Abbildung',u'Abf.':u'Abfahrt',u'Abh.':u'Abhandlung',u'Abk.':u'Abkürzung',u'Abs.':u'Absender',u'Abschn.':u'Abschnitt',
    u'Abt.':u'Abteilung',u'abw.':u'abwesend',u'akad.':u'Akademisch',u'AK':u'Aktienkapital',u'Akk.':u'Akkusativ',u'Akku':u'Akkumulator',u'allg.':u'allgemein',
    u'a.M.':u'am Main',u'Anh.':u'Anhang',u'Ank.':u'Ankunft',u'Anm.':u'Anmerkung',u'Antw.':u'Antwort',u'Anw.':u'Anweisung',u'Anz.':u'Anzeiger',u'Aufl.':u'Auflage',
    u'aussch.':u'Ausschliesslich',u'Az':u'Aktenzeichen',u'Bed.':u'Bedarf',u'begl.':u'beglaubigt',u'beil.':u'beiliegend',u'beisp.':u'beispielweise',
    u'Ber.':u'Bericht',u'bes.':u'besonders',u'Betr.':u'Betreff',u'betr.':u'betreffend',u'Bez.':u'Bezirk',u'bez.':u'Bezeichnung',u'BH':u'Bustenhalter',
    u'Bhf.':u'Bahnhof',u'Bl.':u'Blatt',u'Br.':u'Bruder',u'bz.':u'bezahlt',u'bzw.':u'beziehungsweise',u'cal.':u'Kalorie',u'cand.':u'Kandidat',u'cbm':u'Kubikmeter',
    u'ccm':u'Kubiczentimeter',u'dag.':u'dagegen',u'dam.':u'damals',u'Dat.':u'Dativ',u'dazw.':u'dazwischen',u'db':u'Dezibel',u'desgl.':u'desgleichen',
    u'dgl.':u'dergleichen',u'Dipl.':u'Diplom',u'Doz.':u'Dozent',u'Dr.':u'Doktor',u'Dr.h.c.':u'Doktor honoris causa',u'dt.':u'deutsch',u'dz.':u'derzeit',
    u'ehem.':u'ehemals',u'eigtl.':u'eigentlich',u'EKG':u'Elektrokardiogramm',u'entspr.':u'entsprechend',u'entw.':u'entweder',u'ER':u'Europarat',
    u'Erdg.':u'Erdgeschoss',u'Essl.':u'Esslöffel',u'etw.':u'etwas',u'exkl.':u'exklusive',u'Ff.':u'Fortsetzung folgt',u'Fak.':u'Fakultät',u'Fam.':u'Familie',
    u'Fdw.':u'Feldwebel',u'Fr.':u'Frau',u'Frl.':u'Fraulein',u'geb.':u'geboren',u'Gebr.':u'Gebrüder',u'gegr.':u'gegrundet',u'gesch.':u'geschieden',
    u'geschr.':u'geschrieben',u'ges.gesch.':u'gesetzlich geschützt',u'geschl.':u'geschlossen',u'gest.':u'gestorben',u'gez.':u'gezeichnet',u'GG':u'Grundgesetz',
    u'GmbH':u'Gesellschaft mit beschränkter Haftung',u'gzj.':u'ganzjährig',u'ha.':u'Hektar',u'habil.':u'habilitiert',u'Hbf.':u'Hauptbahnhof',u'hdt.':u'hundert',
    u'hj.':u'halbjährlich',u'höfl.':u'höflichst',u'Hptst.':u'Hauptstadt',u'Hr.':u'Herr',u'i.allg.':u'im allgemeinen',u'i.F':u'in der Fassung',u'ill.':u'illustriert',
    u'inbegr.':u'inbegriffen',u'Ind.':u'Indikativ',u'Ing.':u'Ingenieur',u'Inh.':u'Inhaber',u'inkl.':u'inklusive',u'Insp.':u'Inspektor',u'Inst.':u'Instanz',
    u'Inst.':u'Institut',u'int.':u'international',u'inzw.':u'inzwischen',u'i.R.':u'im Ruhestand',u'iZm.':u'in Zusammenhang mit',u'jew.':u'jewelig',u'Jg.':u'Jahrgang',
    u'Jh.':u'Jahrhundert',u'jun.':u'junior',u'jur.':u'juristisch',u'kath.':u'katholisch',u'Kfm.':u'Kaufmann',u'kg.':u'Kilogramm',u'kgl.':u'königlich',u'Kl.':u'Klasse',
    u'km.':u'Kilometer',u'kn.':u'Knoten',u'kompl.':u'komplett',u'Kpt.':u'Kapitän',u'Kt.':u'Kanton',u'k.u.k.':u'kaiserlich und königlich',u'kW':u'Kilowatt',
    u'led.':u'ledig',u'lfd.':u'laufend',u'Lfrg.':u'Lieferung',u'Lit.':u'Literatur',u'lt.':u'laut',u'Lt.':u'Leutnant',u'MA':u'Mittelalter',u'ma.':u'mittelälterlich',
    u'Mag.':u'Magister',u'm.a.W.':u'mit anderen Worten',u'm.E':u'meines Erachtens',u'mech.':u'mechanisch',u'med.':u'medizinisch',u'mehrf.':u'mehrfach',
    u'MEZ':u'Mitteleuropäische Zeit',u'MFG':u'mit freundlichen Grüssen',u'mg':u'Milligramm',u'Mill.':u'Million',u'Min.':u'Minute',u'mm':u'millimeter',u'Mo':u'Montag',
    u'Mrd.':u'Milliarde',u'mtl.':u'monatlich',u'm.W.':u'meines Wissens',u'MWSt':u'Mehrwertsteuer',u'Mz.':u'Mehrzahl',u'N':u'Nord',u'Nachf.':u'Nachfolger',
    u'nachm.':u'nachmittags',u'nat.':u'national',u'n.J.':u'nächsten Jahres',u'n.M.':u'nächsten Monats',u'N.N.':u'Name unbekannt',u'NO':u'Nordost',
    u'Nr.':u'Nummer',u'NS':u'Nachschrift',u'NW':u'Nordwest',u'NZ':u'Nachrichtenzentrale',u'od.':u'oder',u'o.a.':u'oben angeführt',u'o.ä.':u'oder ähnliches',
    u'o.A.':u'ohne Adresse',u'OB':u'Oberbefelshaber',u'o.B.':u'ohne Befund',u'OEZ':u'Osteuropäische Zeit',u'o.J.':u'ohne Jahr',u'ö.L':u'östlicher Länge',
    u'o.Pr.':u'ordentlicher Professor',u'örtl.':u'örtlich',u'o.V.':u'ohne Verfasser',u'p.A.':u'per Adresse',u'Part.':u'Parterre',u'pat.':u'patentiert',
    u'pharm.':u'pharmazeutisch',u'Pkt.':u'Punkt',u'Pl.':u'Platz',u'pl':u'Plural',u'pol.':u'politisch',u'pol.':u'polizeilich',u'Postf.':u'Postfach',u'priv.':u'privat',
    u'Prof.':u'Professor',u'prot.':u'protestantisch',u'Prov.':u'Provinz',u'qkm':u'Quadratkilometer',u'qm':u'Quadratmeter',u'Quitt.':u'Quittung',u'rd.':u'rund',
    u'Red.':u'Redacteur',u'Reg.':u'Regierung',u'Rep.':u'Republik',u'resp.':u'respektiv',u'Rgt.':u'Regiment',u'Rhld.':u'Rheinland',u'rm.':u'raummeter',u'Rzpt.':u'Rezept',
    u'S-Bahn':u'Schnellbahn',u'SB':u'Selbstbedienung',u'SBB':u'Schweizerische Bundesbahn',u's.Br.':u'südliche Breite',u'sek.':u'sekunde',u'Sekr.':u'Sekretär',
    u'sel.':u'selig',u'Sem.':u'Semester',u'Sen.':u'Senator',u'sen.':u'senior',u'sfr.':u'Schweizer Franken',u's.g.e.':u'sehr gut erhalten',u'sm.':u'Seemeile',
    u'SM':u'Seine Majestät',u'SO':u'Südost',u's.o.':u'siehe oben',u's.u.':u'siehe unten',u'spez.':u'speziell',u'St.':u'Stück',u'städt.':u'städtisch',u'Std.':u'Stunde',
    u'stdl.':u'stündlich',u'stellv.':u'stellvertretend',u'StGB':u'Strafgesetzbuch',u'StKl':u'Steuerklasse',u'StPO':u'Strafprozessordnung',u'Str.':u'Strasse',
    u'StVO':u'Strassenverkehrsordnung',u'svw.':u'soviel wie',u'SW':u'Südwest',u'sZ':u'seinerzeit',u'SZ':u'Sommerzeit',u't':u'Tonne',u'TA':u'Tierartzt',u'Tab.':u'Tabelle',
    u'tägl.':u'täglich',u'Tb.':u'Tuberkulose',u'Teilh.':u'Teilhaber',u'Tel.':u'Telefon',u'TH':u'Technische Hochschule',u'Tnd.':u'Tausend',u'TU':u'Technische Universität',
    u'TV':u'Tarifvertrag',u'u.a.':u'unter anderem',u'u.ä.':u'und ähnliches',u'u.A.w.g.':u'um Antwort wird gebeten',u'Übers.':u'Übersetzer',u'übl.':u'üblich',
    u'üblw.':u'üblicherweise',u'U-Boot':u'Unterseeboot',u'u.dsgl.':u'und desgleichen',u'u.d.M.':u'unter dem Meeresspiegel',u'ue.':u'unehelich',u'u.E.':u'unseres Erachtens',
    u'U/min.':u'Umdrehungen in der Minute',u'Univ.':u'Universität',u'unverk.':u'unverkäuflich',u'urspr.':u'ursprünglich',u'usw.':u'und so weiter',u'u.U.':u'unter Ümständen',
    u'u.ü.V.':u'unter üblichem Vorbehalt',u'u.v.a.':u'und veil andere',u'u.W.':u'unseres Wissens',u'u.zw.':u'und zwar', u'v.a.':u'vor allem',u'var.':u'variabel',
    u'v.A.w.':u'von Amts wegen',u'v.D.':u'vom Dienst',u'verb.':u'verbessert',u'verh.':u'verheiratet',u'Verl.':u'Verlag',u'Verm.':u'Vermerk',u'verst.':u'verstorben',
    u'vgl.':u'vergleiche',u'v.H.':u'vom Hundert',u'v.J.':u'vorigen Jahres',u'v.M.':u'vorigen Monats',u'v.o.':u'von oben',u'Vollm.':u'Vollmacht',u'vollst.':u'vollständig',
    u'vorl.':u'vorläufig',u'vorm.':u'vormittags',u'Vors.':u'Vorsitzender',u'v.T.':u'vom Tausend',u'Wb.':u'Wörterbuch',u'WEZ':u'Westeuropäische Zeit',u'Whg.':u'Wohnung',
    u'Wkst.':u'Werkstatt',u'w.L.':u'westlicher Länge',u'w.o.':u'wie oben',u'Wz.':u'Warenzeichen',u'z.A.':u'zur Ansicht',u'z.B.':u'zum Beispiel',u'z.d.A.':u'zu den Akten',
    u'zgl.':u'zugleich',u'z.H.':u'zu Händen',u'Zi':u'Zimmer',u'Ziff.':u'Ziffer',u'z.K.':u'zur Kenntnisnahme',u'ZPO':u'Zivilprozessordnung',u'z.S.':u'zur See',
    u'z.T.':u'zum Teil',u'Ztg.':u'Zeitung',u'zuf.':u'zufolge',u'zus.':u'zusammen',u'zw.':u'zwischen',u'z.w.V.':u'zur weiteren Veranlassung',u'zzgl.':u'zuzüglich',
    u'z.Z.':u'zur Zeit'}
}
