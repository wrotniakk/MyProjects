# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 00:55:50 2021

@author: kwwro
"""

'''
Tic Tac Toe game
2 Players chose to place O-es and X-es on a 9-slot board
The first one to manage to allign their symbols vertically, horizontally or 
diagonally wins
'''

### function to display the board:
    
def display_board(board):
    print('       |       |       ')
    print(f'   {board[0]}   |   {board[1]}   |   {board[2]}   ')
    print('       |       |       ')
    print('-------|-------|-------')
    print('       |       |       ')
    print(f'   {board[3]}   |   {board[4]}   |   {board[5]}   ')
    print('       |       |       ')
    print('-------|-------|-------')
    print('       |       |       ')
    print(f'   {board[6]}   |   {board[7]}   |   {board[8]}   ')
    print('       |       |       ')

### function for introduction:

def introduction():
    print("Hey! We're about to dive into an epic game of Tic Tac Toe.")
    print("The slots on the board are numerated as following: \n")
    print(" 1 | 2 | 3 \n---|---|---\n 4 | 5 | 6 \n---|---|---\n 7 | 8 | 9 ")
    print("Aight, now that that's dealt with, let's choose the players:")
    options = ['O','X']
    answers = ['Y','N']
    
    p1_symbol = input('Player 1, choose X or O: ')
    
    while p1_symbol not in options:
        print('\nNot what I asked for :(')
            
        p1_symbol = input('Player 1, choose X or O: ')
            
    if p1_symbol == 'O':
        Player_1[1] = 'O'
        Player_2[1] = 'X'
    else:
        Player_1[1] = 'X'
        Player_2[1] = 'O'
    
    p1_choice= input('Player 1, wanna go first? Y or N: ')
        
    while p1_choice not in answers:
        print('\nNot what I asked for :(')
            
        p1_choice= input('Player 1, wanna go first? Y or N: ')
    
    if p1_choice == 'Y':
        Player_1[2] = 1
        Player_2[2] = 2
    else:
        Player_1[2] = 2
        Player_2[2] = 1
                
    print("Great! Let's begin!")
            
### function for checking victory:
    
def check_victory(board):
    if board[0]==board[1]==board[2]=='O' or board[0]==board[1]==board[2]=='X':
        return True
    elif board[3]==board[4]==board[5]=='O' or board[3]==board[4]==board[5]=='X':
        return True
    elif board[6]==board[7]==board[8]=='O' or board[6]==board[7]==board[8]=='X':
        return True
    
    elif board[0]==board[3]==board[6]=='O' or board[0]==board[3]==board[6]=='X':
        return True
    elif board[1]==board[4]==board[7]=='O' or board[1]==board[4]==board[7]=='X':
        return True
    elif board[2]==board[5]==board[8]=='O' or board[2]==board[5]==board[8]=='X':
        return True
    
    elif board[0]==board[4]==board[8]=='O' or board[6]==board[4]==board[2]=='O':
        return True
    elif board[0]==board[4]==board[8]=='X' or board[6]==board[4]==board[2]=='X':
        return True
    
    else: return False
    
    
### function for inserting:
    
def inserting(board):
    
    if Player_1[2] == 1:
        current_player = Player_1
    else: current_player = Player_2
    
    display_board(board)
    
    while True:
        
        index = input(f'{current_player[0]}, where do want to place your {current_player[1]}: ')
        
        while index.isdigit() == False:
             index = input('Please, enter the valid (number) index: ')
        index = int(index)
        board[index-1] = current_player[1]
        display_board(board)
        
        if check_victory(board):
            break
        
        if current_player == Player_1: current_player = Player_2
        else: current_player = Player_1
        
    return current_player


### function for playing the game:
    
def game_play():

    
    introduction()
    current_player = inserting(board)
    
    print(f"Congratulations, {current_player[0]}! You nailed it!")
    
    play_again = input("Do y'all wanna play again? Y or N: ")
    
    while play_again not in ['Y','N']:
        print('\nInvalid answer...')
        play_again = input("Do y'all wanna play again? Y or N: ")
        
    if play_again == 'Y':
        game_play()
    else:
        print("Thanks for playin then! See ya next time!")
 
    
board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
Player_1 = ['Player 1',0,0]
Player_2 = ['Player 2',0,0]

game_play()



            
            
        
        
        
        
        
        
        
        