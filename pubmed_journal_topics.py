# Author: Wei Wang
# Upload date: 2017.08.06


# Python 3

import re

from Bio import Entrez, Medline
Entrez.email = 'YOUR EMAIL'

from nltk.stem import SnowballStemmer

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.hdpmodel import HdpModel
from gensim.parsing.preprocessing import STOPWORDS


def gather_pubmed_journal_article_titles(journal, mindate, maxdate):
# https://dataguide.nlm.nih.gov/eutilities/utilities.html
	handle = Entrez.esearch(db = 'pubmed', term = '{}[Journal]'.format(journal), retmax = 100000, retmode = 'text', mindate = '{}'.format(mindate), maxdate = '{}'.format(maxdate))
	records = Entrez.read(handle)
	id_list = records['IdList']
	#print(idlist) # this is a list	

	handle = Entrez.efetch(db = 'pubmed', id = id_list, rettype = 'medline', retmode = 'text')
	records = Medline.parse(handle)	

	file = open('{}_article_titles.txt'.format(journal),'w')

	for record in records:
		title = re.sub(r'(?!\d)[.,()?;:](?!\d)', '', record.get('TI'))
		file.write(title + '\n')

	file.close()


def generate_topics(journal, num_topics, num_words, passes):
# num_words: number of words we want to see from each topic (defult is 10)
# passes: times to go over the data. 1 can be used for large corpus	

	filename = '{}_article_titles.txt'.format(journal)	

	with open(filename) as f:
		documents = f.readlines()	

	texts = [[word for word in document.lower().split() if word not in STOPWORDS] for document in documents]	

	stemmer = SnowballStemmer('english')
	texts_stemmed = [[stemmer.stem(word) for word in text] for text in texts]	

	dictionary = corpora.Dictionary(texts_stemmed)
	corpus = [dictionary.doc2bow(text) for text in texts] # bow means bag of words	
	

	# LDA model 
	lda = LdaModel(corpus, id2word = dictionary, num_topics = num_topics, passes = passes)	

	for topic in lda.print_topics(num_words = num_words):
	    topicNumber = topic[0]
	    print(topicNumber, ':', sep = '')
	    listOfTerms = topic[1].split('+')
	    for term in listOfTerms:
	        listItems = term.split('*')
	        print('  ', listItems[1], '(', listItems[0], ')', sep = '')	
	

	'''
	# HDP model
	hdp = HdpModel(corpus, id2word = dictionary)	

	for topic in hdp.print_topics(num_words = num_words):
	    topicNumber = topic[0]
	    print(topicNumber, ':', sep = '')
	    listOfTerms = topic[1].split('+')
	    for term in listOfTerms:
	        listItems = term.split('*')
	        print('  ', listItems[1], '(', listItems[0], ')', sep = '')
	'''
