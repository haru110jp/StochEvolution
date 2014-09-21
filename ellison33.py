# this program is designed for 3*3 games

from __future__ import division
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


class Player:
    def __init__(self):
        self.init_action()

    def init_action(self):
        actions = [0, 1, 2]
        self.action = random.choice(actions)
    # the initial action is randomly chosen.


class ellison33():
    # This class "inherits" the class "Player" defined above
    def __init__(self, N=10, n=1,
                 payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]]):
        """
        payoffs takes the form of "the list of the lists containing lists"
        the default payoffs are those of "3*3 coordination games"

        N = 10 # the number of players
        n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
        """
        self.players = [Player() for i in range(N)]
        # "players" is a list consisting of "player"
        self.payoffs = payoffs
        self.N = N
        self.n = n
        self.actions = [0, 1, 2]

    def show_action_profile(self):
        action_profile = [self.players[i].action for i in range(self.N)]

        proportion_0 = action_profile.count(0) / float(self.N)
        proportion_1 = action_profile.count(1) / float(self.N)
        proportion_2 = action_profile.count(2) / float(self.N)

        print (action_profile, proportion_0, proportion_1, proportion_2)

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

        nei_action = [self.players[i].action for i in nei_numbers]
        # neighbors' action profile

        # computing the ratio of players taking a certain action in the nei
        proportion_of_0 = sum(0 == k for k in nei_action) / float(len(nei_action))
        proportion_of_1 = sum(1 == k for k in nei_action) / float(len(nei_action))
        proportion_of_2 = 1 - proportion_of_0 - proportion_of_1

        action_profile = np.array([proportion_of_0, proportion_of_1, proportion_of_2])

        # computing the matrix which contains expected payoffs of each action
        expected_payoffs = np.dot(self.payoffs, action_profile)

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

    def draw_scatter(self, X=100, epsilon=0):
        # draws a scatter diagram about the state dynamics during the game.

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

        ax.scatter3D(proportion_0, proportion_1, proportion_2)
        plt.show()

    def draw_histogram1(self, X=100, epsilon=0):
        # draws a histogram about each proportion

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

        fig, axes = plt.subplots(1, 3, figsize=(8, 12))
        list_of_proportions = [proportion_0, proportion_1, proportion_2]
        for i in range(3):
            axes[i].hist(list_of_proportions[i])

        plt.show()

    def draw_histogram2(self, x=1000, y=100, epsilon=0):
        result_box = []
        for i in range(x):

            for i in range(y):
                if random.uniform(0, 1) > epsilon:
                    self.update_rational()
                else:
                    self.update_irrational()

            action_profile = [self.players[i].action for i in range(self.N)]

            proportion_0 = action_profile.count(0) / float(self.N)
            proportion_1 = action_profile.count(1) / float(self.N)
            proportion_2 = action_profile.count(2) / float(self.N)

            if proportion_0 > proportion_1 and proportion_0 > proportion_2:
                result_box.append(0)
            elif proportion_1 > proportion_0 and proportion_1 > proportion_2:
                result_box.append(1)
            else:
                result_box.append(2)

            self.initialize_action_profile()

        fig, ax = plt.subplots()
        ax.hist(result_box)
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
