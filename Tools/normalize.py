import regex
import unicodedata
import Tools.misc as m
import Tools.uni_beta_code as ubc

MACRON_BREVE = {
    '\u1fb8':'\u0391', # GREEK CAPITAL LETTER ALPHA WITH VRACHY
    '\u1fb9':'\u0391', # GREEK CAPITAL LETTER ALPHA WITH MACRON
    '\u1fb0':'\u03b1', # GREEK SMALL LETTER ALPHA WITH VRACHY
    '\u1fb1':'\u03b1', # GREEK SMALL LETTER ALPHA WITH MACRON
    '\u1fd8':'\u0399', # GREEK CAPITAL LETTER IOTA WITH VRACHY
    '\u1fd9':'\u0399', # GREEK CAPITAL LETTER IOTA WITH MACRON
    '\u1fd0':'\u03b9', # GREEK SMALL LETTER IOTA WITH VRACHY
    '\u1fd1':'\u03b9', # GREEK SMALL LETTER IOTA WITH MACRON
    '\u1fe8':'\u03a5', # GREEK CAPITAL LETTER UPSILON WITH VRACHY
    '\u1fe9':'\u03a5', # GREEK CAPITAL LETTER UPSILON WITH MACRON
    '\u1fe0':'\u03c5', # GREEK SMALL LETTER UPSILON WITH VRACHY
    '\u1fe1':'\u03c5', # GREEK SMALL LETTER UPSILON WITH MACRON
    '\u0304':'', # COMBINING MACRON
    '\u0306':''  # COMBINING BREVE
}

def macron_breve_filter(text):
    return text.translate(str.maketrans(MACRON_BREVE))

MISC_CHARS = {
    # LATIN
    '\u0069':'\u03b9', # LATIN SMALL LETTER I
    '\u006f':'\u03bf', # LATIN SMALL LETTER O
    '\u0070':'\u03c1', # LATIN SMALL LETTER P
    '\u0075':'\u03c5', # LATIN SMALL LETTER U
    '\u0076':'\u03bd', # LATIN SMALL LETTER V
    '\u0078':'\u03c7', # LATIN SMALL LETTER X
    '\u0041':'\u0391', # LATIN CAPITAL LETTER A
    '\u0042':'\u0392', # LATIN CAPITAL LETTER B
    '\u0049':'\u0399', # LATIN CAPITAL LETTER I
    '\u004b':'\u039a', # LATIN CAPITAL LETTER K
    '\u004d':'\u039c', # LATIN CAPITAL LETTER M
    '\u0054':'\u03a4', # LATIN CAPITAL LETTER T
    '\u0058':'\u03a7', # LATIN CAPITAL LETTER X
    '\u005a':'\u0396', # LATIN CAPITAL LETTER Z
    
    # CYRILLIC
    '\u0410':'\u0391', # CYRILLIC CAPITAL LETTER A
    '\u041c':'\u039c', # CYRILLIC CAPITAL LETTER EM
    '\u0424':'\u03a6', # CYRILLIC CAPITAL LETTER EF
    '\u0454':'\u03b5', # CYRILLIC SMALL LETTER UKRAINIAN IE
    '\u0457':'\u03ca', # CYRILLIC SMALL LETTER YI
    '\u0470':'\u03a8', # CYRILLIC CAPITAL LETTER PSI
    
    # GREEK_AND_COPTIC
    '\u03db':'\u03c2', # GREEK SMALL LETTER STIGMA
    
    # OTHER
    '\u05d0':'\u03ba', # HEBREW LETTER ALEF
    '\u00df':'\u03b2'  # LATIN SMALL LETTER SHARP S
}

def misc_chars_filter(text):
    return text.translate(str.maketrans(MISC_CHARS))

def normalize_greek(text, form = 'NFKC'):
    text = macron_breve_filter(text)
    text = unicodedata.normalize(form, text)
    text = misc_chars_filter(text)
    return text

def clean_beta(text_uni):
    text_uni = m.remove_diac(m.remove_capital(text_uni)) #filter capital mark (*) and diacritical marks in unicode string
    text_beta = ubc.uni2beta(text_uni).replace('\n',' ')
    return ''.join([char for char in text_beta if char not in m.non_beta_chars(text_beta)])
"""
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
        
    return ' '.join(words)"""