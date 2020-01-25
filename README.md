# RL-Tic-Tac-Toe

I used https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542 as a resource to help me train a bot to play tic-tac-toe with reinforcement learning. Specifically, the bot is trained using Q-learning with the basic value iteration update V(S_t) <- V(S_t) + a(V(S_(t+1)) - V(S_t). 

run_tic_tac_toe.py uses the State object, Player object, and HumanPlayer object defined in state.py, player.py, and human_player.py respectively to train the bots against each other as well as to play the trained bot against the user. "policy_p1" and "policy_p2" are example policies for the bot going first and second (in tic-tac-toe) respectively. They were dumped with Pickle after training through 2,000 iterations.     
