# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 17:41:59 2017

@author: jzuber
"""
import pandas as pd


def cube(x):
    return x**3    
    
if __name__ == "__main__":
    # A few things I didn't go over.
    # An easy way to make a list, called list comprehension    
    squares = [x*x for x in range(10)]
    print squares
               
    # The map function applies the first argument(a function) 
    # to every element in the second argument (an iterable item)
    map_cubes = map(cube, range(10))
    print map_cubes
    
    # See how simple the function cube() was?  
    # This is frequently when people write what are called
    # lambda functions: simple functions small enough to be 
    # written inline
    map_lambda_cubes = map(lambda x: x**3, range(10))
    print map_lambda_cubes
    
    # Don't do the following, it's ugly. UGLY
    cube_lambda = lambda x: x**3
    print cube_lambda(4)
    
    # Now for one of my favorites, zip!
    # Zip combines two lists into a list of tuples, where 
    # each tuple has one element from the left list comma same element
    # from right list
    zip_list = zip(['a', 'b', 'c'], [1, 2, 3])
    print zip_list
    
    # And finally, we can make dictionaries out of zipped lists
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    simple_dict = dict(zip(keys, values))
    print simple_dict
    
    # You can do this in one line, but be careful not to 
    # do too many things in a single line of code.
    # It's ugly and gets confusing.  
    # That and THOU SHALT NOT PASS COLUMN 80
    one_line_dict = dict(zip(['a', 'b', 'c'], [1, 2, 3]))
    print one_line_dict
    
    # dataframes can be made from dictionaries
    df = pd.DataFrame({'a': range(10), 'b':2})
    print df.head()
    