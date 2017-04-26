# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:09:48 2017

@author: jzuber
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

if __name__ == "__main__":
    # You'll use lists all of the time, they are really easy to construct
    simple_list = [0,1,2,3,4]
    print(simple_list)
    print(type(simple_list))
    
    simple_list[2] = 15
    print(simple_list)
    print(type(simple_list))
    
    # Tuples are like lists, but you can't change their contents
    simple_tuple = tuple(['a', 'b', 'c', 'd', 'e'])
    print simple_tuple    
    simple_tuple[2] = 5 # Fails, since tuples cannot be written
    
    # Dictionaries let you index a list by something other than indices
    test_dict = {'red': 0, 'orange': 1, 'yellow': 2, 'green': 3, 
                 'blue': 4, 'indigo': 5, 'violet': 6}
    print(test_dict['red'])
    print test_dict.keys()
    print test_dict.values()
    for k,v in test_dict.iteritems():
        print "{0} is number {1}".format(k,v)
    # Note that they are in no meaningful order.
    
    simple_list = [1,2,3]
    np_array = np.array(simple_list)
    
    print "numpy arrays can be treated as vectors", np_array*2
    print "Lists act differently, mult:", simple_list * 2
    print "Lists act differently, add:", [1, 3, 5] + [2]
    print "Lists act differently, subtraction:", [1, 3, 5] - [3]
    print "mixed adding will convert list to np array", simple_list + np_array

    print range(5)
    print type(range(5))
    print np.linspace(0, 5, 21)
    print type(np.linspace(0, 5, 21))
    
    # Dataframes can be constructed from a dictionary
    df = pd.DataFrame({'a':np.linspace(0, 3, 50), 'b':2})
    print df
        
    # and their columns can be treated as numpy arrays    
    print df.a + df.b
    
    # The columns can be modified
    df['b'] += 0.01
    
    # Additional columns can be added
    df['c'] = np.sin(df['a'] * np.pi)
    plt.plot(df.a, df.c)

    # zip dict is a great way to make a dataframe
    print zip(['a', 'b'], [range(5), 2])
    print dict(zip(['a', 'b'], [range(5), 2]))
    print pd.DataFrame(dict(zip(['a', 'b'], [range(5), 2])))
    
    x = np.linspace(0, 3*np.pi, 40)
    plt.plot(x, np.sin(x))
    
    print isinstance(range(5), list)
    print isinstance(range(5), np.ndarray)
    
    print isinstance(df['a'], pd.core.series.Series)
    print isinstance(df['a'], np.ndarray)
    
