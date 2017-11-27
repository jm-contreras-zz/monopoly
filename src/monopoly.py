import src.classes as classes
import src.config as config
import src.utils as utils


def main():

    # Initialize game
    g = classes.Game()

    # Create list of players
    g.get_players(config.N_PLAYERS)

    # Create board with properties
    g.get_board(config.BOARD_FILENAME)

    # Continue playing as long as more than one player remains in game
    while len(players) > 1:

        # Take turns
        for turn in range(config.N_PLAYERS):

            # Define current player
            curr_player = players[turn]

            # Double roll counter
            n_double_roll = 0

            # Continue turn until player rolls no doubles or goes to jail
            while True:

                # Roll dice
                roll, rolled_double = utils.roll_dice()

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

                    for case in classes.Switch(type(curr_space).__name__):
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
