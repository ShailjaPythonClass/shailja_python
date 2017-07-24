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

from collections import namedtuple
"""

from random import randint


def damage_done(attack_type,  attack_power, multiplier, accuracy,
                attacker, defender):
   
    
    def critical_hit():
        return 1  # This is not finished yet...    
           
    #same-type attack bonus (1 or 1.5)
    def stab(attack_type, attacker):   
        
        stab = 1
        if attack_type == attacker.type_1 or attack_type == attacker.type_2:
            stab = 1.5
        
        return stab
    
    a_attacker_level = attacker.level #attacker's Level 
    b_attack = attacker.attack(attack_type)
    c_attack_power = attack_power
    d_defense = defender.defense(attack_type)
        

    
    def attack_accuracy(accuracy):
        num = randint(1,100) # includes 1 and 100
        attack_success = 0 # 0 means missed, 1 means success
        
        if num <= accuracy:
            attack_success = 1
                
        return attack_success
    
    z = randint(217,255) # a random number between 217 and 255
    
    damage = 0 
    damage += (2*a_attacker_level)/5+2
    damage *= b_attack*c_attack_power  
    damage /= d_defense
    damage = damage/50+2
    damage *= stab()*multiplier/10
    damage *= z/255
    damage *= attack_accuracy()
           
    return damage



if __name__ == '__main__':
          
    damage_done()
    
"""
 damage_done("Attack", "Pikachu", "Bulbasaur")

"""    
    
    
    












    


    


    







