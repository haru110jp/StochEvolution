"""
This program is designed for the 2*2 "coordination" game
payoff = np.array([[4,0],[3,2]]) # all players share the same payoff matrix
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import random


class Player:
	def __init__(self):
		self.init_action()
	
	def init_action(self):
		actions = [0,1]
		self.action = random.choice(actions) # the initial action is randomly chosen.


class ellison22_coordination(Player): #This class "inherits" the class "Player" defined above
	def __init__(self,actions=[0,1],p=1/3,N=10,n=1):
		self.players = [Player() for i in range(N)]	#"players" is a list consisting of "player" 
		self.p = p
		self.N = N
		self.n = n
		self.actions = actions
	"""	
	<Arguments>
	p = 1/3 #If the proportion of players taking 1 exceeds this,other players are better off to take 1
	N = 10 # the number of players
	n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
	actions = [0,1]		#this is 2*2 game and there are strategy 0 and 1
	"""


	def show_action_profile(self):
		print [self.players[i].action for i in range(self.N)]
	
	def update_rational(self): # function used when a player is "rational"
		# pick a player which can change the action
		d = random.choice(range(self.N))
		nei_numbers = [] # contains the number assigned to each neighbor
		nei_numbers_with_large_small = [i for i in range( -self.n , self.n+1)] # contains the chosen player,may contain inappropriate numbers
		del nei_numbers_with_large_small[self.n] #delete the chosen player
		
		for i in nei_numbers_with_large_small:
			if i < 0:
				i = i + self.N

			if i >= self.N:
				i = i - self.N

			nei_numbers.append(i)
			
		nei_action = [self.players[i].action for i in nei_numbers] # neighbors' action profile
		
		if sum(nei_action) > self.p:   # determine the action so that it is the best response to the action profile of the community
			self.players[d].action = 1
		else:
			self.players[d].action = 0

	def update_irrational(self): # function used when a player is "irrational"
		d = random.choice(range(self.N))
		self.players[d].action = random.choice(self.actions) # action is randomly chosen because he is irrational
	

	def play(self,X=10000,epsilon=0.01): # X is the number of repetition.epsilon is the possibility of a player getting "irrational"
		self.show_action_profile() #show the initial action profile
		for i in range(X):
			if random.uniform(0,1) > epsilon:
				self.update_rational() #the argument "update_rational" takes is the list "players" the function "play" takes.
			else:    # it is confusing because the same name is used for both.I should make it clearer
				self.update_irrational()
	
		self.show_action_profile() # show the action profile at the end of the game

	def reset(self): # after using "play" you wanna use this to initialize the action profile
		for i in self.players:
			i.init_action()

	def draw_histogram(self,X=100,epsilon=0.01): # draws a histogram about the state dynamics during the game.
 		state_list =[] # "state" is the number of players taking 1 devided by N
		action_profile = [self.players[i].action for i in range(self.N)]
		state_list.append(sum(action_profile) / float(self.N)) #added the initial state
	
		for i in range(X):
			if random.uniform(0,1) > epsilon:
				self.update_rational()
			else:
				self.update_irrational()
		
			action_profile = [self.players[i].action for i in range(self.N)]
			state_list.append(sum(action_profile) / float(self.N))
		
		fig, ax = plt.subplots()
		ax.hist(state_list)
	
		plt.show()
	
	def draw_graph(self,X=100,epsilon=0.01): #draws a graph which represents the state dynamics during the game
		state_list =[] # "state" is the number of players taking 1 devided by N
		action_profile = [self.players[i].action for i in range(self.N)]
		state_list.append(sum(action_profile) / float(self.N)) #added the initial state
	
		for i in range(X):
			if random.uniform(0,1) > epsilon:
				self.update_rational()
			else:
				self.update_irrational()
		
			action_profile = [self.players[i].action for i in range(self.N)]
			state_list.append(sum(action_profile) / float(self.N))
				
		fig, ax = plt.subplots()
		ax.plot(state_list,label='state')
		ax.legend(bbox_to_anchor=(1.05, 0), loc='best', borderaxespad=0) 
	
		plt.show()
		