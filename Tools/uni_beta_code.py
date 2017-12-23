""" Edit from the cltk beta_to_unicode script, to do the reverse operation """
from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.utils.formatter import cltk_normalize
import string
import json
import os

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
         text_uni = cltk_normalize(text_uni)
         text_beta = text_uni.translate(dict)
         text_beta = text_beta.translate(str.maketrans(string.ascii_uppercase,string.ascii_lowercase))
         return text_beta

def beta2uni(text_beta):
         text_beta = text_beta.translate(str.maketrans(string.ascii_lowercase,string.ascii_uppercase))
         text_uni = Replacer().beta_code(text_beta)
         return text_uni
