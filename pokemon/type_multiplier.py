# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 16:35:58 2017

@author: dgoodchild
"""

import numpy as np
import pandas as pd

def type_multiplier(attack_type, target_pokemon): 
    """
    Returns type multiplier for attack against a given pokemon
    
    attack_type: string, type of elemental attack
    target_pokemon: string, name of pokemon being attacked
    
    """
    ## lazy load data
    try: 
        pokestats = type_multiplier.pokestats
        attack_matrix = type_multiplier.attack_matrix
    except AttributeError:
        type_multiplier.pokestats = pd.read_csv('./data/pokemon_alopez247.csv')
        type_multiplier.attack_matrix = pd.read_csv('./data/poke-type.csv')
        type_multiplier.attack_matrix.set_index("Attacking", inplace=True)
        pokestats = type_multiplier.pokestats
        attack_matrix = type_multiplier.attack_matrix
        
    ## fix arguments 
    attack_type = attack_type.title()
    target_pokemon = target_pokemon.title()
    pk_stats = pokestats[pokestats.Name == target_pokemon].squeeze()
    multiplier = 10
    types = [pk_stats['Type_1'], pk_stats['Type_2']]    
    for target_type in types:
        if target_type is not np.nan:        
            multiplier *= attack_matrix[target_type][attack_type]
    return multiplier

if __name__ == "__main__":
    assert type_multiplier("Fire", "Bulbasaur") == 20, "Test1"
    
    assert type_multiplier("fIRe", "buLBAsaur") == 20, "CaseTest"
    
    assert type_multiplier("rOCK", "butterFREE") == 40, "CaseTest2"
    
    assert type_multiplier("grASS", "metapod") == 5, "HalfTest"
    
    assert type_multiplier("ghost", "pidgey") == 0.0, "HalfTest2"
    
    assert type_multiplier("fairy", "charmander") == 5, "OneType"