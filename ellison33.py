# this program is designed for 3*3 games

from __future__ import division
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


class Player:
    def __init__(self, how_many_actions):
        self.num_of_actions = how_many_actions
        self.init_action()
        
    def init_action(self):
        possible_actions = range(self.num_of_actions)
        self.action = random.choice(possible_actions)
    # the initial action is randomly chosen.


class ellison33():
    # This class "inherits" the class "Player" defined above
    def __init__(self, N=10, n=1,
                 payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]]):
        """
        the default payoffs are those of "3*3 coordination games"

        N = 10 # the number of players
        n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
        """
        self.players = [Player(len(payoffs)) for i in range(N)]
        # "players" is a list consisting of "player"
        self.payoffs = payoffs
        self.strategies = len(payoffs)
        self.N = N
        self.n = n
        # actions players can take
        self.actions = range(len(payoffs))

    def show_action_profile(self):
        action_profile = [self.players[i].action for i in range(self.N)]
        proportions = np.empty(self.strategies)
        for i in range(self.strategies):
            proportion_of_i = action_profile.count(i) / float(self.N)
            proportions[i] = proportion_of_i

        print (action_profile,proportions)

    def update_rational(self):  # function used when a player is "rational"
        # pick a player which can change the action
        d = random.choice(range(self.N))
        nei_numbers = []  # contains the number assigned to each neighbor
        nei_numbers_with_large_small = [i for i in range(d-self.n, d+self.n+1)]
        # contains the chosen player,may contain inappropriate numbers
        del nei_numbers_with_large_small[self.n]  # delete the chosen player

        for i in nei_numbers_with_large_small:
            if i < 0:
                i = i + self.N

            if i >= self.N:
                i = i - self.N

            nei_numbers.append(i)

        nei_actions = [self.players[i].action for i in nei_numbers]
        # neighbors' action profile

        # computing the ratio of players taking a certain action in the nei
        proportions = np.empty(self.strategies)
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

    def draw_histogram(self, x=1000, y=100, epsilon=0):
        result_box = []
        for i in range(x):

            for i in range(y):
                if random.uniform(0, 1) > epsilon:
                    self.update_rational()
                else:
                    self.update_irrational()

            action_profile = [self.players[i].action for i in range(self.N)]
            proportions = np.empty(self.strategies)
            for i in range(self.strategies):
                proportion_of_i = action_profile.count(i) / float(self.N)
                proportions[i] = proportion_of_i
            
            # finding out the most popular strategy
            result_box.append(proportions.argmax())
            # Initializing the profile to go on to the next game
            self.initialize_action_profile()

        fig, ax = plt.subplots()
        ax.hist(result_box)
        plt.show()

"""
Visually ugly and useless methods.I don't delete it just because it can be helpful for me in 
writting a method with a similar functionality.
Another bad thing about these methods is that they can be used only for
3*3 games.

    def draw_scatter(self, X=100, epsilon=0): # only for 3*3
        # draws a scatter diagram about the state dynamics during the game.

        action_profile = [self.players[i].action for i in range(self.N)]
        proportions = np.empty((self.strategies, X))
        for i in range(len(self.payoffs)):
            proportion_of_i = action_profile.count(i) / float(self.N)
            proportions[i, 0] = proportion_of_i

        for t in range(X):
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()

            action_profile = [self.players[m].action for m in range(self.N)]
            for i in range(len(self.payoffs)):
                proportion_of_i = action_profile.count(i) / float(self.N)
                proportions[i, t] = proportion_of_i
            
        

        fig = plt.figure()
        ax = Axes3D(fig)
        dots = np.vsplit(proportions, self.strategies)
        print(dots)
        ax.scatter3D(dots[0], dots[1], dots[2])
        plt.show()
        
    def draw_graph(self, X=100, epsilon=0):
        # draws a graph which represents the state dynamics during the game
        action_profile = [self.players[i].action for i in range(self.N)]

        # creating a list of proportions of players taking a certain action
        proportion_0 = []
        proportion_1 = []
        proportion_2 = []

        # computing the initial proportions
        proportion_0.append(action_profile.count(0) / float(self.N))
        proportion_1.append(action_profile.count(1) / float(self.N))
        proportion_2.append(action_profile.count(2) / float(self.N))

        for i in range(X):
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()

            action_profile = [self.players[i].action for i in range(self.N)]
            proportion_0.append(action_profile.count(0) / float(self.N))
            proportion_1.append(action_profile.count(1) / float(self.N))
            proportion_2.append(action_profile.count(2) / float(self.N))

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_wireframe(proportion_0, proportion_1, proportion_2)

        plt.show()

    def draw_histogram1(self, X=100, epsilon=0):
        # draws a histogram about each proportion

        action_profile = [self.players[i].action for i in range(self.N)]

        proportions = np.empty((self.strategies, X))
        for i in range(len(self.payoffs)):
            proportion_of_i = action_profile.count(i) / float(self.N)
            proportions[i, 0] = proportion_of_i

        for t in range(X):
            if random.uniform(0, 1) > epsilon:
                self.update_rational()
            else:
                self.update_irrational()

            action_profile = [self.players[n].action for n in range(self.N)]
            for i in range(self.strategies):
                proportion_of_i = action_profile.count(i) / float(self.N)
                proportions[i, t] = proportion_of_i

        profiles = np.vsplit(proportions, self.strategies)
        print(profiles[0])
        for i in profiles:
            i.transpose()
        fig, axes = plt.subplots(1, self.strategies, figsize=(8, 12))
        for i in range(self.strategies):
            axes[i].hist(profiles[i])

        plt.show()

"""
