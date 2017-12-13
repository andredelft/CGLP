from lxml import etree
from cltk.corpus.utils.formatter import cltk_normalize
import regex

URL = "{http://www.tei-c.org/ns/1.0}"

def FJO_CC(wordlist):
	for i,word in enumerate(wordlist):
		wordlist[i] = regex.sub('[\[\]]','',word)
	return(wordlist)

class dictionary:
	def __init__(self, filename, name = ''):
		self.tree = etree.parse(filename)
		self.root = self.tree.getroot()
		self.entries = self.root.find('%stext/%sbody'%(URL,URL)).getchildren()
#		self.wordlist = [child.find('%sform/%sorth'%(URL,URL)).text for child in self.entries]
#		self.wordlist = regex.sub("[ ’‛†',\-.0-9>?\[\]]",'',self.wordlist)
		
		self.wordlist = [cltk_normalize(child.find('%sform/%sorth'%(URL,URL)).text) for child in self.entries]
		if name != '':
			try:
				self.wordlist = eval(name)(self.wordlist)
			except NameError:
				print("'%s' is not a recognized dictionary format"%name)
