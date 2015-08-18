############################
##Parse names from ORCID Name database (http://orcid.org)
##based on set of common family names
import requests
import json
import codecs

def parseNames(response):
	fn = ''
	names=[]
	for line in response.text.splitlines():
		if 'given-names' in line:
			fn = line.split('>')[1].split('<')[0].title()
		if fn != '' and 'family-name' in line:
			name = fn+' '+line.split('>')[1].split('<')[0].title()
			names.append(name)
			fn = ''
	return names

def readEnglishFamilyNames():
	with open('data/english_names.csv', 'r') as fin:
	    return fin.read().splitlines()

def readSpanishFamilyNames():
	with codecs.open('data/spanish_names.csv', encoding='utf-8') as fin:
	    return fin.read().splitlines()

def scrapeOrcidNames(content, lim):
	list_of_names=[]
	for i in content:
		lastname = i.split(' ')[1]
		print 'Scraping '+lastname,
		url = 'http://pub.orcid.org/v1.2/search/orcid-bio/?q=family-name:'+lastname+'&start=0&rows=10000'
		response = requests.get(url)
		list_of_names.extend(parseNames(response))
		print ': ',len(list_of_names)
		if len(list_of_names) > lim:
			break
	return list_of_names


def writeCleanFileUTF(fname, data):
	with codecs.open(fname+'.csv', 'with', encoding='utf-8') as fout:
		for nm in data:
			fout.write(nm+'\n')
	fout.close()

def main():
	MAX=25000
	print '---SPANISH---'
	writeCleanFileUTF('data/scrapped_spanish_names',scrapeOrcidNames(readSpanishFamilyNames(),MAX))
	print '---ENGLISH---'
	writeCleanFileUTF('data/scrapped_english_names',scrapeOrcidNames(readEnglishFamilyNames(),MAX))

main()

# name='Sanchez'
# url = 'http://pub.orcid.org/v1.2/search/orcid-bio/?q=family-name:'+name
# response = requests.get(url)
# print response.text
