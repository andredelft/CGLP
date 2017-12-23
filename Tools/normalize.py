from uni_beta_code import beta2uni
from uni_beta_code import uni2beta
import regex
import unicodedata

#IN PROGRESS
LATIN = [
	('i',beta2uni('i')),
	('o',beta2uni('o')),
	('p',beta2uni('r')),
	('u',beta2uni('u')),
	('v',beta2uni('n')),
	('x',beta2uni('x')),
	('A',beta2uni('*a')),
	('B',beta2uni('*B')),
	('I',beta2uni('*i')),
	('K',beta2uni('*k')),
	('M',beta2uni('*m')),
	('T',beta2uni('*t')),
	('X',beta2uni('*x')),
	('Z',beta2uni('*z'))
]

CYRILLIC = [
	('А',beta2uni('*A')),
	('М',beta2uni('*M')),
	('Ф',beta2uni('*F')),
	('є',beta2uni('e')),
	('ї',beta2uni('i+')),
	('Ѱ',beta2uni('*Y'))
]

GREEK_AND_COPTIC = [
	('ϛ',beta2uni('s'))
]

OTHER = [
	(chr(0x5d0),beta2uni('k')), # Hebrew Aleph
	('ß',beta2uni('b'))
]

unicode_blocks = [LATIN,CYRILLIC,GREEK_AND_COPTIC,OTHER]

pattern = []
for block in unicode_blocks:
	pattern.append([(regex.compile(old),new) for (old,new) in block])

def normalize_greek(text):
	words = []
	for word in text.split():
		if ''.join(regex.findall('[A-Za-z]',word)) == word:
			# Make sure to skip words that are entirely in latin form
			words.append(word)
		else:
			for (repl,new) in pattern[0]:
				word = repl.sub(new,word)
			words.append(word)
	
		for (i,p) in enumerate(pattern):
			for (repl,new) in p:
				word = repl.sub(new,word)
		
	return ' '.join(words)