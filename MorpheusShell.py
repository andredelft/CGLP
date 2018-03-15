import regex
import os
import requests
from bs4 import BeautifulSoup

import Tools.misc as m
import Tools.uni_beta_code as ubc

import inspect
__file__ = os.path.dirname(inspect.getfile(inspect.currentframe()))

""" Run C script of Morpheus from within Python
    Morpheus root folder should be located at ./morpheus
    Returns 1 for succes, 0 for failure"""
def cruncher(filename, switch = ''):
    if filename.split('.')[-1] == 'words':
        filename = os.path.splitext(filename)[0]
        print('Start Morpheus')
        os.system('MORPHLIB={} {} {} {}'.format(os.path.join(__file__,'morpheus','stemlib'),
                                                os.path.join(__file__,'morpheus','bin','cruncher'),
                                                switch, filename))
        print('Exit Morpheus')
        return 1
    else:
        print('Incorrect file: extension .words is necessary for the Morpheus cruncher')
        return 0

def cruncher_single(word_beta, switch = '', raw = False, beta = True):
    with open(os.path.join(__file__,'log.words'),'w') as f:
        f.write(word_beta)
    cruncher(os.path.join(__file__,'log.words'),switch)
    with open(os.path.join(__file__,'log.morph')) as f:
        try:
            morphout = f.read().split('\n')[-2]
        except IndexError:
            morphout = ''
        
    os.remove(os.path.join(__file__,'log.words'))
    os.remove(os.path.join(__file__,'log.failed'))
    os.remove(os.path.join(__file__,'log.stats'))
    os.remove(os.path.join(__file__,'log.morph'))
    
    if raw:
        return morphout
    else:
        return morph2data(morphout,beta)

def compile_stemlib(lang = 'Greek'):
    try:
        cwd = os.getcwd()
        os.chdir(os.path.join(__file__,'Morpheus','stemlib',lang))
        os.system('export PATH=$PATH:{};MORPHLIB=.. make all'.format(os.path.join('..','..','bin')))
        os.chdir(cwd)
    except FileNotFoundError:
        print('{} is an unsupported language'.format(lang))
        return

""" Extracts all data from raw Morpheus output in the form:
[[[lemmata1],[categories]], [[lemmata2],[categories2]], ...]"""
def morph2data(morphout,beta=False):
    outs = regex.findall('(?<=<NL>[A-Z] )([^\t ]+)[\t ](.+?)(?=</NL>)',morphout)
    data = []
    for out in outs:
        if beta:
            lemmata = [word for word in out[0].split(',')]
        else:
            lemmata = [ubc.beta2uni(regex.sub('[_^0-9]','',word)) for word in out[0].split(',')]
        categories = out[1].split()
        data.append([lemmata,categories])
    return(data)

def morpheus(tag, switch = '', cap = False):
    # Remove possible .words extension
    tag = os.path.splitext(tag)[0]
    
    cruncher(tag+'.words', switch)
    
    # Retry the capitalized words without capitals:
    # SHOULD BE DONE IN THE SOURCE CODE, BUT DOESN'T DO IT FOR SOME REASON
    if cap:
        with open(tag + '.failed') as f:
            words = f.read().split()
        words_cap = [m.remove_capital(word) for word in words if word[0] == '*']
        if len(words_cap) == 0:
            print('0 capitalized words found')
            return
        else:
            print("{} capitalized word{} found, retrying without capitals".format(len(words_cap),
                                                                                  '' if len(words_cap) == 1 else 's'))
        with open(tag + '_cap.words','w') as f:
            f.write('\n'.join(words_cap))
        cruncher(tag + '_cap.words', switch)
        
        with open(tag + '.stats') as f:
            rep1 = f.read()
        with open(tag + '_cap.stats') as f:
            rep2 = f.read()
        n1 = [int(n) for n in regex.findall('[0-9.]+',rep1)[:2]]
        n2 = [int(n) for n in regex.findall('[0-9.]+',rep2)[:2]]
        rep_tot = 'TOTAL:  words {}, analyzed {} ({:.2f} pct)'.format(n1[0], n1[1]+n2[1], 100*(n1[1]+n2[1])/n1[0])
        with open(tag + '.stats','a') as f:
            f.write('\nDecapitalization routine:\n' + rep2)
            f.write('\n' + rep_tot)
        print(rep_tot)

def add(nom_file = 'Morpheus/stemlib/Greek/stemsrc/nom37.montanari'):
    line = input()
    while line != 'exit':
        morphout = cruncher_single(line,raw=True)
        if morphout == '':
            print('{} not recognized by Morpheus'.format(line))
            type = input('Type: ')
            lemma = input('Lemma: ')
            stem = input('Stem: ')
            tags = input('Tags: ')
            inflection_group = input('Inflection group: ')
            if not os.path.isfile('Morpheus/stemlib/Greek/endtables/source/{}.end'.format(inflection_group)):
                print('Inflection group not recognized')
            else:
                data = ":le:{}\n:{}:{} {} {}".format(lemma,type,stem,inflection_group,tags)
                print(data)
                with open(nom_file,'a') as f:
                    f.write('\n\n{}'.format(data))
        else:
            print(morphout)
        line = input()    

Pers_dict = {
    ord('('): '%28',
    ord(')'): '%29',
    ord('/'): '%2F',
    ord('\\'): '%5C',
    ord('='): '%3D',
    ord('|'): '%7C'
}

# Scrape the morphological analysis from the online tool available at http://www.perseus.tufts.edu/hopper
def scrape_Perseus(word_beta):
    url = "http://www.perseus.tufts.edu/hopper/morph?l={}&la=greek".format(word_beta.translate(Pers_dict))
    content = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    
    # Pragmatic method of extracting relevant data: a bit sloppy, but works fine so far
    entries = [entry.get_text() for entry in soup.find_all('tr')][5:]

    data = []
    for entry in entries:
        data.append([soup.find('h4').text] + entry.split()[1:])
    return data