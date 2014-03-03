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

def get_players(n_players):
    
    # Ensure the number number of players is acceptable
    if n_players < 2:
        raise ValueError('A game must have at least 2 players.')
    elif n_players > 10:
        raise ValueError('A game must have no more than 10 players.')
    
    # Define player class
    class Player(object):
        
        def __init__(self, player_id):
            self.id = player_id  # Identification number
            self.cash = 1500     # Cash on hand
            self.properties = [] # List of properties
            self.position = 0    # Board position
            self.jail_card = 0   # Number of "Get Out Of Jail Free" cards
            self.jail_turns = 0  # Number of remaining turns in jail
            
        def move(self, dice_value):
            self.position += dice_value
            if self.position >= 40:
                self.position -= 40
                self.cash += 200
        
        def buy(self, prop_id, price):
            self.properties.append(prop_id)
            self.cash -= price
        
        def pay(self, payee, payment):
            if self.cash > payment:
                self.cash -= payment
                players[payee].cash += payment
            else:
                players[payee].cash += self.cash
                self.default(payee, payment)
        
        def default(self):
            del players[self.id]
            
    # Create and fill players list
    players = []
    [players.append(Player(p)) for p in range(n_players)]
    
    # Return players list
    return players



def get_board():

    class Property(object):
        def __init__(self, name, property_type, position, price, rent):
            self.name = name
            self.property_type = property_type
            self.position = position
            self.price = price
            self.price_mortgage = price / 2
            self.rent = rent
            self.rent_now = rent
            self.mortgage = 0
            self.owner = 0
    
    class Utility(Property):
        def __init__(self, name, property_type, position, price, rent):
            Property.__init__(self, name, property_type, position, price, rent)
            self.rent_monopoly = rent + 6
    
    class Railroad(Property):
        def __init__(self, name, property_type, position, price, rent):
            Property.__init__(self, name, property_type, position, price, rent)
            self.rent_double = rent * 2
            self.rent_triple = self.rent_double * 2
            self.rent_monopoly = self.rent_triple * 2
    
    class Street(Property):
        def __init__(self, name, property_type, position, price, rent, color,
                     rent_building, price_building):
                         Property.__init__(self, name, property_type, position,
                                           price, rent)
                         self.rent_monopoly = rent * 2
                         self.color = color
                         self.rent_building = rent_building
                         self.price_building = price_building
                         self.n_building = 0
    
    class Tax(object):
        def __init__(self, name, position, price):
            self.name = name
            self.position = position
            self.price = price
    
    class Space(object):
        def __init__(self, name, position):
            self.name = name
            self.position = position    
    
    # Create a board
    import csv
    with open('board.csv', 'rU') as handle:
        board_csv = csv.DictReader(handle)
        board = []
        for b in board_csv:
            
            # Properties
            if b['type'] == 'street':
                board.append(Street(b['name'], int(b['position']), b['color'],
                                    int(b['price']), int(b['rent']),
                                    int(b['rent_build_1']), int(b['rent_build_2']),
                                    int(b['rent_build_3']), int(b['rent_build_4']),
                                    int(b['rent_build_5']), int(b['cost_build'])))            
            elif b['type'] == 'railroad':
                board.append(Railroad(b['name'], int(b['position'])))
            elif b['type'] == 'utility':
                board.append(Utility(b['name'], int(b['position'])))
            
            # Tax
            elif b['type'] == 'tax':
                board.append(Tax(b['name'], int(b['position']), int(b['price'])))
            
            # Other
            else:
                board.append(Space(b['name'], int(b['position'])))
    
    return board



def roll_dice():
    
    # Import module
    from random import randint

    # Roll two six-sided die
    return sum(randint(1, 6, 2))



def main():
    
    # Declarations
    n_players = 5 # Number of players
    
    # Get board, players, and properties
    players = get_players(n_players)    
    
    # Start the game
    while len(players) > 1:
        
        # Take turns
        for turn in range(n_players):
            
            # Move player
            players[turn].move(roll_dice())
        
        # sum values across list
        # sum(players[i].cash for i in range(0,4))