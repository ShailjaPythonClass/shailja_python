# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 14:33:43 2017
Attack damage formula (Pokemon)
@author: shezhang
"""
"""
From: https://www.math.miami.edu/~jam/azure/compendium/battdam.htm

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

from random import randint, seed

from pokemon import Pokemon

def dave_call(move, defender):
    return 1

def damage_done(move, attacker, defender, random_seed=None):
   
    if random_seed:
        seed(random_seed)
        
    attack_type = move.type.values
    attack_power = move.power.values
    accuracy = move.accuracy.values
    multiplier = dave_call(move, defender)

    #same-type attack bonus (1 or 1.5)
    def stab():                   
        if attack_type == attacker.type_1 or attack_type == attacker.type_2:
            stab = 1.5
        else:
            stab = 1
        return stab
    
    a_attacker_level = attacker.level #attacker's Level 
    b_attack = attacker.typed_attack(attack_type)
    c_attack_power = attack_power
    d_defense = defender.typed_defense(attack_type)
              
    def does_attack_hit():
        return 1 * (randint(1,100) <= accuracy)

    def critical_hit():
        # TODO https://bulbapedia.bulbagarden.net/wiki/Critical_hit
        return randint(1, 16) == 1
    
    if critical_hit():
        a_attacker_level *= 2
    
    z = randint(217,255) / float(255) # a random number between 217 and 255
    
    damage = 2 
    damage += (2 * a_attacker_level) / float(5) 
    damage *= b_attack * c_attack_power  
    damage /= float(d_defense)
    damage = 2 + damage / float(50)
    damage *= stab() * multiplier / float(10)
    damage *= z
    damage *= does_attack_hit()

    return damage


if __name__ == '__main__':
    
    move = gimme_move_akshay('Thunderbolt')
    attacker = Pokemon('Pikachu', 20)
    defender = Pokemon('Squirtle', 25)    
    
    dmg = damage_done(move, attacker, defender, random_seed=0)
    assert dmg == 10, "Weird damage ({}) returned!".format(dmg)
    
"""
 damage_done("Attack", "Pikachu", "Bulbasaur")

"""    
    
    
    












    


    


    







