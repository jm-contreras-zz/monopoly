import numpy as np
import pandas as pd


class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.players = []
        self.players_remaining = None
        self.board = []
        self.round = 0

    def get_players(self, n_players):
        """
        Create list of 2 to 8 game players.
        :param int n_players: Number of players in game
        """

        # Ensure number of players requested is legal
        if (n_players < 2) or (8 < n_players):
            raise ValueError('A game must have between 2 to 8 players. You input {} players.'.format(n_players))

        # Create list of players and set number of players remaining
        self.players = [Player(p) for p in range(n_players)]
        self.players_remaining = n_players

    def get_board(self, board_file):
        """
        Create board game with properties from CSV file in board_file.
        :param str board_file: Filename of CSV with board parameters
        """

        for _, r in pd.read_csv(board_file).iterrows():

            for case in Switch(r['class']):

                if case('Street'):
                    self.board.append(Street(r['name'], r['position'], r['color'], r['price_buy'], r['price_build'],
                                             r['rent'], [r['rent_build_1'], r['rent_build_2'], r['rent_build_3'],
                                                         r['rent_build_4'], r['rent_build_5']]))

                elif case('Railroad'):
                    self.board.append(Railroad(r['name'], r['position'], r['price_buy'], r['rent']))

                elif case('Utility'):
                    self.board.append(Utility(r['name'], r['position'], r['price_buy'], r['rent']))

                elif case('Tax'):
                    self.board.append(Tax(r['price_buy']))

                elif case('Chance'):
                    self.board.append(Chance())

                elif case('Chest'):
                    self.board.append(Chest())

                elif case('Jail'):
                    self.board.append(Jail())

                elif case('Idle'):
                    self.board.append(Idle())


class Player:
    # TODO: check_monopoly function for players to determine whether they can build
    # TODO: check_buildings function for players to determine where they can build
    # TODO: Return properties to bank upon bankruptcy

    def __init__(self, player_id):

        self.id = player_id    # Identification number
        self.cash = 1500       # Cash on hand
        self.properties = []   # List of properties
        self.position = 0      # Board position
        self.jail_cards = 0    # Number of "Get Out Of Jail Free" cards
        self.jail_turns = 0    # Number of remaining turns in jail
        self.bankrupt = False  # Bankrupt status

    def move(self, roll):
        """Move forward on board."""

        self.position += roll

        if self.position >= 40:
            self.position -= 40
            self.cash += 200

    def react_to_property_visit(self, players, prop):
        """Decide whether to pay rent or buy property."""

        prop_is_owned = prop.owner is not None
        prop_is_unmortgaged = prop.mortgage is False
        player_can_afford = self.cash >= prop.price

        if prop_is_owned and prop_is_unmortgaged:
            self.pay(players[prop.owner], prop.rent_now)

        elif ~prop_is_owned and player_can_afford:
            self.buy(prop)

    def pay(self, seller, payment):
        """Pay cash to another player or bank."""

        self.cash -= payment
        seller.cash += payment

    def buy(self, prop_on_sale):
        """Buy property from another player or bank."""

        self.properties.append(prop_on_sale.position)
        self.cash -= prop_on_sale.price
        prop_on_sale.owner = self.id

    def go_to_jail(self):
        """Send player to jail."""

        self.position = 10
        self.jail_turns = 3

    def take_jail_turn(self, rolled_double):
        """Take turn in jail."""

        if self.jail_cards > 0:
            self.jail_turns = 0
            self.jail_cards -= 1

        elif self.cash >= 50:
            self.jail_turns = 0
            self.cash -= 50

        else:
            if rolled_double:
                self.jail_turns = 0
            else:
                self.jail_turns -= 1
                if self.jail_turns == 0:
                    self.cash -= 50

    def go_bankrupt(self, game):
        """Remove player from game."""

        self.bankrupt = True
        game.players_remaining -= 1


class Dice:

    def __init__(self):

        self.roll = None
        self.double = False
        self.double_counter = 0

    def roll(self):
        """Roll two fair six-sided die and store the sum of the roll, an indicator of whether the roll was double, and a
        counter of the number of consecutive double rolls."""

        roll = np.random.choice(np.arange(1, 7), 2)

        self.roll = roll.sum()
        self.double = roll[0] == roll[1]
        self.double_counter += self.double


class Property:

    def __init__(self, name, position, price, rent):
        """Initialize base property."""

        self.name = name                 # Property name
        self.position = position         # Board position
        self.price = price               # Price to buy
        self.price_mortgage = price / 2  # Mortgage price
        self.rent = rent                 # Initial rent
        self.rent_now = rent             # Current rent
        self.mortgage = False            # Mortgage status
        self.owner = None                # Property owner


class Street(Property):

    def __init__(self, name, position, color, price, price_building, rent, rent_building):
        """Initialize street."""

        Property.__init__(self, name, position, price, rent)

        self.color = color                    # Monopoly color
        self.price_building = price_building  # Building cost
        self.rent_monopoly = rent * 2         # Rent with monopoly
        self.rent_building = rent_building    # Building rent
        self.n_building = 0                   # Number of buildings


class Railroad(Property):

    def __init__(self, name, position, price, rent):
        """Initialize railroad."""

        Property.__init__(self, name, position, price, rent)

        self.rent_double = rent * 2    # Rent with 2 railroads
        self.rent_triple = rent * 3    # Rent with 3 railroads
        self.rent_monopoly = rent * 4  # Rent with 4 railroads


class Utility(Property):

    def __init__(self, name, position, price, rent):
        """Initialize utility."""

        Property.__init__(self, name, position, price, rent)

        self.rent_monopoly = rent + 6  # Rent with utility monopoly


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
