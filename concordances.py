import MorpheusShell as MS
import Tools.uni_beta_code as ubc
import TEIdict
import os

dictionaries = []
dictionaries.append(TEIdict.dictionary('../Corpora/FJO/FJO_CC_VOLUME I/VOLUME I.xml', tag = 'FJO_CC'))
dictionaries.append(TEIdict.dictionary('../Corpora/FJO/FJO_CC_VOLUME II/VOLUME II.xml', tag = 'FJO_CC'))
dictionaries.append(TEIdict.dictionary('../Corpora/dictionaries', tag = 'MONTANARI'))

def find_match(lemma):
    for i in range(len(dictionaries)):
        try:
            #index = dictionaries[i].wordlist.index(lemma)
            #return dictionaries[i].entries[index]
            # FOR NOW ONLY FOCUS ON LEMLIST
            return dictionaries[i].wordlist.index(lemma),dictionaries[i].tag
        except ValueError:
            pass
    return None

# Checks how many words in tag.words appear in the given dictionaries
def match(tag):
    tag = os.path.splitext(tag)[0]
    MS.morpheus(tag)
    
    with open(tag + '.morph') as f:
        lines = f.read().split('\n')
    if len(lines)%2 != 0 and lines[-1] == '':
        del lines[-1]
        
    inputs = [] # Inputs of all succesfully analyzed words
    lemmata = [] # lemmata[i] is a list of all different lemmata matched by morpheus with input[i]
    for i,line in enumerate(lines):
        if i % 2 == 0:
            inputs.append(ubc.beta2uni(line))
        else:
            morphdata = MS.morph2data(line)
            lem = []
            for md in morphdata:
                lem += [l for l in list(set(md[0])) if l not in lem]
            lemmata.append(lem)
    
    no_lemmata = [len(lem) for lem in lemmata]
    no_matches = [sum([1 for l in lem if find_match(l) != None]) for lem in lemmata]
    print('Succes rate: %.2f pct'%(100 * sum([1 for i in no_matches if i != 0])/len(inputs)))
    print([inputs[i] for i in range(len(inputs)) if no_matches[i] == 0])