import src.classes as classes
import src.config as config


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

            # Continue until turn ends
            while True:

                # Continue if player is bankrupt
                if turn_player.bankrupt:
                    break

                # Continue if player is in jail
                if turn_player.jail_turns > 0:
                    break

                # Roll dice to start turn
                d.roll()

                # Send player to jail if they roll 3 doubles
                if d.double_counter == 3:
                    turn_player.go_to_jail()
                    break

                # Move player
                turn_player.move(d.roll)

                # Define current board space
                curr_space = board[curr_player.position]

                for case in classes.Switch(type(curr_space).__name__):
                    if case('Street'):
                        curr_player.evaluate_buy(curr_space, players)