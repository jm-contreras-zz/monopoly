import logging
import sys

import config
import dice
import game
import spaces


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():

    # Initialize game
    g = game.Game()

    # Create list of players
    g.get_players(config.N_PLAYERS)

    # Create bank
    g.get_bank()

    # Create board with properties
    g.get_board(config.BOARD_FILENAME)

    # Play as long as more than 1 player remains in game
    while g.players_remaining > 1:

        # Update game round
        g.update_round()

        # Define player of turn
        for turn_player in g.players:

            # Initialize dice
            d = dice.Dice()

            # Continue until turn ends
            while True:

                # Skip turn if player is bankrupt
                if turn_player.bankrupt:
                    break

                # Roll the dice
                d.roll()

                # If third double, then go to jail and end turn
                if d.double_counter == 3:
                    turn_player.go_to_jail()
                    break

                # Continue if player is in jail
                if turn_player.jail_turns > 0:
                    stay_in_jail = turn_player.choose_jail_strategy(rolled_double=d.double)
                    if stay_in_jail:
                        break

                # Move player
                turn_player.move(d.roll_sum)

                # Define current board space
                space = g.board[turn_player.position]

                # Pay taxes
                if isinstance(space, spaces.Tax):
                    turn_player.pay(space.tax, g.bank)

                # Choose property strategy
                elif isinstance(space, spaces.Property):
                    turn_player.choose_property_strategy(space)

                # TODO: Write a method that checks for monopolies every time a property is acquired so that you know
                if len(turn_player.properties) > 0:
                    turn_player.choose_building_strategy()


if __name__ == '__main__':

    main()
