""" Edit from the cltk beta_to_unicode script, to do the reverse operation """
import unicodedata
import string
import json
import os
import regex

from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.utils.formatter import cltk_normalize

import Tools.misc as m

import inspect
cwd = os.path.dirname(inspect.getfile(inspect.currentframe()))
with open(os.path.join(cwd,'LOWER.json')) as f:
    LOWER_dict = json.load(f)
with open(os.path.join(cwd,'UPPER.json')) as f:
    UPPER_dict = json.load(f)
uni_dict = {**UPPER_dict,**LOWER_dict}

def uni2beta(text_uni, normalize = True):
    if normalize:
        text_uni = unicodedata.normalize('NFC',text_uni)
    text_beta = text_uni.translate(str.maketrans(uni_dict))
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

def non_greek_chars(text_uni, unique = True, whitespace = False):
    beta_chars = regex.sub('[^*{}a-zA-Z]'.format(m.diac),'',text_uni)
    text_beta = uni2beta(text_uni, normalize = False)
    if not whitespace:
        text_beta = regex.sub(r'\s','',text_beta)
    if unique:
        return sorted(set(beta_chars + m.non_beta_chars(text_beta)))
    else:
        return list(beta_chars + m.non_beta_chars(text_beta))