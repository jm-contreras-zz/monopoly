import numpy as np
import pandas as pd

import classes


def get_players(n_players):
    """Return object with a list of players, ensuring that there are between 2 to 8 players."""

    assert n_players >= 2 & n_players <= 8, 'A game must have at least 2 and no more than 8 players.'

    return [classes.Player(i) for i in range(n_players)]


def get_board(board_file):
    """TODO"""

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

    Attributes:
    :param bool check_double: Specify whether roll_dice returns a boolean indicating if the roll was a double roll
    :return int roll: Sum of the roll
    :return bool roll_is_double: Indicate if the roll was a double roll
    """

    roll = np.random.choice(np.arange(1, 7), 2)

    if check_double:
        return roll.sum(), roll[0] == roll[1]
    else:
        return roll.sum()
