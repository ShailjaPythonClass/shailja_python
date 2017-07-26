# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:26:52 2017

@author: shezhang
"""
from query_api import get_pokemon_moves


def _stat_formula(base, level, is_hp=False, ev=None):
    if not ev:
        ev = min(73, level)             
    retval = int((2*base + 15 + ev/4) * level / 100) + level
    if is_hp:
        return retval + 10
    else:
        return retval + 5
            
class Pokemon:
               
    def __init__(self, name, level, current_hp=None):
        self.name = name
        self.level = level
        base_stats = func_call_that_akshay_has_to_write(name)
        self.max_hp = _stat_formula(base_stats.hp, is_hp=True)
        self.current_hp = self.max_hp
        if current_hp:
            self.current_hp = current_hp
        self.attack = _stat_formula(base_stats.attack)
        self.special_attack = _stat_formula(base_stats.special_attack)
        self.defense = _stat_formula(base_stats.defense)
        self.special_defense = _stat_formula(base_stats.special_defense)
        self.type_1 = _stat_formula(base_stats.type_1)
        self.type_2 = _stat_formula(base_stats.type_2)
        self.movelist = self.choose_moves(get_pokemon_moves(self.name, self.level))
        
        
    def attack(self, attack_type):
        if attack_type == "Physical":
            return self.attack
        else:
            return self.special_attack
        
    def defense(self, attack_type):
        if attack_type == "Physical":
            return self.defense
        else:
            return self.special_defense
            
    def choose_moves(self, move_list):
        pass
        
    
    #In [3]: test_dict
    #Out[3]: {'a': 1, 'b': 2, 'c': 3}
    #
    #test_dict['a']
    #Out[4]: 1
    #
    #test_dict.keys()
    #Out[5]: dict_keys(['c', 'b', 'a'])
    #
    #test_dict.values()
    #Out[6]: dict_values([3, 2, 1])