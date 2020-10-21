#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import random
import time

def clear_screen():
    os.system('clear')  # clears the screen


def print_menu():
    ''' The first screen the user sees when opening the game'''

    clear_screen()
    print("\n\n")
    print("Welcome to Mylla — a Tic Tac Toe game")
    print("\n")
    print_grid([" o ", "   ", " x ", "   ", " o ", "   ", "   ", "   ", " o "])
    print("\n")

def set_up_game():
    ''' Asks the player how the game should be set up, and returns a tuple (x,y),
    where x = Player 1 and y Player 2. Choices are Human (1) or AI (2)'''
    
    user_choice = ("1", "2") # default choice is Human vs. AI. The game logic 
                             # should never default to it, but it is here.

    print("Please select Player 1:\n")
    print("1: Human")
    print("2: AI\n")
 
    x = get_choice("Player 1:", [1,2])
    y = get_choice("Player 2:", [1,2])

    return (x, y)

def get_choice(prompt, acceptable_range):
    ''' Gets and validates input from the player. Takes a string to print at 
        the input prompt. q is always allowed.'''
        
    choice = ""
    within_range = False
    
    while (choice.isdigit() == False or within_range == False) and choice != 'q':

        choice = input(prompt)
        
        if choice.isdigit() == False and choice != 'q':
            print(f"\'{choice}\' is not valid option. Please try again.")
        
        if choice.isdigit() == True:
            if int(choice) in acceptable_range:
                    within_range = True
            else:
                print(f"\'{choice}\' is out of range. Please try again.")

    return choice

def display_grid(state):
    ''' Displays the grid. It takes in a list of 9 elements, each corresponding to 
    a square and displays it. The list must be 9 elements and only contain "x", 
    "o" or "". ''' 
    
    if len(state) != 9:
        print("Error: Something went wrong.")

        return False
    
    if any(element not in set('xo ') for element in "".join(state)): #checks if o, x or empty string 
        print("Error: State has unknown elements.")                  #are in the state
        
        return False
    
    for index, element in enumerate(state): #pads out the state for printing, so it aligns.
        if element == "":
            state[index] = "   "
        else:
            state[index] = " " + element.strip() + " "

    clear_screen()

    print("The current grid is: ")
    print_grid(state) #print grid. Could probably be simplified, but it works

    strip_state(state) #just to clean things up

    return True #if nothing went wrong, we return True.

def print_grid(state):
    print("+" + "-"*3 + "+" + "-"*3 + "+" + "-"*3 + "+")
    print("|" + state[0] + "|" + state[1] + "|" + state[2] + "|")
    print("+" + "-"*3 + "+" + "-"*3 + "+" + "-"*3 + "+")
    print("|" + state[3] + "|" + state[4] + "|" + state[5] + "|")
    print("+" + "-"*3 + "+" + "-"*3 + "+" + "-"*3 + "+")
    print("|" + state[6] + "|" + state[7] + "|" + state[8] + "|")
    print("+" + "-"*3 + "+" + "-"*3 + "+" + "-"*3 + "+")

    return True

def strip_state(state):
    ''' Auxilliary function that keeps the state clean between functions. 
    It strips away all spaces.''' 

    for index, element in enumerate(state):
        state[index] = element.replace(" ", "")

    return state

def update_state(state, square, player):
    ''' Takes in a state, a square to update and a Boolean that indicates the
    current player, True for Player 1 and False for Player 2 '''

    if player == True:
        symbol = "x"
    else: 
        symbol = "o"

    state[square] = symbol

    return strip_state(state)

def check_victory(state):
    ''' checks if the game has been won. Currently just checks every possibility by brute force'''

    if state[0] == 'x' and state[1] == 'x' and state[2] == 'x':
        return True
    elif state[3] == 'x' and state[4] == 'x' and state[5] == 'x':
        return True
    elif state[6] == 'x' and state[7] == 'x' and state[8] == 'x':
        return True
    elif state[0] == 'x' and state[4] == 'x' and state[8] == 'x':
        return True
    elif state[0] == 'x' and state[3] == 'x' and state[6] == 'x':
        return True
    elif state[1] == 'x' and state[4] == 'x' and state[7] == 'x':
        return True
    elif state[2] == 'x' and state[5] == 'x' and state[8] == 'x':
        return True
    elif state[0] == 'o' and state[1] == 'o' and state[2] == 'o':
        return True
    elif state[3] == 'o' and state[4] == 'o' and state[5] == 'o':
        return True
    elif state[6] == 'o' and state[7] == 'o' and state[8] == 'o':
        return True
    elif state[0] == 'o' and state[4] == 'o' and state[8] == 'o':
        return True
    elif state[0] == 'o' and state[3] == 'o' and state[6] == 'o':
        return True
    elif state[1] == 'o' and state[4] == 'o' and state[7] == 'o':
        return True
    elif state[2] == 'o' and state[5] == 'o' and state[8] == 'o':
        return True
    else: 
        return False
    
def check_human(user_menu_choice, player_one_turn):
    ''' checks if the current player is Human or AI. get the menu choice and
    boolen telling if current player is player one'''

    if player_one_turn == True and user_menu_choice[0] == '1': #p1 turn and p1 is human
        return True
    elif player_one_turn == True and user_menu_choice[0] == '2': #p1 turn and p1 is A
        return False
    elif player_one_turn == False and user_menu_choice[1] == '1':
        return True
    elif player_one_turn == False and user_menu_choice[1] == '2':
        return False
    else:
        return True #default assumption that the player is human
    
    return True #if everything went wrong, we again assume humanity

def AI_move(state):
    ''' function to get a move from the AI. At the moment, it is very unsophisticated and only picks a
    move at random. Takes in the state of play and returns a move.'''

    possible_moves = list(range(1,10)) #it can pick any number from 0-9 before we cull the moves.
    state = strip_state(state)

    for index, square in enumerate(state):
        if square == 'x' or square == 'o':
            possible_moves.remove(index+1)
    
    move = random.choice(possible_moves)

    return str(move) #returns a string because elsewhere the input from a player is string.

#game logic goes here

state = ["", "", "", "", "", "", "", "", ""] #game starts with an empty grid

print_menu()
user_menu_choice = set_up_game()

player_one = user_menu_choice[0] #1 = Human, 2 = AI
player_two = user_menu_choice[1]

game_won = False
current_player = "1"
player_one_turn = True #Just to turn the player into a boolean, if False, then P2
square = ''

display_grid(state) # A bit of a hack, fix later

while square != 'q':

    if check_human(user_menu_choice, player_one_turn) == True:
        square = get_choice("Make a move by selecting a square (1-9):", range(1,10))
    else:
        square = AI_move(state) # let the AI move.
        time.sleep(1)

    if square == 'q':
        break

    if square.isdigit() == True:
        square = int(square) #casting to an int 
        square -= 1 #The player enters an number between 1-9, the list has indeces 0-8
 
    if state[square] != "":
        print("That square is already full. Try again.")
        continue

    state = update_state(state, square, player_one_turn)
    game_won = check_victory(state)

    if player_one_turn == True:
        current_player = "1"
    else: 
        current_player = "2"

    if game_won == True:
        display_grid(state)
        print(f"Player {current_player} won!")
        break

    if game_won == False and "" not in state:
        display_grid(state)
        print(f"Draw!")
        break

    player_one_turn =  not player_one_turn #swaps the players
    display_grid(state)