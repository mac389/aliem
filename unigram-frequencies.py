import os, collections, nltk 
import matplotlib.pyplot as plt 
import Graphics as artist

from matplotlib import rcParams
from string import punctuation
rcParams['text.usetex'] = True

stopwords = open('./data/stopwords.txt').read().splitlines()
stopwords += open('./data/aliem-stopwords').read().splitlines()
months = ['January','February','March','April','May','June','July','August',
			'September','October','November','December']

months = [month.lower() for month in months]
def isreference(word):
	return word.startswith('(') and word.endswith(')') and word[1].isdigit()

CLEANSED = 'cleansed'

corpus = []
for root, dirs, files in os.walk(os.path.join(os.getcwd(),'posts')):
	if '.git' not in root: #Ignore Git files
		if files:
			for filename in files:
				if filename.endswith('cleansed'):
					corpus += [x.lower() for x in open(os.path.join(root,filename),'rb').read().splitlines()]

corpus = ' '.join(corpus).split()
print len(corpus)
print len(set(corpus))
#10860 words
#3550 unique words

unigrams = sorted(dict(collections.Counter(corpus)).items(), 
					key=lambda item:item[1], reverse=True)

#Remove stopwords
unigrams = [(word,freq) for word,freq in unigrams 
			if not any([word in stopwords, word.lower() in months, isreference(word),
				 word.isdigit(),word in punctuation, any([ord(ch)>128 for ch in word])])]

artist.generic_frequency_plot(unigrams)