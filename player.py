import numpy as np
import pickle

board_rows = 3
board_cols = 3

"""
Player agent 
"""
class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = [] # all board states played for player in current round
        self.lr = 0.2  # Learning rate, up for experimentation
        self.exp_rate = exp_rate  # exploration rate: % bot takes random move
        self.decay_gamma = 0.9 # % to devalue reward
        self.states_value = {} # reward_value of position

    """
    Converts current board state to String so it can be stored as the value in the dictionary
    """
    def get_hash(self, board):
        board_hash = str(board.reshape(board_cols * board_rows))
        return board_hash

    """
    Returns position that player plays given the current board state.
    There is a exp_rate chance that the player will explore a random move.
    Otherwise, it picked the move with the highest reward given its current information.
    """
    def choose_action(self, positions, current_board, symbol):
        # Player moves randomly self.exp_rate portion of time
        if np.random.uniform(0, 1) < self.exp_rate:
            i = np.random.choice(len(positions))
            action = positions[i]
        # Otherwise, player picks the move with the highest reward
        else:
            value_max = -1000
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_hash(next_board)
                # if board arrangement doesn't exist in states_value yet,
                # player will not move there unless player has not explored any of the possible next board arrangements
                if self.states_value.get(next_board_hash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_board_hash)
                # Updates action if reward is higher in this position than previous positions
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    """
    Value iteration: V(S_t) <- V(S_t) + a(V(S_(t+1)) - V(S_t))
        a: learning rate (self.lr)
        V(S_t): states_value of state t
        V(S_t): states_value of state t+1
    At end of game, backpropagates through all player's board states and applies value iteration from above
    to calculate reward for each state.
    """
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
