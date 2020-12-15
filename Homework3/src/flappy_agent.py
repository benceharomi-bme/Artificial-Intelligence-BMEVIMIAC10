from time import time

import numpy as np
np.random.seed(0)

class FlappyAgent:

    def __init__(self, observation_space_size, action_space, n_iterations):
        self.q_table = np.zeros([*observation_space_size, len(action_space)])
        self.env_action_space = action_space
        self.n_iterations = n_iterations
        self.alfa = 0.9

        self.test = False

    def step(self, state):
        action = 0
        
        if(self.q_table[state][0] >= self.q_table[state][1]):
            action = 0
        else:
            action = 1

        return action

    def epoch_end(self, epoch_reward_sum):
        if(epoch_reward_sum > 0):
            self.alfa *= 0.5

    def learn(self, old_state, action, new_state, reward):
        self.q_table[old_state][action] = self.q_table[old_state][action] + self.alfa * (reward + max(self.q_table[new_state]) - self.q_table[old_state][action])

    def train_end(self):
        self.test = True
