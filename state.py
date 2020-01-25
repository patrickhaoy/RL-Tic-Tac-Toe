import numpy as np

board_rows = 3
board_cols = 3


class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((board_rows, board_cols))
        self.p1 = p1
        self.p2 = p2
        self.is_end = False  # indicates if game ended
        self.board_hash = None
        self.player_symbol = 1  # p1 plays first (p1: 1, p2: -1)

    def get_hash(self):
        self.board_hash = str(self.board.reshape(board_cols * board_rows))
        return self.board_hash

    def available_pos(self):
        pos = []
        for i in range(board_rows):
            for j in range(board_cols):
                if self.board[i, j] == 0:
                    pos.append((i, j))
        return pos

    def update_state(self, pos):
        self.board[pos] = self.player_symbol
        # switch players for next turn
        if self.player_symbol == 1:
            self.player_symbol = -1
        else:
            self.player_symbol = 1

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
        self.is_end = False # !!! Do we need this? !!!
        return None

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
            self.p2.feed_reward(0.5)

