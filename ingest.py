from random import randint
from codecs import open
from re import sub
#import csv


#save cleansed files to disk
def writeCleanFile(fname, data):
	with open(fname+'.csv', 'wb') as fout:
		for nm in data:
			fout.write(nm+'\n')
	fout.close()

#save cleansed files to disk
def writeCleanFileUTF(fname, data):
	with codecs.open(fname+'.csv', 'with', encoding='utf-8') as fout:
		for nm in data:
			fout.write(nm+'\n')
	fout.close()

#generates synthetic english names for training 
def generateEnglishSynthNames(num):
	with open("raw/yob2014.txt", "r") as fin:
	    content_firstname = fin.read().splitlines()

	with open("raw/dist.all.last.txt", "r") as fin:
	    content_lastname = fin.read().splitlines()

	firstnames=[]
	for i in content_firstname:
	    firstnames.append(i.split(',')[0])
	lastnames=[]
	for i in content_lastname:
	    lastnames.append(i.split(' ')[0])
	    
	synth_eng_names=[]
	n=len(firstnames)
	m=len(lastnames)

	for k in range(num):
	    i = random.randint(0,n-1)
	    j = random.randint(0,m-1)
	    synth_eng_names.append(firstnames[i].lower()+' '+lastnames[j].lower())

	writeCleanFile('synthetic_english_names',synth_eng_names)


#generates synthetic spanish names for training 
#data scrapped from http://www.babycenter.com/0_100-most-popular-hispanic-baby-names-of-2011_10363639.bc 
#              and http://genealogy.familyeducation.com/browse/origin/spanish
def generateSpanishSynthNames(num):
	with codecs.open('raw/spanish_firstnames.txt', encoding='utf-8') as fin:
	    content_firstname = fin.read().splitlines()

	with codecs.open('raw/spanish_familynames.csv', encoding='utf-8') as fin:
	    content_lastname = fin.read().splitlines()

	firstnames=[]
	for i in content_firstname:
	    firstnames.append(i)
	lastnames=[]
	for i in content_lastname:
	    lastnames.append(i.split(',')[0])

	synth_spa_names=[]
	n=len(firstnames)
	m=len(lastnames)

	for k in range(num):
	    i = random.randint(0,n-1)
	    j = random.randint(0,m-1)
	    synth_spa_names.append(firstnames[i].lower()+' '+lastnames[j].lower())

	writeCleanFileUTF('synthetic_spanish_names',synth_spa_names)

#Clean English names scrapped from https://en.wikipedia.org/wiki/List_of_English_people
def readEnglishNames():
	#open file
	with open("raw/english_names.csv", "r") as fin:
	    content = fin.read().splitlines()

	#apply cleaning rules and save remaining names in eng_names
	rm_list = '"'
	bl_list = '0123456789'
	nm_list = ['List','Jump']

	eng_names=[]
	for line in content:
	    token=line.split(',')[0]
	    #remove parentheses text from name
	    token = re.sub(r'\([^)]*\)', '', token)
	    #remove one-word names
	    names = token.split(' ')
	    if len(names) < 2 or names[0] in nm_list:
	        continue
	    #block names with numbers in it
	    block = False
	    for i in range(0,len(bl_list)):
	        if bl_list[i] in token:
	            block = True
	            break
	    if block:
	        continue
	    #block lower case names
	    for nm in names:
	        if nm.islower():
	            block = True
	            break
	    if block:
	        continue
	    #remove quotes from names    
	    for i in range(0,len(rm_list)):
	        token = token.replace(rm_list[i],"")
	    
	    eng_names.append(token.lower()) #store names in lower case

	writeCleanFile('english_names',eng_names)


#Clean Spanish names scrapped from 
def readSpanishNames():
	#open file
	with codecs.open('raw/spanish_names.txt', encoding='utf-16') as fin:
	    content = fin.read().splitlines()

	#apply cleaning rules and save remaining names in spa_names
	rm_list = '"'
	bl_list = '0123456789'
	nm_list = ['List','Jump']

	spa_names=[]
	for line in content:
	    token=line.split(',')[0]
	    #remove parentheses text from name
	    token = re.sub(r'\([^)]*\)', '', token)
	    #remove one-word names
	    names = token.split(' ')
	    if len(names) < 2 or names[0] in nm_list:
	        continue
	    #block names with numbers in it
	    block = False
	    for i in range(0,len(bl_list)):
	        if bl_list[i] in token:
	            block = True
	            break
	    if block:
	        continue
	    #block lower case names
	    for nm in names:
	        if nm.islower():
	            block = True
	            break
	    if block:
	        continue
	    #remove quotes from names    
	    for i in range(0,len(rm_list)):
	        token = token.replace(rm_list[i],"")
	    
	    spa_names.append(token.lower())  #store names in lower case

	writeCleanFileUTF('spanish_names',spa_names)


def main():
	num=10000
	generateEnglishSynthNames(num)
	readEnglishNames()
	generateSpanishSynthNames(num)
	readSpanishNames()

#call main as default
main()
