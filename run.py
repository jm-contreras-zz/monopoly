# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:24:44 2013

@author: jmcontreras
"""

# TODO: Allow players to play a second turn when the roll doubles
# TODO: Attempt one play
# TODO: Allow a player without cash to sell their properties before defaulting
#       Check the pay method of the Player object
# TODO: Many of the classes (Card, Chance, Chest, Jail, Idle) need work



# Import modules
import csv
import numpy as np



def get_players(n_players):
    
    # Ensure the number of players is acceptable
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
        
        # Move the player across the board
        def move(self, dice_value):
            self.position += dice_value
            if self.position >= 40:
                self.position -= 40
                self.cash += 200
        
        # Buy a property
        def buy(self, prop_id, price):
            self.properties.append(prop_id)
            self.cash -= price
        
        # Pay anoter player
        def pay(self, payee, payment):
            if self.cash > payment:
                self.cash -= payment
                players[payee].cash += payment
            else:
                players[payee].cash += self.cash
                self.default(payee, payment)
        
        def default(self):
            del players[self.id]
            
    # Create and return players list
    players = [Player(p) for p in xrange(n_players)]
    return players


def get_board(board_file):
    
    class Property(object):
        def __init__(self, name, position, price, rent):
            self.name = name
            self.position = position
            self.price = price
            self.price_mortgage = price / 2
            self.rent = rent
            self.rent_now = rent
            self.mortgage = 0
            self.owner = 0

    class Street(Property):
        def __init__(self, name, position, color, price, price_building, rent,
                     rent_building):
                         Property.__init__(self, name, position, price, rent)
                         self.color = color
                         self.price_building = price_building
                         self.rent_monopoly = rent * 2
                         self.rent_building = rent_building
                         self.n_building = 0

    class Railroad(Property):
        def __init__(self, name, position, price, rent):
            Property.__init__(self, name, position, price, rent)
            self.rent_double = rent * 2
            self.rent_triple = self.rent_double * 2
            self.rent_monopoly = self.rent_triple * 2
    
    class Utility(Property):
        def __init__(self, name, position, price, rent):
            Property.__init__(self, name, position, price, rent)
            self.rent_monopoly = rent + 6
    
    class Tax(object):
        def __init__(self, price):
            self.price = price

    class Card(object):
        pass  
    
    class Chance(object):
        pass
    
    class Chest(object):
        pass
    
    class Jail(object):
        pass
    
    class Idle(object):
        pass
    
    board = []
    for r in csv.DictReader(open(board_file, 'rU')):
        if r['Space'] == 'Street':
            board.append(Street(r['Name'], int(r['Position']), r['Color'],
                                int(r['Price']), int(r['PriceBuild']),
                                int(r['Rent']), [int(r['RentBuild1']),
                                int(r['RentBuild2']), int(r['RentBuild3']),
                                int(r['RentBuild4']), int(r['RentBuild5'])]))
        elif r['Space'] == 'Railroad':
            board.append(Railroad(r['Name'], int(r['Position']),
                                  int(r['Price']), int(r['Rent'])))
        elif r['Space'] == 'Utility':
            board.append(Utility(r['Name'], int(r['Position']),
                                 int(r['Price']), int(r['Rent'])))
        elif r['Space'] == 'Tax':
            board.append(Tax(int(r['Price'])))
        elif r['Space'] == 'Chance':
            board.append(Chance())
        elif r['Space'] == 'Chest':
            board.append(Chest())
        elif r['Space'] == 'Jail':
            board.append(Jail())
        elif r['Space'] == 'Idle':
            board.append(Idle())
    
    return board



def roll_dice():

    # Roll two six-sided die
    return np.random.choice(np.arange(1, 7), 2)



def main():
    
    # Declarations
    n_players = 5
    board_file = '/Users/jmcontreras/GitHub/monopoly/board.csv'
    
    # Get board, players, and properties
    players = get_players(n_players)    
    board = get_board(board_file)
    
    # Start the game
    while len(players) > 1:
        
        # Take turns
        for turn in range(n_players):
            
            # Move player
            players[turn].move(roll_dice())
        
        # sum values across list
        # sum(players[i].cash for i in range(0,4))