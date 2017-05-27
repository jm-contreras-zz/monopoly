import numpy as np
import pandas as pd

import config as c


###########
# CLASSES #
###########

class Player:

    def __init__(self, player_id):
        """Initialize player."""

        self.id = player_id         # Identification number
        self.cash = 1500            # Cash on hand
        self.properties = []        # List of properties
        self.position = 0           # Board position
        self.jail_cards = 0         # Number of "Get Out Of Jail Free" cards
        self.jail_turns = 0         # Number of remaining turns in jail
        self.jail_strategy = None   # Jail strategy

    def move(self, roll):
        """Move forward on board."""

        self.position += roll
        if self.position >= 40:
            self.position -= 40
            self.cash += 200

    def react_to_property_visit(self, players, prop):
        """Decide whether to pay rent or buy property."""

        prop_has_owner = prop.owner is not None
        prop_has_no_mortgage = prop.mortgage is False
        self_can_afford = self.cash >= prop.price

        if prop_has_owner and prop_has_no_mortgage:
            self.pay(players[prop.owner], prop.rent_now)

        elif ~prop_has_owner and self_can_afford:
            self.buy(prop)

    def evaluate_build(self):
        # Create a way to let players know when they have a monopoly
        # Create a way also of letting players know how many buildings they have
        # The second is a little tougher because you have to build them in a certain order
        # At first, just choose randomly
        # Then, they can start building their hotels as soon as they can
        pass

    def buy(self, property_):
        """Acquire a property from the bank or another player. Pay for the property and update ownership."""

        self.properties.append(property_.position)
        self.cash -= property_.price
        property_.owner = self.id

        if c.VERBOSE:
            print 'Player {} bought {} from {}'.format(self.id, property_.name, '')

    def pay(self, other, payment):
        """Pay for a property"""

        self.cash -= payment
        other.cash += payment

        if c.VERBOSE:
            print 'Player {} paid ${} to Player {}'.format(self.id, payment, other.id)

    def go_to_jail(self):
        """Send player to jail."""

        self.position = 10
        self.jail_turns = 3

        if c.VERBOSE:
            print 'Player {} goes to jail'.format(self.id)

    def choose_jail_strategy(self, rolled_double):
        """"""

        if self.jail_cards > 0:
            self.jail_strategy = 'card'
            self.jail_turns = 0
            self.jail_cards -= 1

        elif self.cash >= 50:
            self.jail_strategy = 'pay'
            self.jail_turns = 0
            self.cash -= 50

        else:
            self.jail_strategy = 'roll'
            if rolled_double:
                self.jail_turns = 0
            else:
                self.jail_turns -= 1
                if self.jail_turns == 0:
                    self.cash -= 50

        if c.VERBOSE:
            print 'Player {} took jail strategy {} and has {} turns left'.format(self.id, self.jail_strategy,
                                                                                 self.jail_turns)

    def default(self, players):

        del players[self.id]


class Property(object):
    def __init__(self, name, position, price, rent):
        self.name = name
        self.position = position
        self.price = price
        self.price_mortgage = price / 2
        self.rent = rent
        self.rent_now = rent
        self.mortgage = False
        self.owner = None


class Street(Property):
    def __init__(self, name, position, color, price,
                 price_building, rent, rent_building):
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


#############
# FUNCTIONS #
#############

def get_players(n_players):
    """Return object with a list of players, ensuring that there are between 2 to 8 players."""

    assert n_players >= 2 & n_players <= 8, 'A game must have at least 2 and no more than 8 players.'

    return [Player(i) for i in range(n_players)]


def get_board(board_file):
    """TODO"""

    board = []

    for _, r in pd.read_csv(board_file).iterrows():
        for case in Switch(r['class']):
            if case('Street'):
                board.append(Street(r['name'], r['position'], r['color'], r['price_buy'], r['price_build'], r['rent'],
                                    [r['rent_build_1'], r['rent_build_2'], r['rent_build_3'], r['rent_build_4'],
                                     r['rent_build_5']]))
            elif case('Railroad'):
                board.append(Railroad(r['name'], r['position'], r['price_buy'], r['rent']))
            elif case('Utility'):
                board.append(Utility(r['name'], r['position'], r['price_buy'], r['rent']))
            elif case('Tax'):
                board.append(Tax(r['price_buy']))
            elif case('Chance'):
                board.append(Chance())
            elif case('Chest'):
                board.append(Chest())
            elif case('Jail'):
                board.append(Jail())
            elif case('Idle'):
                board.append(Idle())

    return board


def roll_dice(check_double=True):
    """Roll two fair six-sided die.

    Attributes:
    :param bool check_double: Specify whether roll_dice returns a boolean indicating if the roll was a double roll
    :return int roll: Sum of the roll
    :return bool roll_is_double: Indicate if the roll was a double roll
    """

    roll = np.random.choice(np.arange(1, 7), 2)

    if c.VERBOSE:
        print 'Die roll: {} and {}'.format(roll[0], roll[1])

    if check_double:
        return roll.sum(), roll[0] == roll[1]
    else:
        return roll.sum()


class Switch(object):

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
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def main():

    # Create object with players
    players = get_players(c.N_PLAYERS)

    # Create board with properties
    board = get_board(c.BOARD_FILENAME)

    # Continue playing as long as more than one player remains in game
    while len(players) > 1:

        # Take turns
        for turn in range(c.N_PLAYERS):

            # Define current player
            curr_player = players[turn]

            # Double roll counter
            n_double_roll = 0

            # Continue turn until player rolls no doubles or goes to jail
            while True:

                # Roll dice
                roll, rolled_double = roll_dice()

                # Update double roll counter
                n_double_roll += int(rolled_double)

                # If player is in jail
                if players[turn].jail_turns > 0:

                    # Select jail strategy
                    curr_player.choose_jail_strategy(rolled_double)

                    # If player is still in jail
                    if curr_player.jail_turns > 0:
                        break

                # If player rolled less than 3 doubles
                if n_double_roll < 3:

                    # Move player
                    curr_player.move(roll)

                    # Define current board space
                    curr_space = board[curr_player.position]

                    for case in Switch(type(curr_space).__name__):
                        if case('Street'):
                            curr_player.evaluate_buy(curr_space, players)

                    # If no double rolled, end turn
                    if not rolled_double:
                        break

                # Otherwise, send player to jail and end turn
                elif n_double_roll == 3:

                    curr_player.go_to_jail()
                    break

                    # Now here is where we start interacting with the board
                    # type(board[4]).__name__

        game_round += 1

        if game_round == 10:
            break
