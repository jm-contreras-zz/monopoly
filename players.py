# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 16:34:30 2013

@author: jmcontreras
"""

# TODO
# Add additional properties (cards on hand, including chance and properties)
# Limit the number of players to maximum allowed in game

def get_players(n_players):
    
    # Check number of players is acceptable
    if n_players < 2:
        print 'A game must have at least 2 players.'
    elif n_players > 10:
        print 'A game must have no more than 10 players.'
        
    # Define player class
    class Player(object):
        def __init__(self, id):
            self.id = id            # Identification number
            self.cash = 1500        # Cash on hand
            self.position = 0       # Board position
            self.jail_turns = 0     # Number of remaining turns in jail
    
    # Create and fill players list
    players = []
    for id in range(1, n_players):
        players.append(Player(id))
    
    # Return players list
    return players