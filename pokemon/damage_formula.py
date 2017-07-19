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
import type_multiplier 


def damage_done(attack_type, multiplier, attack_power, 
                attacker, defender):
   
    
    def critical_hit():
        return 1  # This is not finished yet...    
           
    #same-type attack bonus (1 or 1.5)
    def stab():       
        if attack_type == attacker.type_1 or attack_type == attacker.type_2:
            stab = 1.5
        else:
            stab = 1
        return stab
    
    a_attacker_level = attacker.level #attacker's Level 
    b_attack = attacker.attack(attack_type)
    c_attack_power = attack_power
    d_defense = defender.defense(attack_type)
        
    z = randint(217,255) # a random number between 217 and 255
    
    damage = 0 
    damage += (2*a_attacker_level)/5+2
    damage *= b_attack*c_attack_power()  
    damage /= d_defense
    damage = damage/50+2
    damage *= stab()*multiplier/10
    damage *= z/255
               
    return damage



if __name__ == '__main__':
    
    attack
    
    damage_done(attack_type, multiplier, attack_power, 
                attacker, defender)
    
"""
 damage_done("Attack", "Pikachu", "Bulbasaur")

"""    
    
    
    















    


    


    







