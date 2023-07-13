class EvalConstants:
    # Environmental and simulation parameters
    episodes = 1
    compute_metric_interval = 100
    schema_path = "C:\\Users\\sarahk\\PycharmProjects\\CityLearn\\citylearn\\data\\citylearn_challenge_2022_phase_all\\schema.json"
    #./data/citylearn_challenge_2022_phase_1/schema.json'
    evaluation_days = episodes * 20

    # Controller and agents' parameters
    rule_based_params = {"search_depths": [0, 1, 2, 4],
                         "max_search_time": 0.2,
                         "d_action": 0.2,
                         "utility_weighting": (1., 1., 1., 1.),
                         "random_order": False,
                         "action_space_list": None,     # [0, -0.05, 0.05, -0.1, 0.1, -0.3, 0.3, -1, 1]
                         "prediction_method": "IDX",
                         "agent_type": "RB-local",             # ("RB-local", "PLAN-local")
                         "last_agent_type": "RB-local",      # ("RB-local", "RB-global", "PLAN-local", "PLAN-global")
                        }

def action_space_to_dict(action_space):
    """ Only for box space """
    return {"high": action_space.high,
            "low": action_space.low,
            "shape": action_space.shape,
            "dtype": str(action_space.dtype)
            }
