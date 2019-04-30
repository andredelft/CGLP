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
        first_diac = regex.search('(?<=^[a-zA-Z])[{}]+(?=[a-zA-Z])'.format(diac), word_beta)
        if first_diac != None:
            return '*' + first_diac.group() + word_beta[0] + word_beta[first_diac.end():]
        else:
            return '*' + word_beta
    else:
        return word_beta

# Return characters that aren't part of the beta code

    
def remove_diac(word_beta):
    return regex.sub('[{}]'.format(diac),'',word_beta)

def decompose(string, filename = ''):
    decomp = []
    for char in string:
        if len(hex(ord(char))[2:]) <= 4:
            HEX = 'U+{:>4}'.format(hex(ord(char))[2:]).replace(' ','0')
        else:
            HEX = hex(ord(char)).replace('0x','U+')
        try:
            NAME = unicodedata.name(char)
        except ValueError:
            NAME = ''
        decomp.append(' '.join([char,HEX,NAME]))
    if filename != '':
        with open(filename, 'w') as f:
            f.write('\n'.join(decomp))
    else:
        print('\n'.join(decomp))