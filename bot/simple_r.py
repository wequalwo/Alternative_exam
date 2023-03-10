import nltk
from nltk.corpus import words
from nltk.metrics.distance import edit_distance, jaccard_distance
from nltk.util import ngrams
import pandas as pd
import numpy as np

import re
import math
import string
from collections import Counter
import requests

import codecs
with codecs.open('top10000.txt', 'r', encoding = 'utf-8') as file:
    correct_spellings = file.read().replace('\n', ' ') #список правильных слов

correct_spellings = re.findall(r'[а-ё]+', correct_spellings.lower())
#correct_spellings = [w for w in correct_spellings if len(w) > 2]
#correct_spellings[:10]

spellings_series = pd.Series(correct_spellings) # проиндексированный список этих словv

def jaccard(entries, gram_number):
    outcomes = []
    for entry in entries: 
        loopspellings = spellings_series[spellings_series.str.startswith(entry[0])]
        distances = ((jaccard_distance(set(ngrams(entry, gram_number)), set(ngrams(word, gram_number))), word) for word in correct_spellings)
        closest = min(distances)
        outcomes.append(closest[1])
    return outcomes

def JDreco(entries=['чуство']):
#finds the closest word based on jaccard distance
    return jaccard(entries, 1)

def levenstein(entries = ['чуство']):
    outcomes = []
    for entry in entries:
        distances = ((edit_distance(entry, word), word) for word in correct_spellings)
        closest = min(distances)
        outcomes.append(closest[1])
        
    return outcomes
