# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:24:44 2013

@author: jmcontreras
"""

# TODO:
# Present focus is on developing a miniminally-viable board that can be played
# with a WHILE loop to completion
# With players and properties ready to go, you are read to build a board
# The board will be a dictionary that guides the players through the different
# dictionaries (streets, utilities, railroads, and other positions)
# Rather than having multiple dictionries, I wonder if it is possible to create
# a single one to hold all of the board information
# One option would be to write a csv file with one row per board position, with
# different columns filled in for each property, depending on its type
# Then, the for loop that would bring in this documen would have an if flow
# that would determine which kind of object gets created at that particular
# point
# The weakness of this approach may have to do with performing operations
# across the dictionary (e.g., can you check that a person has all monopolies?)
# If not, should this operatin be done at a player level?
# Maybe player level is no good because when  player dies it takes important
# informtion along with it

# Source other scripts
execfile('players.py')
execfile('dice.py')

# Declarations
n_players = get_players(5) # Number of players

# Start the game
while n_players > 1:
    
    # Take turs
    for turn in range(1, n_players):
        
        # Roll the dice        
        n_move = roll_dice()
        
        # Evaluate outcome
        
    # Coun the number of players
    n_players = len(players)
    
    # sum values across list
    # sum(players[i].cash for i in range(0,4))