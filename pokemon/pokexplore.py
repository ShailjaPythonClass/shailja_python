# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:37:23 2017

@author: jzuber
"""
import requests

import numpy as np
import pandas as pd

if __name__ == "__main__":
    pokestats = pd.read_csv('./data/pokemon_alopez247.csv')
    color_dict = {x[1]:x[0] for x in enumerate(pokestats.Color.unique())}
    type_dict = {x[1]:x[0] for x in enumerate(pokestats.Type_1.unique())}
    
    types = np.array([type_dict[x] for x in pokestats.Type_1])
    colors = np.array([color_dict[x] for x in pokestats.Color])
    
    counts = pokestats.groupby(['Color', 'Type_1']).count()['Number']
    counts = counts.reset_index()
    cols = {'Color':'color', 'Type_1':'type', 'Number':'count'}
    counts.rename(columns=cols, inplace=True)    
    counts.sort_values(by='count', ascending=False, inplace=True)
        
    url = 'http://pokeapi.co/api/v2/pokemon/'
    res = requests.get(url + 'bulbasaur')
    movelist = res.json()['moves']
    
    growth_url = 'http://pokeapi.co/api/v2/growth-rate/'    
    growth_dict = requests.get(growth_url + '1').json()
        
    move_url = 'http://pokeapi.co/api/v2/move/'
    move = requests.get(move_url + '1').json()    
    print move['name'], move['power'], 
    print move['accuracy'], move['priority'],
    print move['type']['name'], move['damage_class']['name']
    
    type_df = pd.read_csv('./data/poke-type.csv')
    