# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:54:34 2017

@author: jzuber
"""
import string
import unicodedata

def _to_ascii(name):
    name = unicode(name.lower())
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore')

def _vowel_count(name):
    temp = _to_ascii(name)
    return sum(map(temp.count, "aeiou"))
    
def ends_and_vowels(name):
    """
    A slightly better feature set.
    """
    name = name.lower()        
    vowel_decile = int(10*_vowel_count(name) / float(len(name)))
    return {'first_letter': name[0],
            'last_letter':name[-1],
            'vowel_decile':vowel_decile}
            
            
if __name__=="__main__":
    py_names = sorted(['James', 'Shailja', 'Chris', 'Dave', 'Sheng', 
                'Claire', 'Akshay', 'Catherine', 'Rhonda', 'Emily',
                'Purti'])
    for name in py_names:
        print name, ends_and_vowels(name)
            