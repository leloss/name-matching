import codecs
import ngram

#Encode list of names into an array of ngrams
def learn():

	Dict=[]
	num=1000
	#In the future, a language detector can be used to reduce the amount of data load in memory
	Dict.append(ngram.NGram(readRealNames('english')))
	Dict.append(ngram.NGram(readForeignRealNames('spanish')))
	Dict.append(ngram.NGram(readScrappedNames('english')))
	Dict.append(ngram.NGram(readForeignScrappedNames('spanish')))

	return Dict


def readScrappedNames(language):
	with open('data/scrapped_'+language+'_names.csv', 'r') as fin:
	    content = fin.read().splitlines()

	return content


def readForeignScrappedNames(language):
	with codecs.open('data/scrapped_'+language+'_names.csv', encoding='utf-8') as fin:
	    content = fin.read().splitlines()

	return content	

def readSyntheticNames(language):
	with open('data/synthetic_'+language+'_names.csv', 'r') as fin:
	    content = fin.read().splitlines()

	return content
	

def readForeignSyntheticNames(language):
	with codecs.open('data/synthetic_'+language+'_names.csv', encoding='utf-8') as fin:
	    content = fin.read().splitlines()

	return content
	

def readRealNames(language):

	with open('data/'+language+'_names.csv', 'r') as fin:
	    content = fin.read().splitlines()

	return content

def readForeignRealNames(language):

	with codecs.open('data/'+language+'_names.csv', encoding='utf-8') as fin:
	    content = fin.read().splitlines()

	return content
#TODO: Add more languages
