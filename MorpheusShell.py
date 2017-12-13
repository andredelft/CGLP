import regex
import tools
import os
import requests
from bs4 import BeautifulSoup 


""" Run C script of Morpheus from Python
	Returns 1 for succes, 0 for failure"""
def cruncher(filename, switch = ''):
	if filename.split('.')[-1] == 'words':
		filename = os.path.splitext(filename)[0]
		print('Start Morpheus')
		os.system('MORPHLIB=%s %s %s %s' % (os.path.join('morpheus','setmlib'), os.path.join('morpheus','bin','cruncher') switch, filename))
		print('Exit Morpheus')
		return 1
	else:
		print('Incorrect file: extension .words is necessary for the Morpheus cruncher')
		return 0

""" Extracts all data from raw Morpheus output in the form [[[lemmata1],[categories]], [[lemmata2],[categories2]], ...]"""
def morph2data(morphout):
	outs = regex.findall('(?<=<NL>[A-Z] )([^\t ]+)[\t ](.+?)(?=</NL>)',morphout)
	data = []
	for out in outs:
		lemmata = [regex.sub('[/^—//1-3]','',tools.beta2uni(word)) for word in out[0].split(',')]
		categories = out[1].split()
		data.append([lemmata,categories])
	return(data)

def morpheus(tag, switch = '', cap = False):
	# Remove possible .words extension
	tag = os.path.splitext(tag)[0]
	
	cruncher(tag + '.words', switch)
	
	# Retry the capitalized words without capitals: SHOULD BE DONE IN THE C CODE, BUT DOESN'T DO IT
	if cap:
		with open(tag + '.failed') as f:
			words = f.read().split()
		words_cap = [me.remove_capital(word) for word in words if word[0] == '*']
		print("%s capitalized words found, retrying without capitals" % len(words_cap))
		with open(tag + '_cap.words','w') as f:
			f.write('\n'.join(words_cap))
		cruncher(tag + '_cap.words', switch)
		
		with open(tag + '.stats') as f:
			rep1 = f.read()
		with open(tag + '_cap.stats') as f:
			rep2 = f.read()
		n1 = [int(n) for n in regex.findall('[0-9.]+',rep1)[:2]]
		n2 = [int(n) for n in regex.findall('[0-9.]+',rep2)[:2]]
		rep_tot = 'TOTAL:  words %s, analyzed %s (%.2f pct)' % (n1[0], n1[1]+n2[1], 100*(n1[1]+n2[1])/n1[0])
		with open(tag + '_stats','a') as f:
			f.write('\nDecapitalization routine:\n' + rep2)
			f.write('\n' + rep_tot)
		print(rep_tot)
	
""" Scrape the morphological analysis from the online tool available at http://www.perseus.tufts.edu/hopper"""
def scrape_Perseus(word_beta):
	url = "http://www.perseus.tufts.edu/hopper/morph?l=%s&la=greek" % word_beta.translate(Pers_dict)
	content = requests.get(url).content.decode('utf-8')
	soup = BeautifulSoup(content, 'html.parser')
	
	# Pragmatic method of extracting relevant data: a bit sloppy, but works fine so far
	entries = [entry.get_text() for entry in soup.find_all('tr')][5:]

	data = []
	for entry in entries:
		data.append([soup.find('h4').text] + entry.split()[1:])
	return data