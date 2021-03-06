import regex
import unicodedata

import Tools.misc as m
import Tools.uni_beta_code as ubc

MACRON_BREVE = {
    '\u0304':'', # COMBINING MACRON
    '\u0306':'', # COMBINING BREVE
    '\u0342':'', # COMBINING GREEK PERISPOMENI
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
    '\u1fe1':'\u03c5'  # GREEK SMALL LETTER UPSILON WITH MACRON
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
    
    # GREEK AND COPTIC
    '\u03db':'\u03c2', # GREEK SMALL LETTER STIGMA
    
    # OTHER
    '\u00b5':'\u03bc', # MICRO SIGN
    '\u05d0':'\u03ba', # HEBREW LETTER ALEF
    '\u00df':'\u03b2', # LATIN SMALL LETTER SHARP S
    '\u00a1':'\u03b9'  # INVERTED EXCLAMATION MARK
}

def misc_chars_filter(text):
    return text.translate(str.maketrans(MISC_CHARS))

def normalize_greek(text, form = 'NFC'):
    text = unicodedata.normalize('NFD',text) # Decomposition to filter combined characters better
    text = misc_chars_filter(text)
    text = macron_breve_filter(text)
    if form != 'NFD':
        text = unicodedata.normalize(form, text)
    return text