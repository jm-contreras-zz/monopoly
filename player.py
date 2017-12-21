import logging

import bank
import config


logger = logging.getLogger(__name__)


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
        """
        Move player on the board. Update player's position and collect $200 if player passed Go.
        :param int roll: Number of board positions to move
        """

        old_position = self.position

        self.position += roll

        if self.position >= 40:
            self.position -= 40
            self.cash += 200

        if config.verbose['move']:
            logger.info('Player {id} moved on board from position {old_position} to {new_position}'.format(
                id=self.id, old_position=old_position, new_position=self.position))

    def visit_property(self, property_):
        """
        Visit a property and act accordingly. Currently, a player always tries to buy the property if it is unowned.
        :param Property property_: Property object
        """

        is_owned = property_.owner is not None
        is_unmortgaged = not property_.mortgage
        can_afford_rent = self.cash >= property_.get_rent()
        can_afford_purchase = self.cash >= property_.price

        if is_owned and is_unmortgaged:
            if can_afford_rent:
                self.pay(payment=property_.rent_now, recipient=property_.owner)
            else:
                self.go_bankrupt(creditor=property_.owner)

        elif not is_owned and can_afford_purchase:
            self.buy_property(property_)

    def pay(self, payment, recipient):
        """
        Pay an amount of cash to a recipient.
        :param int payment: Cash to be paid to recipient
        :param obj recipient: Player or bank receiving payment
        """

        if self.cash >= payment:
            self.cash -= payment
            recipient.cash += payment

        if config.verbose['pay']:
            logger.info('Player {id} paid ${payment} to {recipient}'.format(
                id=self.id, payment=payment, recipient=recipient.id))

    def buy_property(self, property_):
        """Buy property from another player or bank."""
        # TODO: Implement option to buy from another player

        self.properties.append(property_)
        self.cash -= property_.price
        property_.owner = self

        self.count_monopolies()

        if config.verbose['buy']:
            logger.info('Player {id} paid ${price} to buy property {property} from the bank'.format(
                id=self.id, price=property_.price, property=property_.name))

    def count_monopolies(self):
        self.properties

    def buy_building(self):
        """Buy any building that can be legally bought."""
        for m in self.monopolies:


    def go_to_jail(self):
        """Send player to jail. Update their position on the board and start the jail turn counter."""

        self.position = 10
        self.jail_turns = 3

        logger.info('Player {id} went to jail'.format(id=self.id))

    def choose_jail_strategy(self, rolled_double):
        # TODO: Replace with artificially-intelligent strategy
        """
        Decide what to do during a turn in jail. Currently, a player chooses the following strategies in this order:
        Roll a double, use a Get Out of Jail Free card, and pay $50.
        :param bool rolled_double: Indicator denoting whether dice roll was double
        :return bool stay_in_jail: Indicator denoting whether player remains in jail for additional turn(s)
        """

        if rolled_double:
            self.jail_turns = 0
            logger.info('Player {id} rolled double'.format(id=self.id))
            return False

        # TODO: Add option to buy a Get Out of Jail Free card
        if self.jail_cards > 0:
            self.jail_turns = 0
            self.jail_cards -= 1
            logger.info('Player {id} used a Get Out of Jail Free card'.format(id=self.id))
            return False

        # TODO: Add option to fix bug of having player with negative cash
        if self.cash >= 50:
            self.jail_turns = 0
            self.cash -= 50
            logger.info('Player {id} paid to leave jail'.format(id=self.id))
            return False

        self.jail_turns -= 1
        return True

    def go_bankrupt(self, creditor):
        """Remove player from game. Update number of players that remain in the game."""
        # TODO: Update to give back cash and properties and pay creditor

        self.bankrupt = True

        if type(creditor) == bank.Bank:
            pass
        else:
            pass

        logger.info('Player {id} went bankrupt'.format(id=self.id))
