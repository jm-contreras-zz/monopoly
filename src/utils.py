import numpy as np
import pandas as pd

import classes


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
