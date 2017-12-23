from uni_beta_code import beta2uni
from uni_beta_code import uni2beta
import regex
import unicodedata

diac = '()/\\\\=|+'

def remove_capital(word_beta):
	word_beta = word_beta.replace('*','')
	first_diac = regex.search('^[%s]+' % diac, word_beta)
	if first_diac != None:
		return word_beta[first_diac.end()] + first_diac.group() + word_beta[first_diac.end()+1:]
	else:
		return word_beta

def add_capital(word_beta):
	if word_beta[0] != '*':
		first_diac = regex.search('(?<=^[a-zA-Z])[%s]+(?=[a-zA-Z])' % diac, word_beta)
		if first_diac != None:
			return '*' + first_diac.group() + word_beta[0] + word_beta[first_diac.end():]
		else:
			return '*' + word_beta
	else:
		return word_beta

# Return characters that aren't part of the beta code
def non_beta_chars(word_beta):
	return regex.sub('[a-zA-Z*%s]' % diac, '', word_beta)
	
def remove_diac(word_beta):
	return regex.sub('[%s]'%diac,'',word_beta)

# Decomposes given string in the unicode values (in hexadecimal notation) of the individual characters
def hex_decompose(string):
	return [hex(ord(char)) for char in string]
	