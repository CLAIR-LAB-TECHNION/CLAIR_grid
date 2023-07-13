import time
from citylearn.citylearn import CityLearnEnv
from .utils import action_space_to_dict



# Reset the environment and create the observation dictionary with all environment info
def env_reset(env):
    observations = env.reset()
    action_space = env.action_space
    observation_space = env.observation_space
    building_info = env.get_building_information()
    action_space_dicts = [action_space_to_dict(asp) for asp in action_space]
    observation_space_dicts = [action_space_to_dict(osp) for osp in observation_space]
    obs_dict = {"action_space": action_space_dicts,
                "observation_space": observation_space_dicts,
                "building_info": building_info,
                "observation": observations}
    return obs_dict

#TODO: change name
def evaluate(CoordinatorClass, AgentClass, eval_constants, verbose=True):

    # init timer
    print("Starting evaluation")
    start_time = time.process_time()

    # Create a CityLearn environment
    env = CityLearnEnv(schema=eval_constants.schema_path)

    # Reset the environment
    obs_dict = env_reset(env)
    observations = obs_dict["observation"]

    # Add coordinator
    rb_coordinator = CoordinatorClass(AgentClass, obs_dict, **eval_constants.rule_based_params)

    # Init local variables
    episodes_completed = 0
    num_steps = 0
    episode_metrics = []

    '''
    # Define the agents' training time
    evaluation_steps = 24 * eval_constants.evaluation_days
    done = False

    # Start the evaluation process
    while True:
        num_steps += 1

        # Take an action
        actions = rb_coordinator.compute_action(observations)

        # Step the environment and collect the observation, reward (user written reward), done and info
        observations_, rewards, done, info = env.step(actions)

        # step the observation
        observations = observations_

        # collect rewards and compute scores and average scores
        rb_coordinator.collect_scores(rewards)

        if num_steps % eval_constants.compute_metric_interval == 0:
            # evaluate the agents
            metrics_t = env.evaluate()

            # collect the metrics
            rb_coordinator.collect_metrics(metrics_t)

            # print scores and metrics
            if verbose:
                rb_coordinator.print_scores_and_metrics(episodes_completed, num_steps)

        # evaluate the last episode and reset the environment
        if done:
            episodes_completed += 1
            metrics_t = env.evaluate()
            metrics = {"price_cost": metrics_t[0],
                       "emission_cost": metrics_t[1],
                       "grid_cost": metrics_t[2]}
            if np.any(np.isnan(metrics_t)):
                raise ValueError("Episode metrics are nan, please contant organizers")
            episode_metrics.append(metrics)
            print(f"Episode complete: {episodes_completed} | Latest episode metrics: {metrics}", )

            # compute average scores
            rb_coordinator.compute_avg_scores()

            # Reset the environment
            done = False
            obs_dict = env_reset(env)
            rb_coordinator.init_score()
            rb_coordinator.reset_battery()
            observations = obs_dict["observation"]

        # terminate evaluation
        if num_steps == evaluation_steps:
            print(f"Evaluation process is terminated after {num_steps} steps.")
            break

    # print the episode mean evaluation score
    if len(episode_metrics) > 0:
        print("Average Price Cost:", np.mean([e['price_cost'] for e in episode_metrics]))
        print("Average Emission Cost:", np.mean([e['emission_cost'] for e in episode_metrics]))
        print("Average Grid Cost:", np.mean([e['grid_cost'] for e in episode_metrics]))
        for e in episode_metrics:
            print(f"Episode Utility: {np.mean(list(e.values()))}")
    return env, rb_coordinator, episode_metrics, time.process_time() - start_time
    '''
