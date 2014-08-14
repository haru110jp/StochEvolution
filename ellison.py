from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import random

#This program is designed for the 2*2 "coordination" game



payoff = np.array([[4,0],[3,2]]) # all players share the same payoff matrix
p = 1/3 #If the proportion of players taking 1 exceeds this,other players are better off to take 1
N = 10 # the number of players
n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
actions = [0,1]

class player:
	def __init__(self,actions):
		self.init_action()
	
	def init_action(self):
		self.action = random.choice(actions) # the initial action is randomly chosen.

players = [player(actions) for i in range(N)] #list of aldrl players in the game.

def show_action_profile(players):
	print [players[i].action for i in range(N)]
	
def update_rational(players): # function used when a player is "rational"
	# pick a player which can change the action
	d = random.choice(range(N))
	nei_numbers = [] # contains the number assigned to each neighbor
	nei_numbers_with_large_small = [i for i in range(-n,n+1)] # contains the chosen player,may contain inappropriate numbers
	del nei_numbers_with_large_small[n] #delete the chosen player
	for i in nei_numbers_with_large_small:
		if i < 0:
			i = i + N

		if i >= N:
			i = i - N

		nei_numbers.append(i)
			
	nei_action = [players[i].action for i in nei_numbers] # neighbors' action profile
		
	if sum(nei_action) > p:   # determine the action so that it is a best response to the action profile of the community
		players[d].action = 1
	else:
		players[d].action = 0

def update_irrational(players): # function used when a player is "irrational"
	d = random.choice(range(N))
	players[d].action = random.choice(actions) # action is randomly chosen because he is irrational
	

def play(players,X=10000,epsilon=0.1): # X is the number of repetition.epsilon is the possibility of a player getting "irrational"
	show_action_profile(players) #show the initial action profile
	for i in range(X):
		if random.uniform(0,1) > epsilon:
			update_rational()
		else:
			update_irrational()
	
	show_action_profile(players) # show the action profile at the end of the game

def reset(players): # after using "play" you wanna use this to initialize the action profile
	for i in players:
		i.init_action()

def draw_histogram(players,X=100,Y=10,epsilon=0.01): # The set of X games are played Y times.
	state_list =[] # "state" is the number of players taking 1 devided by N
	action_profile = [players[i].action for i in range(N)]
	state_list.append(sum(action_profile) / N) #added the initial state
	
	for i in range(X):
		if random.uniform(0,1) > epsilon:
			update_rational(players)
		else:
			update_irrational(players)
		
		action_profile = [players[i].action for i in range(N)]
		state_list.append(sum(action_profile) / N)
		
	fig, axes = plt.subplots()
	axes.hist(state_list)
	
	plt.show()
				
				




"""
HOW TO USE

when you run the code,first copy and paste the whole code on ipython notebook or something.
Then you use "play(players)" You can see action profile of the start and the end at the same time.
Type "reset(players)" if you wanna continue
"""