"""
Simple Markov Chain.
"""
from random import random


class Markov:
    def __init__(self, p1, p2, state1=0, state2=1):
        self.p1 = p1
        self.p2 = p2
        self.state1 = state1
        self.state2 = state2
        self.current_state = state1

    def __call__(self):
        p = random()
        if self.current_state == self.state1:
            if p > self.p1:
                self.current_state = self.state2
        else:
            if p > self.p2:
                self.current_state = self.state1
        return self.current_state

    def reset(self):
        self.current_state = self.state1
