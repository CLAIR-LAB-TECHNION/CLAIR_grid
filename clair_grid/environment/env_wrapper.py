from abc import ABC, abstractmethod

class EnvWrapper(ABC):


    def __init__(self, env):
        self.env = env

    @abstractmethod
    def get_agent_step_data(self, step_data, agent_id):
        pass

    @abstractmethod
    def transform_actions(self, actions):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action):
        pass