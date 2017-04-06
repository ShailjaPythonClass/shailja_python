# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 12:36:41 2017

@author: jzuber
"""

import pandas as pd
import matplotlib.pyplot as plt
   
    
def sample_function():
    """ 
    This is my docstring
    """
    pass

if __name__ == "__main__":
    print "hello world"
    filename = "../sample_data/test_data.csv"    
    
    # How to open a file for raw text reading
    with open(filename, 'r') as infile:
        for line in infile:
            print line
    
    # Open a CSV into a pandas dataframe
    df = pd.read_csv(filename)
    
    # Groupby operations on dataframes
    averages = df.groupby('category').mean()
        
    # Plotting some bars
    x_axis = range(5)
    
    # Make bar plots
    colors = iter(['r', 'g', 'b', 'y'])
    categories_used = []
    for i, row in averages.iterrows():        
        heights = row.tolist()
        f = plt.bar(x_axis, heights, width = 0.1, color=colors.next())
        x_axis = [x + 0.1 for x in x_axis]
        categories_used.append((i, f))
    plt.title("Volume for All Categories".format(i))
        
    
