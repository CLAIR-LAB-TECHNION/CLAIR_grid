from .coordinator import DecentralizedCoordinator, CentralizedCoordinator, DecentralizedWithComCoordinator

class SGDecentralizedCoordinator(DecentralizedCoordinator):

    def __init__(self, env_wrapper, agents, agent_ids, b_random_order=True):
        super().__init__(env_wrapper, agents, b_random_order)
        # agent id's in the environment start with 1
        self.agent_ids = agent_ids
        self.init_joint_action = [[0.0]]*len(self.agents)

    def get_ids(self):
        return self.agent_ids
    def get_initial_data(self):
        joint_observation = self.env_wrapper.reset()
        step_data = self.env_wrapper.step(self.init_joint_action)
        return step_data

    def is_done(self, step_data) -> bool:
        return False




class SGCentralizedCoordinator(CentralizedCoordinator):

    def __init__(self, env_wrapper, agents, agent_ids, central_agent):
        super().__init__(env_wrapper, agents, central_agent)

        self.agent_ids = agent_ids
        # note that agent id's in the environment start with 1
        self.init_joint_action = [[0.0]]*len(self.agents)

    def get_ids(self):
        return self.agent_ids
    def get_initial_data(self):
        joint_observation = self.env_wrapper.reset()
        step_data = self.env_wrapper.step(self.init_joint_action)
        return step_data

    def is_done(self, step_data) -> bool:
        return False


class SGDecentralizedWithComCoordinator(DecentralizedWithComCoordinator):

    def __init__(self, env_wrapper, agents, agent_ids, b_random_order=True, com_signal_generator=None):
        super().__init__(env_wrapper, agents, b_random_order)
        # agent id's in the environment start with 1
        self.agent_ids = agent_ids
        self.init_joint_action = [[0.0]]*len(self.agents)
        self.com_signal_generator = com_signal_generator

    def get_ids(self):
        return self.agent_ids
    def get_initial_data(self):
        joint_observation = self.env_wrapper.reset()
        step_data = self.env_wrapper.step(self.init_joint_action)
        return step_data

    def is_done(self, step_data) -> bool:
        return False

    def get_shared_com_signal(self, step_data):

        if self.com_signal_generator:
            return self.com_signal_generator(self.env_wrapper, step_data)
        else:
            print("no signal generator is defined - null signal emmitted")
            return None
