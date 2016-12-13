import os, json

import utils as tech
import numpy as np 
import matplotlib.pyplot as plt 
import Graphics as artist

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from collections import Counter
from matplotlib import rcParams

from wordcloud import WordCloud
#Create texts
#Sklearn for lsa
rcParams['text.usetex'] = True

FORMATTED_FOR_LSA = os.path.join(os.getcwd(),'data','flat-cleansed-database.json')

titles = open(os.path.join(os.getcwd(),'data','flat-post-names')).read().splitlines()

if not os.path.isfile(FORMATTED_FOR_LSA):
	blogs = json.load(open(os.path.join(os.getcwd(),'data','flat-database.json'),'r'))
	#Order blog posts by titles to maintain order for later analysis

	texts = [tech.cleanse(blogs[title][0]) for title in titles]
	json.dump(dict(zip(titles,texts)), open(FORMATTED_FOR_LSA,'w'))

else: 
	blogs = json.load(open(FORMATTED_FOR_LSA))
	texts = [' '.join(blogs[title]) for title in titles]


vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                             min_df=2, stop_words='english',
                             use_idf=True)

tfidf = vectorizer.fit_transform(texts)
svd = TruncatedSVD(100)
lsa = make_pipeline(svd, Normalizer(copy=False))
X = lsa.fit_transform(tfidf)

explained_variance = svd.explained_variance_ratio_.sum()
top_3_dimensions = np.argsort(svd.explained_variance_ratio_)[::-1][:3]
feature_names = vectorizer.get_feature_names()

#Scatterplot
projections = {title:{} for title in titles}

for idx in xrange(len(titles)):
	for dimension in top_3_dimensions:
		projection = 0	
		axis = svd.components_[dimension]
		counted_tokens = dict(Counter(texts[idx].split()))
		for token in feature_names:
			if token in texts[idx].split():
				projection += axis[feature_names.index(token)] * counted_tokens[token]
		projections[titles[idx]][dimension] = projection

#Scale third dimension
max_third_dim = max([projections[title][top_3_dimensions[-1]] for title in projections])
min_third_dim = min([projections[title][top_3_dimensions[-1]] for title in projections])

scale = lambda x: (x-min_third_dim)/(max_third_dim-min_third_dim)
x,y,z = zip(*[(projections[title][top_3_dimensions[0]],
				projections[title][top_3_dimensions[1]],
				scale(projections[title][top_3_dimensions[-1]])) 
				for title in projections])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x,y,c=z, cmap='gray')
artist.adjust_spines(ax)
ax.set_xlabel(artist.format("First Semantic Dimension"))
ax.set_ylabel(artist.format("Second Semantic Dimension"))
plt.tight_layout()
plt.axis('equal')
plt.savefig(os.path.join(os.getcwd(),'imgs','scatterplot'))
#Scatterplot

del fig, ax

#Associate weights with stop_word
word_cloud = {}
for dimension in top_3_dimensions:
	axis = svd.components_[dimension]

	word_cloud[dimension] = {token:(axis[feature_names.index(token)]-axis.min())/(axis.max()-axis.min())
								for token in feature_names}

	wordcloud = WordCloud(background_color="white").generate_from_frequencies(word_cloud[dimension].items())
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.imshow(wordcloud)
	plt.axis("off")
	plt.savefig(os.path.join(os.getcwd(),'imgs','semantic-dimension-%d'%dimension))
#Word cloud

