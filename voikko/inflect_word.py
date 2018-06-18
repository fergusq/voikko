# Copyright 2018 Kielikone Oy
#
# Added generate_forms that can generate alternative forms
# Guessing -ton/-tön inflection class
# Fixed bugs

# Copyright 2017 Iikka Hauhio
#
# Contains some changes to the original file (voikko-inflect-word).
# The file is no longer a stand-alone program, but a library.
# It reads word classes automatically from the sanat.txt file.
# It also tries to guess the word class, if not found in sanat.txt.
# The file was changed to support Python 3.

# Copyright 2005-2007 Harri Pitkänen (hatapitk@iki.fi)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import voikko.voikkoinfl as voikkoinfl
import os
import sys
import locale
import voikko.voikkoutils as voikkoutils

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

NOUN_AFFIX_FILE = os.path.join(SCRIPT_DIR, 'subst.aff')
VERB_AFFIX_FILE = os.path.join(SCRIPT_DIR, 'verb.aff')
PARAM_ENCODING = 'UTF-8'

noun_types = voikkoinfl.readInflectionTypes(NOUN_AFFIX_FILE)
verb_types = voikkoinfl.readInflectionTypes(VERB_AFFIX_FILE)

def word_and_infl_class(fullclass):
	infclass_parts = fullclass.split('-')
	if len(infclass_parts) == 2:
		wordclass = infclass_parts[0]
		infclass = infclass_parts[1]
	elif len(infclass_parts) == 3:
		wordclass = infclass_parts[0]
		infclass = infclass_parts[1]+u'-'+infclass_parts[2]
	else:
		print('Incorrect inflection class')
		sys.exit(1)
	if not wordclass in [u'subst', u'verbi']:
		print('Incorrect word class')
		sys.exit(1)
	return (wordclass, infclass)

def generate_forms(word, infl_classes=None, pos=None):
	"""Generates inflected forms for the given word."""

	global verb_types
	global noun_types
	if infl_classes is None:
		if word in WORD_CLASSES:
			infl_classes = WORD_CLASSES[word]
		elif len(word) > 3 and word[-3:] in ["ttu", "tty"]:
			infl_classes = ["subst-valo-av1"]
		elif len(word) > 3 and word[-3:] in ["uus", "yys"]:
			infl_classes = ["subst-kalleus"]
		elif len(word) > 3 and word[-2:] in ["ja", "jä"]:
			infl_classes = ["subst-kulkija"]
		elif len(word) > 4 and word[-3:] in ["ton", "tön"]:
			infl_classes = ["subst-onneton-av2"]
		else:
			def end_similarity(word2):
				i = 0
				while i < min(len(word), len(word2)):
					if word[-i-1] != word2[-i-1]:
						break
					i += 1
				return (i, -len(word2))
			def right_wclass(word2):
				if pos is None or any([word_class.startswith(pos) for word_class in WORD_CLASSES[word2]]):
					return 1
				else:
					return 0
			def points(word2):
				return (right_wclass(word2), end_similarity(word2))
			mirror = sorted(list(WORD_CLASSES), key=points)[-1]
			infl_classes = WORD_CLASSES[mirror]
			WORD_CLASSES[word] = infl_classes
			#raise(Exception("Unknown word '" + word + "'"))
	ans = []
	for infl_class in infl_classes:
		(wclass, infclass) = word_and_infl_class(infl_class)
		if wclass == u'verbi': itypes = verb_types
		else: itypes = noun_types
		homonym = {}
		for iword in voikkoinfl.inflectWord(word, infclass, itypes):
			if iword.formName not in homonym:
				homonym[iword.formName] = []
			if iword.inflectedWord not in homonym[iword.formName]:
				homonym[iword.formName].append(iword.inflectedWord)
		ans.append(homonym)
	return ans

def inflect_word(word, classes=None, required_wclass=None):
	"""Deprecated."""

	homonyms = generate_forms(word, infl_classes=classes, pos=required_wclass)
	ans = []
	for homonym in homonyms:
		new_homonym = {}
		for form in homonym:
			new_homonym[form] = homonym[form][0]
		ans.append(new_homonym)
	return ans[0]

WORD_CLASSES = {}

with open(os.path.join(SCRIPT_DIR, 'sanat.txt')) as f:
	for line in f:
		line = line.strip()
		i = line.index(";")
		word = line[:i].replace("=", "")
		classes = line[i+1:]
		
		if word not in WORD_CLASSES:
			WORD_CLASSES[word] = []
		
		WORD_CLASSES[word].append(classes)
