import numpy as np
import pandas as pd

import classes


def get_players(n_players):
    """Return dictionary with list of 2 to 8 players.

    Parameter
    ---------
    n_players : int
        Number of players in game

    Return
    ------
    dict
        Dictionary of players
    """

    if n_players < 2 or 8 < n_players:
        raise ValueError('A game must have between 2 to 8 players. You input {} players.'.format(n_players))

    return {classes.Player(p) for p in range(n_players)}


def get_board(board_file):
    """Return game board.

    Parameter
    ---------
    board_file : str
        Filename of CSV with board parameters

    Return
    ------
    board: list
        Board game with one item per space
    """

    board = []

    for _, r in pd.read_csv(board_file).iterrows():

        for case in classes.Switch(r['class']):

            if case('Street'):
                board.append(classes.Street(r['name'], r['position'], r['color'], r['price_buy'], r['price_build'],
                                            r['rent'], [r['rent_build_1'], r['rent_build_2'], r['rent_build_3'],
                                                        r['rent_build_4'], r['rent_build_5']]))

            elif case('Railroad'):
                board.append(classes.Railroad(r['name'], r['position'], r['price_buy'], r['rent']))

            elif case('Utility'):
                board.append(classes.Utility(r['name'], r['position'], r['price_buy'], r['rent']))

            elif case('Tax'):
                board.append(classes.Tax(r['price_buy']))

            elif case('Chance'):
                board.append(classes.Chance())

            elif case('Chest'):
                board.append(classes.Chest())

            elif case('Jail'):
                board.append(classes.Jail())

            elif case('Idle'):
                board.append(classes.Idle())

    return board


def roll_dice(check_double=True):
    """Roll two fair six-sided die.

    Parameter
    ---------
    check_double : bool
        Specify whether return should include boolean indicating if roll was double (defaults to True)

    Returns
    -------
    roll: int
        Sum of roll
    roll_is_double: bool
        Indicate if roll was double
    """

    roll = np.random.choice(np.arange(1, 7), 2)

    if check_double:
        return roll.sum(), roll[0] == roll[1]
    else:
        return roll.sum()
