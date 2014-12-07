from __future__ import division
import random
from math import sqrt, exp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.interpolate import interp1d

class Player_loglin():
    """
    This is designed for two player games. To compare this with models like
    "stochastic fictitious play," this is sufficient. Remember, however, that
    the original model is a n players game.
    
    <Parameters>
    beta: The indicator of rationality. Completely random if 0.
    payoffs: payoff matrix.Only symmetric games are allowed.
    """
    def __init__(self, beta=1, payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]]):
        # The payoff shocks are assumed to be normally distributed
        self.num_actions = len(payoffs)
        self.action = random.choice(range(len(payoffs)))
        self.beta = beta
        self.payoffs = np.array(payoffs)

    def update_action(self, opponent_action):
        # comptute the prob each action is taken, given the other's action
        # First compute the probability with which an action is taken.
        # Computing (2.3) in the original thesis by Okada and Oliver.
        prob_distribution = np.zeros(self.num_actions)

        for i in range(self.num_actions):
            x = 0
            for n in range(self.num_actions):
                x = x + exp(self.payoffs[opponent_action][n] * self.beta)
            
            y = (self.payoffs[opponent_action][i]) * self.beta
            
            prob_of_i = exp(y) / x
            prob_distribution[i] = prob_of_i

        # Let's decide which action is taken.
        p = prob_distribution.cumsum()
        return p.searchsorted(random.uniform(0, 1))

# draw the histogram about the outcome

T = 10000
result_box = []

player0 = Player_loglin(payoffs=[[13, 3, 0], [5, 0, 13], [0, 2, 16]])
player1 = Player_loglin(payoffs=[[13, 3, 0], [5, 0, 13], [0, 2, 16]])

for i in range(T):
    a = player0.update_action(player1.action)
    b = player1.update_action(player0.action)
    
    result_box.append(a)
    result_box.append(b)

fig, ax = plt.subplots()
ax.hist(result_box)
plt.show()
