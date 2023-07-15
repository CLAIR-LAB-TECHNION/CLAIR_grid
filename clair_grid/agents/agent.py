from abc import ABC, abstractmethod

class Agent(ABC):

    def __init__(self, agent_id):
      self.agent_id = agent_id

    def get_id(self):
        return self.agent_id

    @abstractmethod
    def get_action(self, previous_step_data):
        pass
