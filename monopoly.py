# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:24:44 2013

@author: jmcontreras
"""

# v 1.0 GET THE MECHANICS OF THE GAME GOING

# This is what is happening so far:

# (1) Players go around the board by rolling the dice. Doubles allow another
#     turn and 3 doubles land a player in jail.
# (2) Once in jail, players take the following strategy: use a get-out-of-jail  
#     card if you have one, otherwise pay as soon as you can, otherwise roll

# Next up
# TODO: Allow a player without cash to sell their properties before defaulting
#       Check the pay method of the Player object
# TODO: Many of the classes (Chance, Chest, Idle) need work

# v 2.0 MAKE THE GAME SMART

# TODO: Players consider the state of the board before choosing a jail strategy


# Import modules
import csv
import numpy as np



def get_players(n_players):

    # Ensure number of players is acceptable
    if n_players < 2:
        raise ValueError('A game must have at least 2 players.')
    elif n_players > 8:
        raise ValueError('A game must have no more than 8 players.')
    
    # Define player class
    class Player(object):
        
        def __init__(self, player_id):
            self.id = player_id  # Identification number
            self.cash = 1500     # Cash on hand
            self.properties = [] # List of properties
            self.position = 0    # Board position
            self.jail_cards = 0  # Number of "Get Out Of Jail Free" cards
            self.jail_turns = 0  # Number of remaining turns in jail
            self.jail_strtg = '' # Jail strategy
        
        # Move player across board
        def move(self, roll, verbose=False):
            self.position += roll
            if self.position >= 40:
                self.position -= 40
                self.cash += 200
            if verbose:
                print 'Player {} to space: {}'.format(self.id, self.position)
        
        # Buy property
        def buy(self, prop_id, price):
            self.properties.append(prop_id)
            self.cash -= price
        
        # Pay another player
        def pay(self, payee, payment):
            if self.cash > payment:
                self.cash -= payment
                players[payee].cash += payment
            else:
                players[payee].cash += self.cash
                self.default(payee, payment)
        
        # Go to jail
        def go_to_jail(self):
            self.position = 10
            self.jail_turns = 3
        
        # Choose jail strategy
        def choose_jail_strtg(self, rolled_double):
            if self.jail_cards > 0:
                self.jail_strtg = 'card'
                self.jail_turns = 0
                self.jail_cards -= 1
            elif self.cash >= 50:
                self.jail_strtg = 'pay'
                self.jail_turns = 0
                self.cash -= 50
            else:
                self.jail_strtg = 'roll'
                if rolled_double:
                    self.jail_turns = 0
                else:
                    self.jail_turns -= 1
                    if self.jail_turns == 0:
                        self.cash -= 50
        
        # Default
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



def roll_dice(check_double=True, verbose=False):

    # Roll two six-sided die
    roll = np.random.choice(np.arange(1, 7), 2)
    
    # Report roll, if requested
    if verbose:
        print 'Die roll: {} and {}'.format(roll[0], roll[1])
    
    # Return roll sum and, if requested, double roll indicator
    if check_double:
        return roll.sum(), roll[0] == roll[1]
    else:
        return roll.sum()




class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


def main():
    
    # Declarations
    n_players = 5
    board_file = '/Users/jmcontreras/GitHub/monopoly/board.csv'
    
    # Get players and board (including properties)
    players = get_players(n_players)
    board = get_board(board_file)
    
    game_round = 1    
    
    # Start game
    while len(players) > 1:
        
        # Take turns
        for turn in range(n_players):
            
            # Double roll counter
            n_double_roll = 0
            
            # Continue turn until player rolls no doubles or goes to jail
            while True:
                
                # Roll dice
                roll, rolled_double = roll_dice(verbose=False)

                # Update double roll counter
                n_double_roll += (rolled_double).astype(int)
                
                # If player is in jail
                if players[turn].jail_turns > 0:
                    
                    # Select jail strategy
                    players[turn].choose_jail_strtg(rolled_double)
                    
                    # If player is still in jail
                    if players[turn].jail_turns > 0:
                        break
                
                # If player rolled less than 3 doubles
                if n_double_roll < 3:
                    
                    # Move player 
                    players[turn].move(roll, verbose=False)

                    # If no double rolled, end turn
                    if not rolled_double:
                        break
                
                # Otherwise, send player to jail and end turn
                else:
                    players[turn].go_to_jail()
                    break
                
                # Now here is where we start interacting with the board
                type(board[4]).__name__
                http://code.activestate.com/recipes/410692/
        
        game_round += 1      
        
        if game_round == 20:
            break
        
        # sum values across list
        # sum(players[i].cash for i in range(0,4))

if __name__ == '__main__':
    
    main()