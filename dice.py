import logging
import numpy as np

import config


logger = logging.getLogger(__name__)


class Dice:

    def __init__(self):

        self.roll_sum = None
        self.double = False
        self.double_counter = 0

    def roll(self):
        """Roll two fair six-sided die and store (1) the sum of the roll, (2) an indicator of whether it was a double
        roll and (3) a counter of the number of consecutive double rolls."""

        roll = np.random.choice(np.arange(1, 7), 2)

        self.roll_sum = roll.sum()
        self.double = roll[0] == roll[1]
        self.double_counter += self.double

        if config.verbose['dice']:
            logger.info('Roll a {die_1} and a {die_2}'.format(die_1=roll[0], die_2=roll[1]))
