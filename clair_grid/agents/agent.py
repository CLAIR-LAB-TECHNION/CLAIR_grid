from abc import ABC

class Agent(ABC):

    def __init__(self):
      pass

class TempAgent(Agent):
    def __init__(self):
      a=5

    def init_agent(self):
      a=5
    def set_action_space(self, agent_id, action_space):
        """
        Set the agent's action space and init the agent.
        Args:
            agent_id: The ID of the agent (int - # building).
            action_space: the action space of the # agent.

        Returns:

        """
        self.action_space[agent_id] = action_space
        self.agent_id = agent_id
        self.init_agent()

