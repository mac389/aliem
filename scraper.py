import urllib, os, re, json, itertools, io 
from bs4 import BeautifulSoup

ontology = json.load(open(os.path.join(os.getcwd(),'list_of_blogs.json'),'rb'))

def dict_generator(aDict,pre=[]):
	pre = pre[:] if pre else []
	if isinstance(aDict,dict):
		for key,value in aDict.items():
			if isinstance(value,dict):
				for d in dict_generator(value,pre):
					yield d 
			elif isinstance(value, str):
				yield value
			else:
				yield pre + [value]
	else:
		yield aDict
urls = list(itertools.chain.from_iterable(dict_generator(ontology)))

def get_text(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html,'html.parser')
	return soup.findAll(text=True)

def visible(element):
	if element.parent.name in ['style','script','[document]','head','title']:
		return False
	elif re.match('<!--.*-->',unicode(element)):
		return False
	return True	

for website in ontology:
	path = os.path.join(os.getcwd(),'posts',website)
	if not os.path.exists(path):
	    os.makedirs(path)
	for title,url in ontology[website].iteritems():
		with io.open(os.path.join(path,title),'w',encoding='utf8') as fout:
			fout.write(' '.join(filter(visible,get_text(url))))
