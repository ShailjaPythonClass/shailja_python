# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 14:07:54 2017

@author: jzuber
"""

from tic_tac_toe import winner_check

def deep_copy(board):
    new_board = []
    for row in range(3):
        temp_row = []
        for col in range(3):
            temp_row.append(board[row][col])
        new_board.append(temp_row)
    return new_board

def pick_winning_move(board, my_char):
    
    winner = winner_check(board)
    if winner is not False:
        return "{} already won".format(winner)    

    for i in range(3):
        for j in range(3): 
            if board[i][j] == ' ':
                test_board = deep_copy(board)
                test_board[i][j] = my_char
                if winner_check(test_board) == my_char:
                    return my_char, i, j
    return False

if __name__ == "__main__":
    x_wins = [['x', 'x', 'x'],             
              [' ', ' ', ' '],
              ['o', ' ', 'x']]
    
    x_can_win = [[' ', 'x', 'x'],             
                 [' ', ' ', ' '],
                 ['o', ' ', 'x']]
    
    either_can_win = [['x', 'o', ' '],             
                 [' ', 'x', ' '],
                 ['o', 'o', ' ']]
    
    print(pick_winning_move(x_can_win, 'x'))
    print(pick_winning_move(x_can_win, 'o'))
    
    print(pick_winning_move(either_can_win, 'x'))
    print(pick_winning_move(either_can_win, 'o'))
    