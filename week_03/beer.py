# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:37:45 2017

@author: jzuber
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def safe_colors(num, start=0, end=1):
    """
    Color selection function to overcome compatability issues.
    """
    vect = np.linspace(start, end, num)
    try:
        return plt.cm.viridis(vect)
    except AttributeError:
        return vect

def get_clean_data():
    """
    Returns two dataframes:
        beers: A frame representing beers and their attributes.
        breweries: A frame containing breweries and their locations
    """
    beers = pd.read_csv('../sample_data/beers.csv')    
    breweries = pd.read_csv('../sample_data/breweries.csv')    
    del beers['Unnamed: 0']
    beers.rename(columns={'name': 'beer'}, inplace=True)    
    breweries.rename(columns={'Unnamed: 0':'brewery_id',
                              'name': 'brewery'}, inplace=True)                
    return beers, breweries
        
if __name__ == "__main__":
    beers, breweries = get_clean_data()
    
    merged = pd.merge(beers, breweries, on='brewery_id')
    merged.head()
    merged = merged.dropna()        
    
    # Scatter plot of ABV vs state (sorted alphabetically)
    means = merged.groupby(['style', 'state'], as_index=False).mean().copy()
    states = {s:i for i, s in enumerate(np.unique(merged['state']))}
    plt.scatter(map(lambda i: states[i], means['state']), means.abv)

    # State has extra whitespace    
    merged['state'] = map(lambda x: str(x).strip(), merged['state'])
    data = {state:list(merged[merged['state'] == state]['abv'])
            for state in set(merged['state']) if state < 'I'}
    sorted_data = [data[state] for state in set(data.keys())]
    fig, ax = plt.subplots(figsize=[20,4])    
    
    x_axis = np.linspace(0, 1, len(data))    
    delta_x = x_axis[1] - x_axis[0]
    for x, dat in zip(x_axis, sorted_data):
        jitter = 0.5*delta_x*(np.random.rand(len(dat)) - 0.5)
        ax.scatter(x + jitter, dat, c=[0.8]*len(dat))
    #ax.violinplot(sorted_data, x_axis)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(sorted(data.keys()))
    fig.show()
    