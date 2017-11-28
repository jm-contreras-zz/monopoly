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

    # Create dice
    d = classes.Dice()

    # Play as long as more than 1 player remains in game
    while g.players_remaining > 1:

        # Update game round
        g.round += 1

        # Define player of turn
        for turn_player in g.players:

            # Continue if player is bankrupt
            if turn_player.bankrupt:
                continue

            # Continue if player is in jail
            if turn_player.jail_turns > 0:
                continue

            # Roll dice to start turn
            d.roll()

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
