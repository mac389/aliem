import os, nltk, io
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def cleanse(text):
	text = ' '.join([item for item in text if item])
	return strip_tags(text) 

for root, dirs, files in os.walk(os.path.join(os.getcwd(),'posts')):
	if '.git' not in root: #Ignore Git files
		if files:
			for filename in files:
				if not filename.endswith('cleansed'):
					text = cleanse(open(os.path.join(root,filename),'rb').read().splitlines())
					cleansed_filename = '%s-cleansed'%os.path.join(root,filename)
					with open(cleansed_filename,'w') as fout:
						print>>fout,' '.join(text.split())