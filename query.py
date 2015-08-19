import itertools
from nltk import ngrams
from operator import itemgetter
import sys

#our name learning functions
from train import learn


#Sort a dictionary by value
def sortDictionary(x):
    return sorted(x.items(), key=operator.itemgetter(1),reverse=True)

#skipgram adapted from http://stackoverflow.com/questions/31847682/how-to-compute-skipgrams-in-python
def skipgrams(sequence, n, k):
    for ngram in ngrams(sequence, n + k, pad_right=True):
        head = ngram[:1]
        tail = ngram[1:]
        for skip_tail in itertools.combinations(tail, n - 1):
            if skip_tail[-1] is None:
                continue
            else:
                tmp_tail = ''
                for j in range(0,len(skip_tail)):
                    tmp_tail += skip_tail[j]
                    if j < len(skip_tail)-1:
                        tmp_tail+=' '
            yield ''.join(head) + ' ' + ''.join(tmp_tail)


#Generate bootstrapped version of query through skipgram
def bootstrapQuery(query):
    query=query.lower()
    query_skip_gram = []
    sz = len(query.split())
    for i in range(2,sz+1):
        query_skip_gram += list(skipgrams(query.split(), n=i, k=2))
    
    return query_skip_gram


#matches all possible skipgrams of query
#and stores high score matches
def matchQuerySkipgram(query_skipgram, ngramDict):
    matches={}
    for i in range(0,len(query_skipgram)):
        for ngr in ngramDict:
            res=ngr.search(query_skipgram[i])
            for nm in res:
                name, score = nm
                if score > .25:
                    if name in matches:
                        if score > matches[name]:
                            matches[name.encode('UTF-8')]=nm[1]
                    else:
                        matches[name.encode('UTF-8')]=score

    return matches

def match(query):
    res = matchQuerySkipgram(bootstrapQuery(query),learn())
    return res

