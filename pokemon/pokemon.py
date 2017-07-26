# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:26:52 2017

@author: shezhang
"""


class Pokemon:
    
    def __init__(self, attack, special_attack, defense, special_defense, level,
                 type_1, type_2):
        self.attack = attack
        self.special_attack = special_attack
        self.defense = defense
        self.special_defense = special_defense
        self.level = level
        self.type_1 = type_1
        self.type_2 = type_2
             
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


"""        
pikachu = Pokemon(10,20, 30,30,40,"Electric",None)
pikachu.attack 

""" 


