# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:26:52 2017

@author: shezhang
"""
from collections import namedtuple
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
    
    _pokestats_df = None
             
    def __init__(self, name, level, current_hp=None):
        if Pokemon._pokestats_df is None:
            _pokestats_df = pd.read_csv('./data/pokemon_alopez247.csv')
            _pokestats_df.Name = _pokestats_df.Name.apply(lambda x: x.lower())
        self.name = name.lower()
        row = _pokestats_df[_pokestats_df.Name == self.name]
        if len(row) == 0:
            throw(KeyError("Pokemon {} Not found.".format(name)))  
        row = row.to_dict(orient='records')[0]
        self.level = int(level)        
        self.max_hp = _stat_formula(row['HP'], level, is_hp=True)
        self.current_hp = self.max_hp
        if current_hp:
            self.current_hp = current_hp
        self.attack = _stat_formula(row['Attack'], level)
        self.special_attack = _stat_formula(row['Sp_Atk'], level)
        self.defense = _stat_formula(row['Defense'], level)
        self.special_defense = _stat_formula(row['Sp_Def'], level)
        self.type_1 = _stat_formula(row['Type_1'], level)
        self.type_2 = _stat_formula(row['Type_2'], level)
        self.movelist = self.choose_moves(get_pokemon_moves(self.name, 
                                                            self.level))
        

    def typed_attack(self, attack_type):

        if attack_type == "Physical":
            return self.attack
        else:
            return self.special_attack
        
    def typed_defense(self, attack_type):
        if attack_type == "Physical":
            return self.defense
        else:
            return self.special_defense
   
    def choose_moves(self, move_list):
        some_list = get_pokemon_moves(self.name, self.level)
        ranks = []
        attack = namedtuple('Attack', 'name power')
        
        for i in range(len(some_list)): 
            flag = False
            for j in range (len(ranks)):
                if some_list[i]['move'] == ranks[j][0]:
                    flag = True
                
            if flag == False:
                if some_list[i]['power'] > 0:
                    ranks.append(attack(some_list[i]['move'],
                            some_list[i]['accuracy']*some_list[i]['power']))
            
        ranks = sorted(ranks, key = lambda x: int(x[1]))
        move_set=[]
        for j in range(4):
            move_set.append(ranks[j*-1][0])
        
        return move_set

if __name__ = "__main__":        
    pikachu = Pokemon("Pikachu", 15)
    pikachu = Pokemon("piKAChU", 13.2)




