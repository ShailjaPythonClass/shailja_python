# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:37:40 2017

@author: jzuber
"""
import unicodecsv
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
    
if __name__ == "__main__":
    from load_names import load_born_names
    boys, girls, ambig = load_born_names(1994)
    ngrams = find_ngrams(boys + girls + ambig)
    