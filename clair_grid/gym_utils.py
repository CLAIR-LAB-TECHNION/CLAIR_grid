from gym.spaces.box import Box

def dict_to_box(x):
    """
    Transforms a dictionary space into a Gym's Box space
    :param x: a dictionary space
    :return: Box space
    """
    return Box(low=x["low"], high=x["high"], shape=(x["shape"]), dtype=x["dtype"])