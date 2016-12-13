import os 
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from string import punctuation

wordnet_lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
stopwords = open(os.path.join(os.getcwd(),'data','stopwords.txt'),'r').read().splitlines()
aliem_stopwords =  open(os.path.join(os.getcwd(),'data','aliem-stopwords'),'r').read().splitlines()
months = ['January','February','March','April','May','June','July','August',
			'September','October','November','December']
stopwords +=aliem_stopwords

months = [month.lower() for month in months]
def isreference(word):
	return word.startswith('(') and word.endswith(')') and word[1].isdigit()

def cleanse(astr):
	blob = TextBlob(astr)

	tokens = []
	#get pos tags
	tagged_words = blob.tags
	for word,tag in tagged_words:
		token = word.lemmatize(get_wordnet_pos(tag)).lower()
		if tag not in ['CD','DT','TO','IN']:
			if not any([token in stopwords, token in months, 
						any([stopword in token for stopword in aliem_stopwords]),
						any([ord(ch)>128 for ch in token]), isreference(token),
						token in punctuation]):
				tokens += [token] 

	#get bigrams
	for phrase in blob.noun_phrases:
		if len(phrase.split()) == 2:
			tokens += [phrase]

	return tokens