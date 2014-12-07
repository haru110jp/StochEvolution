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
import matplotlib.animation as animation

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
        self.belief = [1,0,0] #or, self.init_belief
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
# Returns the position of dots on the simplex
def project_3d_to_simplex(points_ndarray):
    x = np.empty((2, len(points_ndarray)))
    x[:] = \
        (points_ndarray[:, 0] + 2*points_ndarray[:, 2])*sqrt(3)/3, \
        points_ndarray[:, 0]
    return x

player0 = Player_Noah()
player1 = Player_Noah()

T = 1000 # the number of repetition

# Playing the game, saving the belief profile at every t.
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
    
# Determine the positions on the simplex
points_simplex = project_3d_to_simplex(beliefs_0)
points2_simplex = project_3d_to_simplex(beliefs_1)

# Drawing the triangle (= simplex)
vertices= np.array([[sqrt(3)/3, 1], [0, 0], [2*sqrt(3)/3, 0]])
triangle = tri.Triangulation(vertices[:, 0], vertices[:, 1])

fig,ax  = plt.subplots()

# ax.set_xlim(0, 2*sqrt(3)/3)
# ax.set_ylim(0, 1)
ax.triplot(triangle)
ax.set_axis_off()
# ax.set_xlim(0, 2*sqrt(3)/3)
# ax.set_ylim(0, 1)
ax.text(0, 0, '1')
ax.text(sqrt(3)/3, 1, '0')
ax.text(2*sqrt(3)/3, 0, '2')


# Plot the scatter. 
ims1 = []
ims2 = []

# Converting s.t. we can use Artist animation
for i in range(T):
    im1 = plt.scatter(points_simplex[0][i], points_simplex[1][i], c="blue")
    ims1.append([im1])
    
    im2 = plt.scatter(points_simplex[0][i], points_simplex[1][i], c="red")
    ims2.append([im2]) 
     
ani1 = animation.ArtistAnimation(fig, ims1, interval=1, repeat_delay=1000)
ani2 = animation.ArtistAnimation(fig, ims2, interval=1, repeat_delay=1000)

plt.show()


# Drawing a histogram
result_box = []

for i in range(T):
    a = player0.update_action()
    b = player1.update_action()
    
    result_box.append(a)
    result_box.append(b)

    player0.update_belief(b)
    player1.update_belief(a)

fig, ax = plt.subplots()
ax.hist(result_box)
plt.show()