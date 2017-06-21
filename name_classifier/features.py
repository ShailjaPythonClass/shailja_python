# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:54:34 2017

@author: jzuber
"""
import unicodedata

from ngrams import load_ngrams

def ngrams_ends_and_vowels(name, ngrams=None):
    """
    A slightly better feature set that checks for the presence
    of ngrams in addition to the first letter, last letter and
    the portion of the name that is vowels.
    """
    if not ngrams:
        ngrams = load_ngrams()
    name = name.lower()
    vowel_decile = int(10*_vowel_count(name) / float(len(name)))
    retval = {'first_letter': name[0],
              'last_letter':name[-1],
              'vowel_decile':vowel_decile}

    keys = map(lambda c: u'contains_{}'.format(c), ngrams)
    vals = map(lambda c: c in name, ngrams)
    retval.update(dict(zip(keys, vals)))
    return retval


def ends_and_vowels(name):
    """
    A slightly better feature set.
    """
    name = name.lower()
    vowel_decile = int(10*_vowel_count(name) / float(len(name)))
    return {'first_letter': name[0],
            'last_letter':name[-1],
            'vowel_decile':vowel_decile}

def _to_ascii(name):
    name = unicode(name.lower())
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore')

def _vowel_count(name):
    temp = _to_ascii(name)
    return sum(map(temp.count, "aeiou"))


if __name__=="__main__":
    py_names = sorted(['James', 'Shailja', 'Chris', 'Dave', 'Sheng',
                'Claire', 'Akshay', 'Catherine', 'Rhonda', 'Emily',
                'Purti'])
    for name in py_names:
        print name, ends_and_vowels(name)
        
    for name in py_names:
        print name, ngrams_ends_and_vowels(name)
