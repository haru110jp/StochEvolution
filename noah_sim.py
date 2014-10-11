"""
''Author'': Atsushi Yamagishi
''File Name'': noah_sim.py
''License'': MIT license

I thank Daisuke Oyama for his guidance and helpful advice.

This program can simulate the stochastic fictitious play model
by Noah(2014).
"""

from __future__ import division
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Player_Noah():
    """
    <Parameters>
    sigma: the standard deviation of the shock distribution.
           Normal distribution is assumed for simplicitty

    payoffs: payoff matrix.Only symmetric games are allowed.
    epsilon: Weight on the current observation
    """
    def __init__(self, var=1, payoffs=[[4, 0], [3, 2]], epsilon=0.01):
        
        self.num_actions = len(payoffs)
        self.action = 0 # The initial action doesn't matter.
        self.belief = self.init_belief()
        self.epsilon = epsilon
        self.var = var
        self.payoffs = np.array(payoffs)

    def init_belief(self):
        b = [1, 0]
        """
        x = 1
        for i in range(self.num_actions):
            if i != self.num_actions:
                x = random.uniform(0, x)
                b.append(x)
            else:
                y = 1 - sum(b)
                b.append(y)
        """
        return b

    def update_belief(self, opponent_action):
        for i in range(self.num_actions):
            if i == opponent_action:
                self.belief[i] = self.belief[i] + self.epsilon * (1 - self.belief[i])
            else:
                self.belief[i] = (1 - self.epsilon) * self.belief[i]

    def update_action(self):
        expected_payoffs = np.dot(self.payoffs, self.belief)
        # draw the payoff shocks
        for i in range(self.num_actions):
            expected_payoffs[i] = expected_payoffs[i] + random.gauss(0, self.var)
        # determine the best response
        self.action = np.argmax(expected_payoffs)
        
        return self.action

player0 = Player_Noah()
player1 = Player_Noah()

action_0 = []
action_1 = []

for i in range(100000):
    a = player0.update_action()
    action_0.append(a)
    b = player1.update_action()
    action_1.append(b)

    player0.update_belief(b)
    player1.update_belief(a)

n_00 = 0
n_01 = 0
n_10 = 0
n_11 = 0
for i in range(100000):
    b = (action_0[i], action_1[i])
    if b == (0, 0):
        n_00 = n_00 + 1
    if b == (0, 1):
        n_01 = n_01 + 1
    if b == (1, 0):
        n_10 = n_10 + 1
    if b == (1, 1):
        n_11 = n_11 + 1

print(n_00, n_01, n_10, n_11)