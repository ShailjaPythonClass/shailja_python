# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:12:46 2017

@author: jzuber
"""
import unicodecsv

import pandas as pd

import features
from improve_nlpk import label_names
from international_names import load_international_names

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

def features_to_df(feat_labels):
    labels = [1*(gender=='female') for (feats, gender) in feat_labels]
    columns = feat_labels[0][0].keys()
    temp_dict = {}
    for col in columns:
        value = feat_labels[0][0][col]
        if isinstance(value, bool):
            vect = [1*feats[col] for (feats, _) in feat_labels]
        elif isinstance(value, unicode) and len(value) == 1:
            vect = [ord(feats[col]) for (feats, _) in feat_labels]
        else:
            vect = [feats[col] for (feats, _) in feat_labels]
        temp_dict.update({col:vect})    
    df = pd.DataFrame(temp_dict)
    return df, labels

def find_ngrams(name_list):
    counter = CountVectorizer(analyzer='char', 
                              ngram_range=(2,4), 
                              min_df=0.007)
    ngrams = counter.fit(name_list)
    data = ngrams.get_feature_names()
    letters = set("".join([name.lower() for name in name_list]))
    data = data + list(letters)
    with open('../sample_data/ngrams.csv', 'w') as outf:
        w = unicodecsv.writer(outf)
        w.writerows([[n] for n in data])
    return data
    
def load_ngrams():
    with open('../sample_data/ngrams.csv', 'r') as inf:
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
    func = all_ngrams()
    boys, girls = load_international_names()
    test_set, train_set = label_names(boys, girls, func)
    
    classifier = RandomForestClassifier(n_estimators=100)
    train_df, train_labels = features_to_df(train_set)
    classifier.fit(train_df.as_matrix(), train_labels)
    test_df, test_labels = features_to_df(test_set)

    print classifier.score(test_df, test_labels)

