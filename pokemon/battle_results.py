# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:17:51 2017

@author: xma
"""
import numpy as np
from pokemon import Pokemon
from query_api import get_move_stats
from damage_formula import damage_done


def battle_results(pokemon1, pokemon2):
    pokemon1.best_move = find_best_move(pokemon1, pokemon2)
    pokemon2.best_move = find_best_move(pokemon2, pokemon1)
    
    first = pokemon1 if pokemon1.speed > pokemon2.speed else pokemon2
    second = pokemon1 if pokemon1.speed <= pokemon2.speed else pokemon2
    
    hps = np.array([first.current_hp, second.current_hp])
    
    rounds = 0
    while sum(hps <= 0) < 1:
        rounds += 1
        hps[1] -= damage_done(first.best_move, first, second)
        if hps[1] <= 0:
            break
        hps[0] -= damage_done(second.best_move, second, first)
        if hps[0] <= 0:
            break
    first.current_hp, second.current_hp = hps

    if hps[0] <= 0:
        return second, rounds
    else:
        return first, rounds

def find_best_move(attacker, defender):
    bestsum = 0
    for m in attacker.movelist:
        move = get_move_stats(m)
        sum_damage = 0
        for i in range(100):
            sum_damage += damage_done(move, attacker, defender)
        if sum_damage > bestsum:
            bestsum = sum_damage
            bestmove = move    
    return bestmove


def find_the_winner(attacker, defender):
    #sum_hp -= original_hp 
    pass



if __name__ == "__main__":
    p1 = Pokemon('squirtle', 5)
    p2 = Pokemon('charmander', 5)

    winner, rounds = battle_results(p1, p2)
    print('winner: {}, rounds: {}'.format(winner.name, rounds))
