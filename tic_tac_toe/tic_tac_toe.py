# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 14:05:34 2017

@author: jzuber
"""

def print_board(board):
    for i, row in enumerate(board):
        print("|".join(row))
        if i < 2:
            print("------")

def all_match(a,b,c):
    if a==b and b==c:
        return True

def row_checker(board):
    for row in board:
        if all_match(*row):
            winning_character = row[0]
            if winning_character in ['x', 'o']:                
                return winning_character
    return False
    
def column_checker(board):
    transpose = []
    for i in range(3):
        column = [board[0][i], board[1][i], board[2][i]]
        transpose.append(column)
    return row_checker(transpose)

def diag_checker(board):
    left_diag = [board[i][i] for i in range(3)]
    right_diag = [board[i][2-i] for i in range(3)]
    blank = ['', '', '']
    return row_checker([left_diag, right_diag, blank])
        
def winner_check(board):
    col_winner = column_checker(board)
    row_winner = row_checker(board)
    diag_winner = diag_checker(board)
    for char in [col_winner, row_winner, diag_winner]:
        if char is not False:
            return char
    return False

if __name__ == "__main__":
    x_wins = [['x', 'x', 'x'],             
              [' ', ' ', ' '],
              ['o', ' ', 'x']]
    
    o_wins = [['o', 'x', 'x'],             
              ['o', ' ', ' '],
              ['o', ' ', 'x']]
    
    diag_wins = [['o', 'x', 'x'],             
                 ['x', 'o', ' '],
                 ['o', ' ', 'o']]
    
    for i, board in enumerate([x_wins, o_wins, diag_wins]):        
        print(winner_check(board))
        
    
    
    
    
    
    
    
    