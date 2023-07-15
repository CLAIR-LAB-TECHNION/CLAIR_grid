import random

from .agent import Agent

class ESRandomAgent(Agent):

    def __init__(self, agent_id):
      self.agent_id = agent_id

    def get_id(self):
        return self.agent_id

    def get_action(self, step_data):
        action = random.uniform(-1, 1)
        return action

    def get_observation(self, step_data):
        return step_data

class CentralESRandomAgent(Agent):

    def __init__(self, agent_ids):
      self.agent_ids = agent_ids

    def get_action(self, step_data):

        joint_action = {}
        for agent_id in self.agent_ids:
            action = random.uniform(-1, 1)
            joint_action[agent_id] = action

        return joint_action

    def get_observation(self, step_data):
        return step_data