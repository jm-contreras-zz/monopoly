import src.classes as classes
import src.config as config


def main():

    # Initialize game
    g = classes.Game()

    # Create list of players
    g.get_players(config.N_PLAYERS)

    # Create board with properties
    g.get_board(config.BOARD_FILENAME)

    # Play as long as more than 1 player remains in game
    while g.players_remaining > 1:

        # Update game round
        g.round += 1

        # Define player of turn
        for turn_player in g.players:

            # Initialize dice
            d = classes.Dice()

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
                    leave_jail = turn_player.choose_jail_strategy(rolled_double=d.double)
                    if not leave_jail:
                        break

                # Move player
                turn_player.move(d.roll)

                # TODO: This is where you stopped
                # Define current board space
                curr_space = board[curr_player.position]

                for case in classes.Switch(type(curr_space).__name__):
                    if case('Street'):
                        curr_player.evaluate_buy(curr_space, players)