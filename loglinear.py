from __future__ import division
import random
from math import sqrt, exp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.interpolate import interp1d
import gth_solve as gth


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
                x = x + exp(self.payoffs[n][opponent_action] * self.beta)
            
            y = (self.payoffs[i][opponent_action]) * self.beta
            
            prob_of_i = exp(y) / x
            prob_distribution[i] = prob_of_i

        # Let's decide which action is taken.
        p = prob_distribution.cumsum()
        return p.searchsorted(random.uniform(0, 1))

    def compute_stationary(self, p=0.5):
        # p: the probability player a is given the opportunity to act.
        num_states = self.num_actions**2
        tran = np.zeros([num_states, num_states])
        
        for a in range(num_states):
            action_a = a // self.num_actions
            action_b = a % self.num_actions
            x = 0
            s = 0
            prob_distribution = np.zeros(self.num_actions)

            for b in range(self.num_actions):
                x = x + exp(self.payoffs[b][action_b] * self.beta)

            for c in range(self.num_actions):
                y = (self.payoffs[c][action_b]) * self.beta
                prob_of_c = p * (exp(y) / x)
                prob_distribution[c] = prob_of_c
            
            for i in range(self.num_actions):
                tran[a][action_b + self.num_actions*i] = prob_distribution[i]

            for d in range(self.num_actions):
                s = s + exp(self.payoffs[d][action_a] * self.beta)
            
            for e in range(self.num_actions):
                t = (self.payoffs[e][action_a]) * self.beta
                prob_of_e = (1 - p) * (exp(t) / s)
                prob_distribution[e] = prob_of_e
            
            for i in range(self.num_actions):
                if action_a==0:
                    tran[a][self.num_actions*action_a + i] += prob_distribution[i]
                elif action_a==1:
                    tran[a][self.num_actions*action_a + i] += prob_distribution[i]
                elif action_a==2:
                    tran[a][self.num_actions*action_a + i] += prob_distribution[i]
                    
        u = gth.gth_solve(tran)
        return u


# draw the histogram about the outcome
"""
T = 10000
result_box = []

player0 = Player_loglin(payoffs=[[13, 3, 0], [5, 0, 13], [0, 2, 16]])
player1 = Player_loglin(payoffs=[[13, 3, 0], [5, 0, 13], [0, 2, 16]])

for i in range(T):
    if np.random.random() > 0.5:
        a = player0.update_action(player1.action)
        result_box.append(a)

    else:
        b = player1.update_action(player0.action)
        result_box.append(b)

fig, ax = plt.subplots()
ax.hist(result_box)
plt.show()
"""