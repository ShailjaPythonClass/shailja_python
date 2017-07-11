# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 14:33:43 2017
Attack damage formula (Pokemon)
@author: shezhang
"""
"""
((2A/5+2)*B*C)/D)/50)+2)*X)*Y/10)*Z)/255

A = attacker's Level
B = attacker's Attack or Special
C = attack Power
D = defender's Defense or Special
X = same-Type attack bonus (1 or 1.5)
Y = Type modifiers (40, 20, 10, 5, 2.5, or 0)
Z = a random number between 217 and 255

"""

from collections import namedtuple
from random import randint

pokemon = namedtuple('pokemon', ['attack', 'special_attack', 'defense',
                                'special_defense', 'level', 
                                'type_1', 'type_2'])

#charmander = pokemon(10,11,5,13, 40,'Fire', None)  #attacker
#Squirtle = pokemon(12,9,6,12,39,'Water', None) #defender

#Deleted target_pokemon


def damage_done(attack_type, 
                attacker, defender):

    def critical_hit():
        return 1  # This is not finished yet...    
    
    def b_attack_function(attack_type):
        if attack_type == "Attack": # physical attack
           return attacker.attack
        elif attack_type == "Special": # special attack
           return attacker.special_attack
        else:
           return "Error: wrong attack type; enter either 'Attack' or 'Special'!"
    
    def c_attack_power():
        return 60      # This is not finished yet...
        
    def d_defense_function(attack_type):
        if attack_type == "Attack": # physical attack
           return defender.defense
        elif attack_type == "Special": # special attack
           return defender.special_defense
        else:
           return "Error: wrong attack type; enter either Attack or Special!"
           
    def x_STAB(): #same-type attack bonus (1 or 1.5)
        return 1 #This is not finished yet...
        
    def y_type_modifiers(): # Type modifiers (40,20,10,5,2.5, or 0)
        return 10 # Not finished yet...

    
    a_attacker_level = attacker.level #attacker's Level 
       
    z = randint(217,255) # a random number between 217 and 255
    
    damage = 0 
    damage += (2*a_attacker_level)/5+2
    damage *= b_attack_function(attack_type)*c_attack_power()  
    damage /= d_defense_function(attack_type)
    damage = damage/50+2
    damage *= x_STAB()*y_type_modifiers()/10
    damage *= z/255
               
    return damage


















    


    


    







