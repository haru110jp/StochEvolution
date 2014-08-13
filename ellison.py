from __future__ import division
import numpy as np
import random

#This program is designed for the 2*2 "coordination" game



payoff = np.array([[4,0],[3,2]]) # all players share the same payoff matrix
p = 1/3 #If the proportion of players taking 1 exceeds this,other players are better off to take 1
N = 100 # the number of players
n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
actions = [0,1]

class player:
	def __init__(self,actions):
		init_action = random.choice(actions) # the initial action is randomly chosen.
		self.action = init_action
	
players = [player(actions) for i in range(N)] #list of all players in the game

def show_action_profile():
	print [players[i].action for i in range(N)]
	
def update_rational(): # function used when a player is "rational"
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
		
	if sum(nei_action) > p:   # determine the action
		players[d].action = 1
	else:
		players[d].action = 0

def update_irrational(): # function used when a player is "irrational"
	d = random.choice(range(N))
	players[d].action = random.choice(actions)
	

def play(X=10000,epsilon=0.1): # X is the number of repetition.epsilon is the possibility of a player getting "irrational"
	show_action_profile()
	for i in range(X):
		if random.uniform(0,1) > epsilon:
			update_rational()
		else:
			update_irrational()
	
	show_action_profile()




"""
HOW TO USE

when you run the code,first copy and paste the whole code on ipython notebook or something.
Second, you want to type "show_action_profile()",you can check the initial action profile.
Then you type "update()" and "show_action_profile()".This way you can set the clock one step forward
Repeat the third if necessary
"""