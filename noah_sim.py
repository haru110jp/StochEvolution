"""
''Author'': Atsushi Yamagishi
''File Name'': noah_sim.py
''License'': MIT license

I thank Daisuke Oyama for his guidance and helpful advice.

This program can simulate the stochastic fictitious play model
by Noah Williams(2014).
"""

from __future__ import division
import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.interpolate import interp1d

class Player_Noah():
    """
    <Parameters>
    sigma: the standard deviation of the shock distribution.
           Normal distribution is assumed for simplicitty

    payoffs: payoff matrix.Only symmetric games are allowed.
    epsilon: Weight on the current observation
    """
    def __init__(self, var=1, \
                 payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]], epsilon=0.2):
        # The payoff shocks are assumed to be normally distributed
        self.num_actions = len(payoffs)
        self.action = 0 # The initial action doesn't matter.
        self.belief = self.init_belief()
        self.epsilon = epsilon
        self.var = var
        self.payoffs = np.array(payoffs)

    def init_belief(self):
        b = []
        # Random mode
        
        x = 1
        for i in range(self.num_actions):
            if i != self.num_actions - 1:
                m = random.uniform(0, x)
                x = x - m
                b.append(m)
            else:
                y = 1 - sum(b)
                b.append(y)

        return b
        

    def update_belief(self, opponent_action):
        
        for i in range(self.num_actions):
            if i == opponent_action:
                current = self.belief[i]
                self.belief[i] = current + self.epsilon * (1 - current)
            else:
                current = self.belief[i]
                self.belief[i] = (1 - self.epsilon) * current
            
        return self.belief

    def update_action(self):
        expected_payoffs = np.dot(self.payoffs, self.belief)
        # draw the payoff shocks
        for i in range(self.num_actions):
            ep_i = expected_payoffs[i] 
            expected_payoffs[i] = ep_i + random.gauss(0, self.var)
        # determine the best response
        self.action = np.argmax(expected_payoffs)
        
        return self.action

# plotting the belief part
"""
"project_3d_to_simplex" is taken from plot_simplex.py by "oyamad"
https://gist.github.com/oyamad/7a11edb8f8e8e24bcf0c
"""

def project_3d_to_simplex(points_ndarray):
    x = np.empty((2, len(points_ndarray)))
    x[:] = \
        (points_ndarray[:, 0] + 2*points_ndarray[:, 2])*sqrt(3)/3, \
        points_ndarray[:, 0]
    return x

player0 = Player_Noah()
player1 = Player_Noah()

T = 10000 # the number of repetition

beliefs_0 = np.empty((T, player0.num_actions))
beliefs_1 = np.empty((T, player1.num_actions))

for i in range(T):
    for m in range(player0.num_actions):
        beliefs_0[i][m] = player0.belief[m]

    for n in range(player1.num_actions):
        beliefs_1[i][n] = player1.belief[n]
        
    a = player0.update_action()
    b = player1.update_action()

    player0.update_belief(b)
    player1.update_belief(a)
    

points_simplex = project_3d_to_simplex(beliefs_0)
points2_simplex = project_3d_to_simplex(beliefs_1)


vertices= np.array([[sqrt(3)/3, 1], [0, 0], [2*sqrt(3)/3, 0]])
triangle = tri.Triangulation(vertices[:, 0], vertices[:, 1])
 
fig, ax = plt.subplots()
ax.triplot(triangle)
ax.set_axis_off()
# ax.set_xlim(0, 2*sqrt(3)/3)
# ax.set_ylim(0, 1)
ax.text(0, 0, '0')
ax.text(sqrt(3)/3, 1, '1')
ax.text(2*sqrt(3)/3, 0, '2')

ax.set_aspect('equal')
ax.scatter(points_simplex[0], points_simplex[1], c='black')
ax.scatter(points2_simplex[0], points2_simplex[1], c='red')
plt.show()
































"""
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
"""