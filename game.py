import logging

import pandas as pd

import bank
import config
import dice
import player
import spaces


logger = logging.getLogger(__name__)


class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.round = 0
        self.players = None
        self.bank = None
        self.board = None
        self.dice = None
        self.players_remaining = None

        self.get_players(config.n_players)
        self.get_bank()
        self.get_board(config.board_filename)

    def get_players(self, n_players):
        """
        Create list of 2 to 8 game players.
        :param int n_players: Number of players in game
        """

        # Ensure number of players requested is legal
        if (n_players < 2) or (8 < n_players):
            raise ValueError('A game must have between 2 to 8 players. You input {} players.'.format(n_players))

        # Create list of players and set number of players remaining
        self.players = [player.Player(p) for p in range(1, n_players + 1)]
        self.players_remaining = n_players

    def get_bank(self):
        """
        Create a bank and subtract from its reserves the cash allotted to players.
        """

        self.bank = bank.Bank()
        self.bank.cash -= self.players_remaining * 1500

    def get_board(self, board_file):
        """
        Create board game with properties from CSV file in board_file.
        :param str board_file: Filename of CSV with board parameters
        """

        board_df = pd.read_csv(board_file)

        for _, attributes in board_df.iterrows():

            if attributes['class'] == 'Street':
                self.board.append(spaces.Street(attributes))

            if attributes['class'] == 'Railroad':
                self.board.append(spaces.Railroad(attributes))

            if attributes['class'] == 'Utility':
                self.board.append(spaces.Utility(attributes))

            if attributes['class'] == 'Tax':
                self.board.append(spaces.Tax(attributes))

            if attributes['class'] == 'Chance':
                self.board.append(spaces.Chance())

            if attributes['class'] == 'Chest':
                self.board.append(spaces.Chest())

            if attributes['class'] in ['Jail', 'Idle']:
                self.board.append([])

    def pass_dice(self):

        self.dice = dice.Dice()

    def update_round(self):

        self.round += 1

        if config.verbose['round']:
            logger.info('\n')
            logger.info('Starting round {round}...'.format(round=self.round))
