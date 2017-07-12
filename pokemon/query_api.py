# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 14:33:04 2017

@author: apsingh
"""

import requests
import pandas as pd
import numpy as np

def pull_all_versions():
    version_dict = {}
    for version in np.arange(16)+1:
        url = 'http://pokeapi.co/api/v2/version-group/{}'.format(version)
        res = requests.get(url).json()
        version_dict.update({res['name']: version})

    return version_dict

    
def extract_moves(pokemon, moves, game_version, version_dict):
    selected_moves = []
    for move in moves:
        for group in move['version_group_details']:
            if ((group['move_learn_method']['name'] == 'level-up') &
               (version_dict[group['version_group']['name']] == game_version)):
                selected_moves.append((pokemon,
                                      move['move']['name'],
                                      group['level_learned_at']))
    return selected_moves


def get_pokemon_abilities(pokemons=['all'], game_version=16):
    versions = pull_all_versions()
    pokemon_moves = []
    if pokemons[0].lower() != 'all':
        for pokemon in pokemons:
            url = 'http://pokeapi.co/api/v2/pokemon/{}'.format(pokemon)
            res = requests.get(url).json()
            pokemon_moves.extend(extract_moves(res['name'],
                                               res['moves'],
                                               game_version,
                                               versions))
    else:
        df = pd.read_csv('./data/pokemon_alopez247.csv')
        for name in df.Name.values:
            url = 'http://pokeapi.co/api/v2/pokemon/{}'.format(name)
            res = requests.get(url).json()
            pokemon_moves.extend(extract_moves(res['name'],
                                               res['moves'],
                                               game_version,
                                               versions))
    return pokemon_moves

def pull_all_moves():
    moves = []
    keys = ['name', 'power', 'accuracy', 'pp', 'target', 'type', 'damage_class',
            'priority', 's']
    
    for move in np.arange(719)+1:
        url = 'http://pokeapi.co/api/v2/move/{}'.format(move)
        res = requests.get(url).json()

if __name__ == '__main__':
    #res = requests.get('http://pokeapi.co/api/v2/pokemon/ivysaur').json()
    pokemons = ['ivysaur', 'bulbasaur']
    abilities = get_pokemon_abilities(pokemons)