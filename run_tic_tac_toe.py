from player import Player
from state import State
from human_player import HumanPlayer

p1 = Player("p1")
p2 = Player("p2")

st = State(p1, p2)
print("training...")
st.play(100000)

p1 = Player("computer", exp_rate=0)
p1.load_policy("policy_p1")

p2 = HumanPlayer("human")

st = State(p1, p2)
st.play2()
