class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action column:"))
            action = (row, col)
            if action in positions:
                return action

    def add_state(self, state):
        pass

    def feed_reward(self, reward):
        pass

    def reset(self):
        pass