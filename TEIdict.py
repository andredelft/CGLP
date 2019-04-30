from lxml import etree
import regex
import Tools.normalize as norm
import os

URL = "{http://www.tei-c.org/ns/1.0}"

def FJO_CC(DIR):
    tree = etree.parse(DIR)
    root = tree.getroot()
    entries = root.find('%stext/%sbody'%(URL,URL)).getchildren()
    wordlist = [child.find('%sform/%sorth'%(URL,URL)).text for child in entries]
    wordlist = [regex.sub('[\[\]]','',word) for word in wordlist]
    return wordlist

def MONTANARI(DIR):
    with open(os.path.join(DIR,'lemlist_filtered.txt')) as f:
        wordlist = f.read().split('\n')
    return [regex.sub('[0-9]+/. ','',word) for word in wordlist]

class dictionary:
    def __init__(self, DIR, tag = ''):
#       self.tree = etree.parse(filename)
#       self.root = self.tree.getroot()
#       self.entries = self.root.find('%stext/%sbody'%(URL,URL)).getchildren()
#       self.wordlist = [child.find('%sform/%sorth'%(URL,URL)).text for child in self.entries]
#       self.wordlist = regex.sub("[ ’‛†',\-.0-9>?\[\]]",'',self.wordlist)
#       self.wordlist = [cltk_normalize(child.find('%sform/%sorth'%(URL,URL)).text) for child in self.entries]
        
        self.tag = tag
        
        if tag != '':
            try:
                self.wordlist = eval(tag)(DIR)
            except NameError as error:
                raise NameError("{0} ('{1}' is not a recognized dictionary format)"%(error,tag))
