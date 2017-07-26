# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:17:51 2017

@author: xma
"""
import numpy as np

def battle_results(attacker, defender):
    pass

    return #winner & HP left & #rounds it took 

def find_best_move(attacker, defender):
    bestsum = attacker.attack[0]
    for m in attacker.get_moves():
        sum_damage = 0
        for i in range(100):
            sum_damage += damage(m, attacker, defender)
        if sum_damage > bestsum:
            bestsum = sum_damage
            bestmove = m    
    return bestmove

def damage(move, attacker, defender):
    return move*np.random.rand()   

class FakePokemon():
    
    def get_moves(self):
        return [1,2,3,4]

def find_the_winner(attacker, defender):
    #sum_hp -= original_hp 
    pass



if __name__ == "__main__":
   
    attacker = FakePokemon()
    find_best_move(FakePokemon(), FakePokemon())

#    moves = [1, 2, 3, 4]
#    
#    bestmove = moves[0]
#    bestsum = -10
#    for m in moves:
#        temp = 0
#        for i in range(100):
#            temp += damage(m, None, None)
#        if temp > bestsum:
#            bestsum = temp
#            bestmove = m    
#    print bestmove
#    print bestsum       
