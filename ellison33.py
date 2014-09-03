# this program is designed for 3*3 games

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import random


class Player:
    def __init__(self):
	    self.init_action()
	
    def init_action(self):
        actions = [0,1,2]
        self.action = random.choice(actions) # the initial action is randomly chosen.


class ellison33(Player): #This class "inherits" the class "Player" defined above
    def __init__(self,N=10,n=1,payoffs=[[[6,6],[0,5],[0,0]],[[5,0],[7,7],[5,5]],[[0,0],[5,5],[8,8]]]):
        """
        payoffs takes the form of "the list of the lists containing lists"
        the default payoffs are those of "3*3 coordination games"
        
        N = 10 # the number of players
        n = 1 # the number of neighbors on one side.it is 2 in total when n = 1
        """
        self.players = [Player() for i in range(N)]	#"players" is a list consisting of "player" 
        self.N = N
        self.n = n
        self.payoff_0 = np.array(payoffs[0]) #possible payoffs if a player takes 0 
        self.payoff_1 = np.array(payoffs[1])
        self.payoff_2 = np.array(payoffs[2])
        self.actions = [0,1,2]
        
        

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
        
        #computing the ratio of players taking a certain action in the neighborhood
        proportion_of_0 = sum(0 == k for k in nei_action)
        proportion_of_1 = sum(1 == k for k in nei_action)
        proportion_of_2 = 1 - proportion_of_0 - proportion_of_1
        
        action_profile = np.array([proportion_of_0,proportion_of_1,proportion_of_2])
        
        #computing the expected payoff of each action
        ev0 = np.dot(action_profile,self.payoff_0)
        ev1 = np.dot(action_profile,self.payoff_1)
        ev2 = np.dot(action_profile,self.payoff_2)
        
        # determine the action so that it is the best response to the action profile of the community
        if ev0[0] >= ev1[0] and ev0[0] >= ev2[0]:
            self.players[d].action = 0
        
        elif ev1[0] >= ev0[0] and ev1[0] > ev2[0]:
            self.players[d].action = 1
        
        else:
            self.players[d].action = 2
        
        
        
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


#ここまで3*3で動作確認済み。ここからはまた改定します。（2014 9/3）



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
