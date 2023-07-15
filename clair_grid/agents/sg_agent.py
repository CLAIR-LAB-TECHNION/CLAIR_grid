import random

from .agent import Agent

class SGAgent(Agent):
    def get_action(self, previous_step_data):
        action = random.uniform(-1, 1)
        return action

