from abc import ABC, abstractmethod

class Agent(ABC):

    @abstractmethod
    def get_action(self, step_data):
        pass


    @abstractmethod
    def get_observation(self, step_data):
        pass

