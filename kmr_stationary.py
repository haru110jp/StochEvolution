from __future__ import division
import random
from math import factorial
import numpy as np

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