from clair_grid.agents.sg_random_agent import ESRandomAgent, CentralESRandomAgent
from clair_grid.coordination.sg_coordinator import SGDecentralizedCoordinator, SGCentralizedCoordinator, SGDecentralizedWithComCoordinator

from citylearn.citylearn import CityLearnEnv
from citylearn.reward_function import SolarPenaltyReward
from clair_grid.environment.citylearn_wrapper import CityLearnWrapper

from clair_grid.evaluation import run_training, run_evaluation

def dummy_step_evaluation_func(env_wrapper, step_data, joint_action)->dict:
    step_eval = {}
    step_eval["comfort"] = 5
    step_eval["CO2"] = -3
    return step_eval

def dummy_agg_evaluation_func(evaluation_data:dict):
    total_scores = {}
    for iteration in evaluation_data:
        iteration_data = evaluation_data[iteration]
        for score_key in iteration_data:
            if not score_key in total_scores.keys():
                total_scores[score_key] = 0
            total_scores[score_key]+=iteration_data[score_key]
    return total_scores
def dummy_com_signal_generator(env_wrapper, step_data):
    return "test"


def run_training_and_evaluation_decenralized():

    # create the environment
    dataset_name = 'citylearn_challenge_2022_phase_1'
    env = CityLearnEnv(dataset_name)
    env.reward_function = SolarPenaltyReward(env)
    env_wrapper = CityLearnWrapper(env)

    # create the agents
    num_of_agents = len(env.buildings)
    agents = {}
    agent_ids= range(1, num_of_agents+1)
    for agent_id in  agent_ids:
        agent = ESRandomAgent(agent_id)
        agents[agent_id] = agent

    # initialize the coodinator
    b_random_order = False
    coordinator = SGDecentralizedCoordinator(env_wrapper, agents, agent_ids, b_random_order)

    # run training
    coordinator.run(100, b_log=True, b_train = True, b_evaluate=False)


    # run evaluation
    return coordinator.run(100, b_log=True, b_train = False, b_evaluate=True, step_evaluation_func=dummy_step_evaluation_func, agg_evaluation_func=dummy_agg_evaluation_func)


def run_evaluation_decenralized():

    # create the environment
    dataset_name = 'citylearn_challenge_2022_phase_1'
    env = CityLearnEnv(dataset_name)
    env.reward_function = SolarPenaltyReward(env)
    env_wrapper = CityLearnWrapper(env)

    # create the agents
    num_of_agents = len(env.buildings)
    agents = {}
    agent_ids= range(1, num_of_agents+1)
    for agent_id in  agent_ids:
        agent = ESRandomAgent(agent_id)
        agents[agent_id] = agent

    # initialize the coodinator
    b_random_order = False
    coordinator = SGDecentralizedCoordinator(env_wrapper, agents, agent_ids, b_random_order)

    # run evaluation
    return coordinator.run(100, b_log=True, b_train = True, b_evaluate=True, step_evaluation_func=dummy_step_evaluation_func, agg_evaluation_func=dummy_agg_evaluation_func)

def run_evaluation_cenralized():

    # create the environment
    dataset_name = 'citylearn_challenge_2022_phase_1'
    env = CityLearnEnv(dataset_name)
    env_wrapper = CityLearnWrapper(env)

    # create the agents
    num_of_agents = len(env.buildings)
    agents = {}
    agent_ids= range(1, num_of_agents+1)
    for agent_id in agent_ids:
        agent = ESRandomAgent(agent_id)
        agents[agent_id] = agent

    central_agent = CentralESRandomAgent(agent_ids)

    # initialize the coodinator
    coordinator = SGCentralizedCoordinator(env_wrapper, agents, agent_ids, central_agent)

    # run evaluation
    return coordinator.run(100, b_log=True, b_train = True, b_evaluate=True, step_evaluation_func=dummy_step_evaluation_func, agg_evaluation_func=dummy_agg_evaluation_func)


def run_evaluation_decenralized_with_com():

    # create the environment
    dataset_name = 'citylearn_challenge_2022_phase_1'
    env = CityLearnEnv(dataset_name)
    env.reward_function = SolarPenaltyReward(env)
    env_wrapper = CityLearnWrapper(env)

    # create the agents
    num_of_agents = len(env.buildings)
    agents = {}
    agent_ids= range(1, num_of_agents+1)
    for agent_id in  agent_ids:
        agent = ESRandomAgent(agent_id)
        agents[agent_id] = agent

    # initialize the coodinator
    b_random_order = False
    coordinator = SGDecentralizedWithComCoordinator(env_wrapper, agents, agent_ids, b_random_order, dummy_com_signal_generator)

    # run evaluation
    return coordinator.run(100, b_log=True, b_train = True, b_evaluate=True, step_evaluation_func=dummy_step_evaluation_func, agg_evaluation_func=dummy_agg_evaluation_func)

def test_run_training_and_evaluation():

    # create the environment
    dataset_name = 'citylearn_challenge_2022_phase_1'
    env = CityLearnEnv(dataset_name)
    env.reward_function = SolarPenaltyReward(env)
    env_wrapper = CityLearnWrapper(env)

    # create the agents
    num_of_agents = len(env.buildings)
    agents = {}
    agent_ids= range(1, num_of_agents+1)
    for agent_id in  agent_ids:
        agent = ESRandomAgent(agent_id)
        agents[agent_id] = agent

    # initialize the coodinator
    b_random_order = False
    coordinator = SGDecentralizedWithComCoordinator(env_wrapper, agents, agent_ids, b_random_order, dummy_com_signal_generator)

    run_training(coordinator, 1000, False)

    return run_evaluation(coordinator, 1000, True, step_evaluation_func=dummy_step_evaluation_func, agg_evaluation_func=dummy_agg_evaluation_func)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("running decentralized")
    print(run_evaluation_decenralized())
    print("running centralized")
    print(run_evaluation_cenralized())
    print("running decenralized with com")
    print(run_evaluation_decenralized_with_com())

    print("running test_run_training_and_evaluation")
    print(test_run_training_and_evaluation())

