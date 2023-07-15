from abc import ABC, abstractmethod
from ..utils import get_elements_order

class Coordinator(ABC):

    # init agents and the environment
    def __init__(self, env, agents, scores_and_metrics=None):
        self.env = env
        self.agents = agents
        self.scores_and_metrics = scores_and_metrics

    # how to perform the entire run
    def run(self, iteration_limit,  b_log = False):


        step_data = self.get_initial_data()

        if b_log:
            self.log_step(step_data)

        iteration_counter = 0
        done = False
        while done is not True and iteration_counter<iteration_limit:

            iteration_counter += 1
            if done:
                break

            step_data = self.run_step(step_data)

            # log relevant data
            if b_log:
                self.log_step(step_data)

            # check if done
            done = self.is_done(step_data)

    # how to perform a single iteration
    def run_step(self, step_data):

        # get actions for all agents and perform it
        joint_action = self.get_joint_action(step_data)
        step_data = self.perform_joint_action(joint_action)
        return step_data

    # activate the joint action in the environment
    def perform_joint_action(self, joint_action):
        step_data = self.env.step(joint_action)
        return step_data

    @abstractmethod
    def get_joint_action(self, previous_step_data):
        pass

    @abstractmethod
    def is_done(self, step_data) -> bool:
        pass

    def log_step(self, previous_step_data):
        pass

    def init_log_data(self):
        pass

    def get_ids(self):
        pass


class DecentralizedCoordinator(Coordinator):
    def __init__(self, env, agents, b_random_order= True):

        super().__init__(env, agents)

        self.b_random_order = b_random_order


    def get_joint_action(self, previous_step_data):

        """
        Compute the joint action.
        """
        agents_ids = self.get_ids()
        agents_order = get_elements_order(self.b_random_order, agents_ids)

        # returning a dictionary of actions to be performed by each agent
        actions = {}
        for agent_id in agents_order:
            agent = self.agents[agent_id]
            agent_step_data = self.get_agent_step_data(previous_step_data, agent_id)
            action = agent.get_action(agent_step_data)
            actions[agent_id] = action

        return self.transform_actions(actions)

    @abstractmethod
    def get_agent_step_data(self, step_data, agent_id):
        pass

    #used to adapt the action list format to the specific domain
    def transform_actions(self, actions):
        return actions


class CentralizedCoordinator(Coordinator):
    def __init__(self, env, agents, central_agent):

        super().__init__(env, agents)
        self.central_agent = central_agent


    def get_joint_action(self, previous_step_data):

        # returning a dictionary of actions to be performed by each agent
        joint_action = self.central_agent.get_action(previous_step_data)

        return joint_action

