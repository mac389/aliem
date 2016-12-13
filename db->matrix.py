import os, json

flat_database = {} 

for root, dirs, files in os.walk(os.path.join(os.getcwd(),'posts')):
	if '.git' not in root: #Ignore Git files
		if files:
			for filename in files:
				if filename.endswith('cleansed'):
					text = open(os.path.join(root,filename),'rb').read().splitlines()
					flat_database['%s-%s'%(os.path.basename(root),filename)] = text

OUT_NAME = "flat-database.json"
OUT_FILE = os.path.join(os.getcwd(),'data',OUT_NAME)
json.dump(flat_database,open(OUT_FILE,'wb'))
with open(os.path.join(os.getcwd(),'data','flat-post-names'),'w') as outfile:
	for name in flat_database.iterkeys():
		print>>outfile,name