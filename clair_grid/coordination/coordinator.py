from abc import ABC, abstractmethod
from ..utils import get_elements_order

class Coordinator(ABC):

    # init agents and the environment

    def __init__(self, env_wrapper, agents:dict):
        self.env_wrapper = env_wrapper
        self.agents = agents
        self.evalulation_log = None

    # how to perform the entire run
    def run(self, iteration_limit, b_log = False, b_train = False, b_evaluate=False, step_evaluation_func= None, agg_evaluation_func= None):

        step_data = self.get_initial_data()

        if b_log:
            self.log_step(step_data)
        if b_evaluate:
            evaluation_data = {}

        iteration_counter = 0
        done = False
        while done is not True and iteration_counter<iteration_limit:

            iteration_counter += 1
            if done:
                break

            [step_data, joint_action] = self.run_step(step_data)

            # log relevant data
            if b_log:
                self.log_step(step_data)

            # evaluate performance
            if step_evaluation_func:
                evaluation_data[iteration_counter]=self.evaluate_step(step_evaluation_func, step_data, joint_action)

            # if the agent is training, update its policy
            if b_train:
                self.perform_training_step(step_data, joint_action)

            # check if done
            done = self.is_done(step_data)

        # after training is done - evaluate performance
        if b_evaluate:
            return self.evaluate_agg(agg_evaluation_func, evaluation_data)
        else:
            return None

    # how to perform a single iteration
    def run_step(self, step_data):

        # get actions for all agents and perform it
        joint_action = self.get_joint_action(step_data)
        step_data = self.perform_joint_action(joint_action)
        return [step_data,joint_action]

    # activate the joint action in the environment
    def perform_joint_action(self, joint_action):
        step_data = self.env_wrapper.step(joint_action)
        return step_data

    def evaluate_step(self, evaluation_func, step_data, joint_action)->dict:
        return evaluation_func(self.env_wrapper, step_data, joint_action)

    def evaluate_agg(self, evaluation_func, evaluation_data)->dict:
        return evaluation_func(evaluation_data)

    def perform_training_step(self, step_data, joint_action):
        pass

    @abstractmethod
    def get_joint_action(self, step_data):
        pass

    @abstractmethod
    def is_done(self, step_data) -> bool:
        pass

    def log_step(self, step_data):
        pass

    def init_log_data(self):
        pass

    def get_ids(self):
        pass


class DecentralizedCoordinator(Coordinator):
    def __init__(self, env, agents, b_random_order= True):

        super().__init__(env, agents)

        self.b_random_order = b_random_order


    def get_joint_action(self, step_data):

        """
        Compute the joint action.
        """
        agents_ids = self.get_ids()
        agents_order = get_elements_order(self.b_random_order, agents_ids)

        # returning a dictionary of actions to be performed by each agent
        actions = {}
        for agent_id in agents_order:
            agent = self.agents[agent_id]
            agent_step_data = agent.get_observation((self.env_wrapper).get_agent_step_data(step_data, agent_id))
            action = agent.get_action(agent_step_data)
            actions[agent_id] = action

        return self.env_wrapper.transform_action_dict_to_env_format(actions)


    def perform_training_step(self, step_data, joint_action):

        joint_action = self.env_wrapper.transform_action_env_format_to_dict(joint_action)
        for agent_id in self.get_ids():
            agent_action = joint_action[agent_id]
            agent_step_data = self.agents[agent_id].get_observation((self.env_wrapper).get_agent_step_data(step_data, agent_id))
            self.agents[agent_id].perform_training_step(agent_action, agent_step_data)


class CentralizedCoordinator(Coordinator):
    def __init__(self, env, agents, central_agent):

        super().__init__(env, agents)
        self.central_agent = central_agent

    def get_joint_action(self, step_data):

        # get the agent's observation
        step_data= self.central_agent.get_observation(step_data)

        # returning a dictionary of actions to be performed by each agent
        joint_action = self.central_agent.get_action(step_data)

        joint_action = self.env_wrapper.transform_action_dict_to_env_format(joint_action)

        return joint_action

    def perform_training_step(self, step_data, joint_action):
        self.central_agent.perform_training_step(step_data, joint_action)



class DecentralizedWithComCoordinator(DecentralizedCoordinator):
    def __init__(self, env, agents, b_random_order= True):

        super().__init__(env, agents, b_random_order)


    def get_joint_action(self, step_data):

        """
        Compute the joint action.
        """
        agents_ids = self.get_ids()
        agents_order = get_elements_order(self.b_random_order, agents_ids)

        signal = self.get_shared_com_signal(step_data)

        # returning a dictionary of actions to be performed by each agent
        actions = {}
        for agent_id in agents_order:
            agent = self.agents[agent_id]
            agent_step_data = agent.get_observation((self.env_wrapper).get_agent_step_data(step_data, agent_id))
            agent_step_data = [agent_step_data, signal]
            action = agent.get_action(agent_step_data)
            actions[agent_id] = action

        return self.env_wrapper.transform_action_dict_to_env_format(actions)


    @abstractmethod
    def get_shared_com_signal(self, step_data):
        pass
