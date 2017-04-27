# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:08:12 2017

@author: jzuber
"""
import inspect

import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
    
import features

from international_names import load_international_names

def all_functions_from_module(module):
    """ 
    Get all non-private functions in module
    
    return: List of (name, function) pairs
    """
    return [(name,func) \
            for name, func in module.__dict__.iteritems() \
            if inspect.isfunction(func) and name[0] != '_']

if __name__ == "__main__":    
    boys, girls = load_international_names()    
    all_functions = all_functions_from_module(features)

    func_name, func = all_functions[0]
    girl_feats = map(func, girls)
    boy_feats = map(func, boys)
            
    def frac_counts(features):
        counts = Counter([x['vowel_decile'] for x in features])
        heights = np.array([1.0*counts.get(i,0) for i in range(11)])
        heights /= len(features)
        return heights

    x_axis = np.linspace(0, 10, 11)
    heights = frac_counts(girl_feats)
    plt.bar(x_axis, heights, width = 0.3, label='Girls')
    x_axis = x_axis + 0.3
    heights = frac_counts(boy_feats)
    plt.bar(x_axis, heights, width = 0.3, label='Boys', color='g')
    plt.legend()
    
    plt.title('{} vowel deciles'.format(func_name))
    