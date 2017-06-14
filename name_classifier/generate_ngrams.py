# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:12:46 2017

@author: jzuber
"""
import unicodecsv

import pandas as pd

import features
from load_names import load_born_names

from sklearn.feature_extraction.text import CountVectorizer

def find_ngrams(name_list, frac=0.0045):
    counter = CountVectorizer(analyzer='char', 
                              ngram_range=(2,4), 
                              min_df=frac)
    ngrams = counter.fit(name_list)
    data = ngrams.get_feature_names()
    letters = set("".join([name.lower() for name in name_list]))
    data = data + list(letters)
    with open('data_sets/ngrams.csv', 'w') as outf:
        w = unicodecsv.writer(outf)
        w.writerows([[n] for n in data])
    return data
    
def load_ngrams():
    with open('data_sets/ngrams.csv', 'r') as inf:
        r = unicodecsv.reader(inf, encoding='utf-8')
        ngrams = [name[0] for name in r]
    return ngrams

def all_ngrams():
    ngrams = load_ngrams()
    return lambda x: contains_ends_and_vowels(x, ngrams)
    
def contains_ends_and_vowels(name, ngrams):
    """
    A slightly better feature set.
    """    
    name = name.lower()    
    vowel_decile = int(10*features._vowel_count(name) / float(len(name)))
    retval = {'first_letter': name[0],
              'last_letter':name[-1],
              'vowel_decile':vowel_decile}
            
    keys = map(lambda c: u'contains_{}'.format(c), ngrams)
    vals = map(lambda c: c in name, ngrams)
    retval.update(dict(zip(keys, vals)))
    return retval
    
if __name__ == "__main__":
    old_boys, old_girls, old_ambig = load_born_names(1994)
    find_ngrams(old_boys + old_girls + old_ambig)

#
