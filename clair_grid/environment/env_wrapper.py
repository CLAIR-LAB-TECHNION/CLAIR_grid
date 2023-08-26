from abc import ABC, abstractmethod

class EnvWrapper(ABC):


    def __init__(self, env):
        self.env = env

    @abstractmethod
    def get_agent_step_data(self, step_data, agent_id):
        pass

    def transform_action_dict_to_env_format(self, actions:dict):
        pass

    def transform_action_env_format_to_dict(self, actions) -> dict:
        pass


    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action):
        pass
    @abstractmethod
    def is_done(self, step_data):
        pass