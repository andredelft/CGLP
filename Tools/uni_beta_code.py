""" Edit from the cltk beta_to_unicode script, to do the reverse operation """
import unicodedata
import string
import json
import os
import regex

from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.utils.formatter import cltk_normalize

import Tools.misc as m

with open(os.path.join('Tools','LOWER.json')) as f:
    LOWER = json.load(f)
with open(os.path.join('Tools','UPPER.json')) as f:
    UPPER = json.load(f)

dict = {}
for character in UPPER:
    dict[ord(character[1])] = character[0]
for character in LOWER:
    dict[ord(character[1])] = character[0]

def uni2beta(text_uni):
    text_uni = unicodedata.normalize('NFC',text_uni)
    text_beta = text_uni.translate(dict)
    text_beta = text_beta.translate(str.maketrans(string.ascii_uppercase,string.ascii_lowercase))
    return text_beta

def beta2uni(text_beta):
    text_beta = text_beta.translate(str.maketrans(string.ascii_lowercase,string.ascii_uppercase))
    text_uni = Replacer().beta_code(text_beta)
    return text_uni

def clean_beta(text_uni):
    text_uni = m.remove_diac(m.remove_capital(text_uni)) #filter capital mark (*) and diacritical marks in unicode string
    text_beta = uni2beta(text_uni).replace('\n',' ')
    return ''.join(char for char in text_beta if char not in m.non_beta_chars(text_beta))

def non_greek_chars(word_uni):
    diac_chars = regex.sub('[^*{}]'.format(m.diac),'',word_uni)
    word_beta = uni2beta(word_uni)
    return diac_chars + m.non_beta_chars(word_beta)