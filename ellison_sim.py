"""
''Author'': Atsushi Yamagishi
''File Name'': ellison_sim.py
''License'': MIT license

I thank Daisuke Oyama for his guidance and helpful advice.

This program can simulate the stochastic evolution model raised
by G, Ellison(1993). The class of games this can handle
is a symmetric game with n strategies.

"""
from __future__ import division
import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.animation as animation
import networkx as nx

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

class Player:
    def __init__(self, how_many_actions, init):
        self.num_of_actions = how_many_actions
        self.init_action(random)

    def init_action(self, random):
        if init != None:
            # random takes int
            self.action = random
        else:
            possible_actions = range(self.num_of_actions)
            self.action = random.choice(possible_actions)
            # the initial action is randomly chosen.


class ellison:
    # This class "inherits" the class "Player" defined above
    def __init__(self,network=nx.cycle_graph(10), n=1,
                 payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]], init=None):
        """
        the default payoffs are those of "3*3 coordination games"

        n = 1  How far players you play a game with
        payoffs = The payoff matrix of the game
        network = The network you want to analyze.Use NetworkX graph
        example: nx.cycle_graph(6)
        """
        self.players = \
        [Player(len(payoffs), init) for i in range(nx.number_of_nodes(network))]
        # "players" is a list consisting of "player"
        self.payoffs = payoffs
        self.num_actions = len(payoffs) # the number of actions
        self.N = nx.number_of_nodes(network) # The number of players
        self.n = n
        self.network = network
        self.adj_matrix = nx.adjacency_matrix(network)
        # actions players can take
        self.actions = range(len(payoffs))

    def show_action_profile(self):
        # shows the current action profile
        action_profile = [self.players[i].action for i in range(self.N)]
        proportions = np.empty(self.num_actions)
        for i in range(self.num_actions):
            proportion_of_i = action_profile.count(i) / float(self.N)
            proportions[i] = proportion_of_i

        print (action_profile,proportions)

    def update_rational(self):  # function used when a player is "rational"
        # pick a player which can change the action
        d = random.choice(range(self.N))
        # computing the shotest_path_length of every pair of players
        s_path = nx.shortest_path_length(self.network)
        s_path_from_d = s_path[d]

        # you cannot play a game with players further by more than n
        for i in s_path_from_d.keys():
            if s_path_from_d[i] > self.n:
                del(s_path_from_d[i])

        del(s_path_from_d[d]) # can't play a game with yourself

        neighbors = s_path_from_d.keys() # whom you play a game with
        # neighbors' action profile
        nei_actions = [self.players[i].action for i in neighbors]

        # computing the ratio of players taking a certain action in the nei
        proportions = np.empty(self.num_actions)
        for i in range(len(self.payoffs)):
            proportion_of_i = nei_actions.count(i) / float(len(nei_actions))
            proportions[i] = proportion_of_i

        # computing the matrix which contains expected payoffs of each action
        expected_payoffs = np.dot(self.payoffs, proportions)

        # determine the action so that
        # it is the best response to the action profile of the community
        self.players[d].action = np.argmax(expected_payoffs)

    def update_irrational(self):  # function used when a player is irrational
        d = random.choice(range(self.N))
        self.players[d].action = random.choice(self.actions)
        # action is randomly chosen because he is irrational

    def play(self, X=10000, epsilon=0):
        """
        X is the number of repetition
        epsilon = the possibility of a player getting "irrational"
        """
        self.show_action_profile()  # show the initial action profile
        for i in range(X):
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()

        self.show_action_profile()
        # show the action profile at the end of the game

    def initialize_action_profile(self):  # initialize players' actions
        for i in self.players:
            i.init_action()

    def visualize_the_network(self):
        nx.draw(self.network)
        plt.show()

    def draw_histogram(self, x=1000, y=100, epsilon=0):
        """
        x: How many times you repeat the "set" of games
        y: How many games constitute one set of games
        """
        result_box = []
        for i in range(x):

            for i in range(y):
                if random.uniform(0, 1) > epsilon:
                    self.update_rational()
                else:
                    self.update_irrational()

            action_profile = [self.players[i].action for i in range(self.N)]
            proportions = np.empty(self.num_actions)
            for i in range(self.num_actions):
                proportion_of_i = action_profile.count(i) / float(self.N)
                proportions[i] = proportion_of_i

            # finding out the most popular strategy
            result_box.append(proportions.argmax())
            # Initializing the profile to go on to the next game
            self.initialize_action_profile()

        fig, ax = plt.subplots()
        ax.hist(result_box)
        plt.show()

    def draw_scatter2(self,x=1000, epsilon=0.1): # only for 2*2 games
        fig, ax = plt.subplots()
        ax.set_xlim([0.0, 1.1])
        ax.set_ylim([0.0, 1.1])
        plt.xlabel("0")
        plt.ylabel("1")

        action_profile = [self.players[i].action for i in range(self.N)]
        # the proportion of action1
        profile = []
        initial_state = action_profile.count(0) / float(self.N)
        initial_dot = plt.scatter(initial_state, 1 - initial_state, c="red")
        profile.append([initial_dot])

        for i in range(x):
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()
            current_profile = [self.players[s].action for s in range(self.N)]
            state = current_profile.count(0) / float(self.N)
            dot = plt.scatter(state, 1- state, c="red")
            profile.append([dot])

        ani = animation.ArtistAnimation(fig, profile, interval=1, repeat_delay=1000)
        plt.show()

    def draw_scatter3(self, x=1000, epsilon=0.1):
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

        action_profile = [self.players[i].action for i in range(self.N)]
        state_lists = np.empty((x, self.num_actions))

        for m in range(x):
            for i in range(self.num_actions): # computing the state
                current_profile = [self.players[s].action for s in range(self.N)]
                proportion_of_i = current_profile.count(i) / float(self.N)
                state_lists[m][i] = proportion_of_i
            # proceed the game
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()

        states_on_simplex = project_3d_to_simplex(state_lists)

        # Plot the scatter.
        ims = []
        # Converting s.t. we can use Artist animation
        for i in range(x):
            im = plt.scatter(states_on_simplex[0][i], states_on_simplex[1][i], c="blue")
            ims.append([im])
        ani = animation.ArtistAnimation(fig, ims, interval=1, repeat_delay=1000)

        plt.show()
