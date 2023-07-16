from clair_grid.coordination import coordinator

def run_training(coordinator, num_of_iterations, b_log):
    # run training
    coordinator.run(num_of_iterations, b_log, b_train = True, b_evaluate=False)


def run_evaluation(coordinator, num_of_iterations, b_log, step_evaluation_func, agg_evaluation_func):
    # run evaluation
    return coordinator.run(num_of_iterations, b_log, b_train = False, b_evaluate=True, step_evaluation_func=step_evaluation_func, agg_evaluation_func=agg_evaluation_func)
