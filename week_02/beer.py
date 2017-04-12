# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:37:45 2017

@author: jzuber
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

if __name__ == "__main__":
    beers = pd.read_csv('../sample_data/beers.csv')    
    breweries = pd.read_csv('../sample_data/breweries.csv')
    del beers['ibu']
    del beers['Unnamed: 0']
    beers.rename(columns={'name': 'beer'}, inplace=True)
    breweries.columns = ['id'] + list(breweries.columns[1:])
    breweries.rename(columns={'Unnamed: 0':'brewery_id',
                              'name': 'brewery'}, inplace=True)
    del breweries['city']
    del breweries['state']
        
    merged = pd.merge(beers, breweries, on='id')
    merged.head()
    merged = merged.dropna()
    
    merged.groupby('style').mean()['abv'].sort_values()
        
    num_varieties = len(set(merged['style']))
    cmap = plt.cm.viridis(np.linspace(0, 1, num_varieties))
    frequency = merged.groupby('style').count()['abv'].sort_values()
    names = map(lambda x: x.decode('utf-8'), frequency.index)
    plt.pie(frequency, labels=names, colors=cmap)    
    plt.show()
    
    n_popular = num_varieties / 10
    cmap = plt.cm.viridis(np.linspace(0.25, 1, n_popular))
    cutoff = min(frequency[-n_popular:])
    frequency = frequency[-n_popular:]
    names = map(lambda x: x.decode('utf-8'), frequency.index)
    plt.pie(frequency, 
            labels=names, 
            colors=cmap, 
            autopct='%1.1f%%',
            explode = [0.05 for _ in frequency],
            shadow=True)
    plt.show()
        
    plt.figure()
    cmap = plt.cm.viridis(np.linspace(0, 1, n_popular))
    for style, color in zip(names, cmap):        
        sub = merged[merged['style'] == style]
        num_beers = sub['abv'].count()
        avg_proof = sub['abv'].mean()
        plt.scatter(num_beers, avg_proof, 
                    label=style.decode('utf-8'),
                    c=color)
    plt.xlabel('num_beers')
    plt.ylabel('abv')
    plt.legend(loc='best')
    plt.title('Alcohol content by in popular varities')
    plt.show()
    
    plt.figure()
    cmap = plt.cm.viridis(np.linspace(0, 1, num_varieties))
        
    num_beers = merged.groupby('style').count()['abv']
    avg_proof = merged.groupby('style').mean()['abv']
    plt.scatter(num_beers, avg_proof, c=np.linspace(0, 1, len(num_beers)))
    plt.xlabel('num_beers')
    plt.ylabel('abv')    
    plt.title('Alcohol content in all varities')
    plt.show()