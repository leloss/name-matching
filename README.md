#Name Matching

by Leandro Loss - August 2015


## RUNNING THE CODE 

Unzip files, keeping the original folder structure. 
  The zip file comes with a sample dataset containing both
  English and Spanish names (See how to ingest new/more names
  below).
  
Code can then be tested using a python interpreter:

```sh

$ python
>>> import query
>>> query.match('John Smith')
```

BUT it has better interface when run from a browser:

```sh
$ python server.py
```

On browser, type address 127.0.0.1:5000

I also put it up online:

```sh
>> https://floating-hollows-2712.herokuapp.com/
```

Note: The name matching app is being hosted by
      a free tier web server (Heroku), which could
      present higher latency due to low hardware specs


##INGESTING DATA

Ingestion.py offers 2 ways of populating 
  the name data sets used for matching:
  
1) Cleaning raw, scrapped data from the web.
   Raw names can be scrapped from the web using
   a web scrapper such as the Google Chrome extension 
   data miner. These names are parsed by ingestion.py 
   cleansing the data and writing to another file that
   will be used for matching.
   
2) Synthetic names can be created by randomly grouping
   popular first and last names. ingestion.py allows
   one to set the number of resulting names.    

As one can notice, the above ingestions are either
  tedious or artificial. A better way to ingest names,
  scrape-orcid.py allows for scrapping real names using
  ORCID's API. That API lets anyone query by first or last 
  names, in addition to other types of information. I used 
  lists of popular family names in English and Spanish to
  pull full names from ORCID's public database.

##TECHNICAL APPROACH

Our approach utilizes n-gram models to represent a name
  space. As per its definition, an n-gram model is a type 
  of probabilistic language model for predicting chunks 
  of information in a sequence. It is simple and scales 
  well to large amounts of data. Because of its probabilistic
  approach, n-grams produce a score for how well these chunks
  fit the model. 
  
For our name matching problem, a name query
  is analyzed against a name data set encoded as n-grams.
  In other words, letters and syllables in a name are 
  modeled as a sequence of events. We used Python's n-gram 
  implementation. To improve the matching capability of our 
  algorithm, we bootstrap the name query into many "versions" of 
  the name. This is achieved by encoding the name query using a 
  skip-gram, which is a variation of n-gram models to consider 
  absence of events. That is a powerful concept in our approach 
  because it takes into account misspellings, contractions, 
  missing names, etc, that are common in search.
  
Summarizing, our approach is split by two main tasks: training 
  and querying. Training encodes lists of names into n-grams.
  Querying reads one name, encodes it as a skip-gram (becoming
  now many queries), which is compared to the trained set.

##TECHNICAL DETAILS

We used Python's n-gram library (https://pythonhosted.org/ngram/)
  and a public implementation of the skip-gram 
  (http://stackoverflow.com/questions/31847682/how-to-compute-skipgrams-in-python).
  Skip-gram's skipping parameter was set to 2, which means it is able to generalize
  the name query up to 2 "skips" (missing tokens). ngram's matching score is
  converted into a confidence score, and only scores above 25% are returned.
  
For training, despite all ingestion options above, the most realistic set
  is given by ORCID's scrapped names. We scrapped a total of 50000 names 
  from common English and Spanish family names (sources in ingestion.py).
  

##LIMITATIONS

The parameters set above limit the extent of name mistakes and variations allowed
  during querying. The size of the data set influences the retrieval time. 50k 
  names can be queried in less than 1 second. No formal complexity analysis 
  was performed but the retrieval time is expected to grow below linearly 
  due to optimizations by ngram.
  
Although only tested with English and Spanish (and some French, German, and Japanese
  names that were picked up during ingestion, the app is expected to keep its
  performance for any Roman alphabet-based language. It is not, however, optimized
  for other alphabets. 
  
Another improvement on the to-do list is the addition of a "nickname data set', so 
  names like 'William' can be matched against 'Will', 'Bill', etc.




