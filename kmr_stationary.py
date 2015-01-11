from __future__ import division
import random
from math import factorial
import numpy as np
from gth_solve import gth_solve

def cool_lex(s, t):
    """
    This function implements the algorithm which arranges 0s and 1s.
    Reference : "The Coolest Way to Generate combinations"

    s : int 
        The number of 0s

    t : int
        The number of 1s
    """
    zeros = ""
    ones = ""
    states = []
    for i in range(s):
        zeros = zeros + "0"
    for i in range(t):
        ones = ones + "1"

    current_state = ones + zeros
    states.append(current_state)
    num_repetition = int(factorial(s + t) / (factorial(s)*factorial(t)) - 1)

    for i in range(num_repetition):
        a = current_state.find("010")
        b = current_state.find("011")

        if a == b == -1:
            current_state = current_state[-1] + current_state[0:-1]
            states.append(current_state)

        elif a != -1 and b == -1:
            rotation_before = current_state[:a + 3]
            residual = current_state[a + 3:]
            rotation_after = rotation_before[-1] + rotation_before[0:-1]
            current_state = rotation_after + residual
            states.append(current_state)

        elif a == -1 and b != -1:
            rotation_before = current_state[:b + 3]
            residual = current_state[b + 3:]
            rotation_after = rotation_before[-1] + rotation_before[0:-1]
            current_state = rotation_after + residual
            states.append(current_state)

        elif a != -1 and b != -1 and a < b:
            rotation_before = current_state[:a + 3]
            residual = current_state[a + 3:]
            rotation_after = rotation_before[-1] + rotation_before[0:-1]
            current_state = rotation_after + residual
            states.append(current_state)
            
        elif a != -1 and b != -1 and a > b:
            rotation_before = current_state[:b + 3]
            residual = current_state[b + 3:]
            rotation_after = rotation_before[-1] + rotation_before[0:-1]
            current_state = rotation_after + residual
            states.append(current_state)
            
    return states

def kmr_compute_stationary(n, epsilon=0.01, payoffs=[[6, 0, 0], [5, 7, 5], [0, 5, 8]]):
    """
    This function calculates the stationary state of KMR in genetal cases.
    n : int 
        The number of Players
    epsilon : float
        The probability of mutation
    Payoffs : list
        The payoff matrix(symmetric)
    """
    num_action = len(payoffs)
    states_cool_lex = cool_lex(n, num_action-1)
    states = []
    num_zeros = n
    num_ones = num_action -1
    num_states = int(factorial(num_zeros + num_ones) / (factorial(num_zeros)*factorial(num_ones)))
    tran_matrix = np.zeros([num_states, num_states])
    print states_cool_lex
    for i in states_cool_lex:
        profile = []
        for m, n in enumerate(i.split("1")):
            profile.append(len(n))
        states.append(profile) # ex. [nparray([0,2,0,1,0]), ...]

    for s, i in enumerate(states):
        current_profile = np.array(i) / sum(i)
        expected_payoff = np.dot(payoffs, current_profile)
        best_reply = expected_payoff.argmax()
        state_no_before = s
        for m, n in enumerate(i):
            if n != 0: # The player may be chosen
                for k in range(num_action):
                    adjacent_state = list(i)
                    adjacent_state[m] = adjacent_state[m] - 1
                    adjacent_state[k] = adjacent_state[k] + 1
                    state_no_after = states.index(adjacent_state)
                    if k == best_reply:
                        tran_matrix[state_no_before][state_no_after] = 1 - epsilon*(1 - 1/float(num_action))
                    else:
                        tran_matrix[state_no_before][state_no_after] = epsilon * (1/float(num_action))
    print tran_matrix
    return gth_solve(tran_matrix)