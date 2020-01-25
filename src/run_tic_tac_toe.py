from player import Player
from state import State
from human_player import HumanPlayer

p1 = Player("p1")
p2 = Player("p2")

# Trains p1 and p2 against each other 100,000 times. Policies dumped as "policy_p1" and "policy_p2"
st = State(p1, p2)
print("training...")
#st.play(100000)

# Simulate game against player where bot goes first
p1 = Player("computer", exp_rate=0)  # exp_rate set to 0 since bot is not learning here
p1.load_policy("policy_p1")
p2 = HumanPlayer("human")
st = State(p1, p2)
st.play2()

# Simulate game against player where bot goes second
# p1 = HumanPlayer("human")
# p2 = Player("computer", exp_rate=0)
# p2.load_policy("policy_p2")
# st = State(p1, p2)
# st.play2()
