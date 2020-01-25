import numpy as np

board_rows = 3
board_cols = 3

"""
Tic Tac Toe board which updates states of either player as they take an action, judges end of game,
and rewards players accordingly.
"""


class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((board_rows, board_cols))
        self.p1 = p1
        self.p2 = p2
        self.is_end = False  # indicates if game ended
        self.board_hash = None
        self.player_symbol = 1  # p1 plays first (p1: 1, p2: -1)

    """
    Converts current board state to String so it can be stored as the value in the dictionary
    """
    def get_hash(self):
        self.board_hash = str(self.board.reshape(board_cols * board_rows))
        return self.board_hash

    """
    Returns available positions (cells with 0) as an array of pairs representing (x, y) coordinates
    """
    def available_pos(self):
        pos = []
        for i in range(board_rows):
            for j in range(board_cols):
                if self.board[i, j] == 0:
                    pos.append((i, j))
        return pos

    """
    Updates state of board with player's move and switches players for the next turn
    """
    def update_state(self, pos):
        self.board[pos] = self.player_symbol
        # switch players for next turn
        if self.player_symbol == 1:
            self.player_symbol = -1
        else:
            self.player_symbol = 1

    """
    If p1 wins, 1 is returned. If p2 wins, -1 is returned. If it is a tie, 0 is returned.
    In either of these three cases, the game ends. If the game continues, None is returned.
    """
    def winner(self):
        # checks rows for winner
        for i in range(board_rows):
            if sum(self.board[i, :]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.is_end = True
                return -1

        # checks columns for winner
        for i in range(board_rows):
            if sum(self.board[:, i]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.is_end = True
                return -1

        # checks diagonals for winner
        diag_sum1 = sum([self.board[i, i] for i in range(board_cols)])
        diag_sum2 = sum([self.board[i, board_cols - i - 1] for i in range(board_cols)])
        if abs(diag_sum1) == 3 or abs(diag_sum2) == 3:
            self.is_end = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # checks for tie
        if len(self.available_pos()) == 0:
            self.is_end = True
            return 0

        # else, game has not ended yet
        self.is_end = False
        return None

    """
    The winner gets a reward of 1, and the loser gets a reward of 0. 
    As ties are also "undesirable", we set its reward from 0.5 to 0.1 (this is up for experimentation).
    """
    def give_reward(self):
        winner = self.winner()
        if winner == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif winner == -1:
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        else:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.1)

    """
    Training the bots against each other and saving the policies for the player going first as "policy_p1"
    and the player going second as "policy_p2".
    """
    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Round {}".format(i))
            while not self.is_end:
                # Simulating p1's turn
                pos = self.available_pos()
                p1_action = self.p1.choose_action(pos, self.board, self.player_symbol)
                self.update_state(p1_action)
                board_hash = self.get_hash()
                self.p1.add_state(board_hash)

                if self.winner() is not None:
                    self.total_reset()
                    break
                else:
                    pos = self.available_pos()
                    p2_action = self.p2.choose_action(pos, self.board, self.player_symbol)
                    self.update_state(p2_action)
                    board_hash = self.get_hash()
                    self.p2.add_state(board_hash)

                    if self.winner() is not None:
                        self.total_reset()
                        break
        self.p1.save_policy()
        self.p2.save_policy()

    def play2(self):
        while not self.is_end:
            pos = self.available_pos()
            p1_action = self.p1.choose_action(pos, self.board, self.player_symbol)
            self.update_state(p1_action)
            self.show_board()
            winner = self.winner()
            if winner is not None:
                if winner == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.state_reset()
                break

            else:
                pos = self.available_pos()
                p2_action = self.p2.choose_action(pos)

                self.update_state(p2_action)
                self.show_board()
                winner = self.winner()
                if winner is not None:
                    if winner == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.state_reset()
                    break

    def state_reset(self):
        self.board = np.zeros((board_rows, board_cols))
        self.board_hash = None
        self.is_end = False
        self.player_symbol = 1

    def total_reset(self):
        self.give_reward()
        self.p1.reset()
        self.p2.reset()
        self.state_reset()

    def show_board(self):
        for i in range(0, board_rows):
            print("-------------")
            out = "|"
            for j in range(0, board_cols):
                if self.board[i, j] == 1:
                    token = 'x'
                elif self.board[i, j] == -1:
                    token = 'o'
                else:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')
