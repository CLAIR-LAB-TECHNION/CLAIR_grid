from .env_wrapper import EnvWrapper
class CityLearnWrapper(EnvWrapper):

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def get_agent_step_data(self, step_data, agent_id):
        # agent id's start at 1 and are stored according to order in a list
        [observations, rewards, done, info] = step_data
        agent_step_data = [observations[agent_id - 1], rewards[agent_id - 1], done]
        return agent_step_data


    def transform_actions(self, actions):
        # transform the dictionary to an ordered list
        action_list = [None] * len(actions)
        for agent_id in actions.keys():
            action_list[agent_id - 1] = [actions[agent_id]]

        return action_list
