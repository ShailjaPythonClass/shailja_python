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

if __name__ == "__main__":
    beers = pd.read_csv('../sample_data/beers.csv')    
    breweries = pd.read_csv('../sample_data/breweries.csv')
    del beers['ibu']
    del beers['Unnamed: 0']
    beers.rename(columns={'name': 'beer'}, inplace=True)
    breweries.columns = ['id'] + list(breweries.columns[1:])
    breweries.rename(columns={'id':'brewery_id',
                              'name': 'brewery'}, inplace=True)
    del breweries['city']
    del breweries['state']
        
    merged = pd.merge(beers, breweries, on='brewery_id')
    merged.head()
    merged = merged.dropna()
    
    abv = merged.groupby('style').mean()['abv'].copy()
    abv.sort()
    print abv
        
    num_varieties = len(set(merged['style']))
    cmap = safe_colors(num_varieties)
    frequency = merged.groupby('style').count()['abv'].copy()
    frequency.sort()
    names = map(lambda x: x.decode('utf-8'), frequency.index)
    plt.pie(frequency, labels=names, colors=cmap)    
    plt.show()
    
    n_popular = num_varieties / 10    
    cmap = safe_colors(n_popular, 0.25, 1)
    cutoff = min(frequency[-n_popular:])
    frequency = frequency[-n_popular:]
    names = map(lambda x: x.decode('utf-8'), frequency.index)
    plt.pie(frequency, 
            labels=names, colors=cmap, 
            autopct='%1.1f%%',
            explode = [0.05 for _ in frequency],
            shadow=True)
    plt.show()
        
    plt.figure()
    try:
        cmap = safe_colors(n_popular, start=0.25)
    except:
        cmap = np.linspace(0,1,n_popular)
    for style, color in zip(names, cmap):        
        sub = merged[merged['style'] == style]
        num_beers = sub['abv'].count()
        avg_proof = sub['abv'].mean()
        plt.scatter(num_beers, avg_proof, 
                    label=style.decode('utf-8'), c=color)
    plt.xlabel('num_beers')
    plt.ylabel('abv')    
    plt.title('Alcohol content by in popular varities')
    plt.show()
    
    plt.figure()
    cmap = safe_colors(num_varieties)        
    num_beers = merged.groupby('style').count()['abv']
    avg_proof = merged.groupby('style').mean()['abv']
    plt.scatter(num_beers, avg_proof, c=cmap)
    plt.xlabel('num_beers')
    plt.ylabel('abv')    
    plt.title('Alcohol content in all varities')
    plt.show()