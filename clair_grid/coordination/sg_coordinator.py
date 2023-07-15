from .coordinator import DecentralizedCoordinator, CentralizedCoordinator

class SGDecentralizedCoordinator(DecentralizedCoordinator):

    def __init__(self, env, agents, b_random_order=True):
        super().__init__(env, agents, b_random_order)
        # agent id's in the environment start with 1
        self.agent_ids = [*range(1, len(self.agents)+1)]
        self.init_joint_action = [[0.0]]*len(self.agents)


    def get_agent_step_data(self, step_data, agent_id):
        print(step_data)
        # agent id's start at 1 and are stored according to order in a list
        [observations, reward, done, info] = step_data
        agent_step_data = [observations[agent_id - 1], reward, done]
        return agent_step_data

    def get_initial_data(self):
        joint_observation = self.env.reset()
        step_data = self.env.step(self.init_joint_action)
        return step_data

    def is_done(self, step_data) -> bool:
        return False

    def get_ids(self):
        return self.agent_ids

    def transform_actions(self, actions):

        # transform the dictionary to an ordered list
        action_list = [None]*len(actions)
        for agent_id in actions.keys():
            action_list[agent_id-1] = [actions[agent_id]]

        print(action_list)
        return action_list