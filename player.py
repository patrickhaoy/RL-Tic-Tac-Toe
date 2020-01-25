import numpy as np
import pickle

board_rows = 3
board_cols = 3

class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}

    def get_hash(self, board):
        board_hash = str(board.reshape(board_cols * board_rows))
        return board_hash

    def choose_action(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) < self.exp_rate:
            i = np.random.choice(len(positions))
            action = positions[i]
        else:
            # ??? choosing p, but how? ???
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_hash(next_board)
                if self.states_value.get(next_board_hash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_board_hash) # ??? Missing value = ???
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] = self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def add_state(self, state):
        self.states.append(state)

    def reset(self):
        self.states = []

    def save_policy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()
