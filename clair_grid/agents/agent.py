from abc import ABC, abstractmethod

class Agent(ABC):

    @abstractmethod
    def get_action(self, step_data):
        pass


    @abstractmethod
    def get_observation(self, step_data):
        pass

    def perform_training_step(self, action, step_data):
        pass
