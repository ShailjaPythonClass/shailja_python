# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 14:33:04 2017

@author: apsingh
"""

import requests
import pandas as pd
import numpy as np


def get_pokemon_moves(pokemon, level):

    ability_df, moves = make_datasets()
    pokemon = ability_df[ability_df.pokemon == pokemon.lower()]
    pokemon = pokemon.merge(moves, left_on='move', right_on='name')
    pokemon = pokemon[pokemon.level <= level]
    pokemon.drop(['name', 'pokemon'], axis=1, inplace=True)

    return pokemon.to_dict(orient='record')


def make_datasets(game_version=16):
    df = pd.read_csv('./data/pokemon_alopez247.csv')
    versions = pull_all_versions()

    if type(game_version) == str:
        game_version = versions[game_version]

    try:
        ability_df = pd.read_csv('./data/pokemon_abilities.csv')
    except:
        abilities = get_pokemon_abilities(df[df.Generation == 1].copy(),
                                          game_version)
        ability_df = pd.DataFrame(abilities,
                                  columns=['pokemon', 'move', 'level'])
        ability_df.to_csv('./data/pokemon_abilities.csv', index=False)

    try:
        move_df = pd.read_csv('./data/moves.csv')
    except:
        moves = []
        moves.extend(pull_all_moves(range(622)))
        move_df = create_moves_df(moves)
        move_df.to_csv('./data/moves.csv', index=False)

    return ability_df, move_df


def pull_all_versions():
    try:
        version_dict = dict(pd.read_csv('./data/versions.csv').values)
    except:
        version_dict = {}
        for version in np.arange(16)+1:
            url = 'http://pokeapi.co/api/v2/version-group/{}'.format(version)
            res = requests.get(url).json()
            version_dict.update({res['name']: version})
        version_df = pd.DataFrame.from_dict(version_dict, orient = 'index')
        version_df.reset_index(inplace=True)
        version_df.columns = ['name', 'version']
        version_df.to_csv('./data/versions.csv', index=False)

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


def get_pokemon_abilities(df, game_version=16):
    versions = pull_all_versions()
    pokemon_moves = []

    for num in df.Number.values:
        url = 'http://pokeapi.co/api/v2/pokemon/{}'.format(num)
        res = requests.get(url).json()
        pokemon_moves.extend(extract_moves(res['name'],
                                           res['moves'],
                                           game_version,
                                           versions))
    return pokemon_moves


def pull_all_moves(move_nums=range(622)):
    moves = []
    keys = ['name', 'power', 'accuracy', 'pp', 'target', 'type',
            'damage_class', 'priority']

    for move in move_nums:
        url = 'http://pokeapi.co/api/v2/move/{}'.format(move)
        res = requests.get(url).json()
        try:
            moves.append([res[key] for key in keys])
        except:
            continue
    return moves


def create_moves_df(moves):
    keys = ['name', 'power', 'accuracy', 'pp', 'target', 'type',
            'damage_class', 'priority']
    movedf = pd.DataFrame()
    for move in moves:
        add = {keys[i]: move[i] for i in range(4)}
        add.update({keys[i]: move[i]['name'] for i in range(4, 7)})
        add.update({keys[-1]: move[-1]})
        movedf = movedf.append(add, ignore_index=True)
    return movedf


def get_move_stats(move):
    try:
        move_df = pd.read_csv('./data/moves.csv')
    except:
        moves = []
        moves.extend(pull_all_moves(range(622)))
        move_df = create_moves_df(moves)
        move_df.to_csv('./data/moves.csv', index=False)

    return move_df[move_df.name == move]



if __name__ == '__main__':

    df = pd.read_csv('./data/pokemon_alopez247.csv')
    versions = pull_all_versions()
    abilities = get_pokemon_abilities(df[df.Generation == 1].copy())
    ability_df = pd.DataFrame(abilities, columns=['pokemon', 'move', 'level'])
    
    moves = []
    moves.extend(pull_all_moves(range(622)))
    movedf = create_moves_df(moves)

