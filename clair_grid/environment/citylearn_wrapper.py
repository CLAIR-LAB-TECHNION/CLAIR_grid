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

    def transform_action_dict_to_env_format(self, actions:dict):
        action_list = [None] * len(actions)
        for agent_id in actions.keys():
            action_list[agent_id - 1] = [actions[agent_id]]

        return action_list

    def transform_action_env_format_to_dict(self, actions) -> dict:
        action_dict = {}
        for agent_index in range(0,len(actions)):
            agent_id = agent_index+1
            action_dict[agent_id] = actions[agent_index]

        return action_dict

    def is_done(self, step_data):
        done = step_data[2]
        return done

    def get_kpi_value(self, kpi_index, agent_index = None):
        pass




