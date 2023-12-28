# This file contains the options that you should modify to solve Question 2

def question2_1():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": 0
    }


def question2_2():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,
        "discount_factor": 0.2,
        "living_reward": 0.5
    }


def question2_3():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -0.1
    }

#For question2_4, we want the policy to seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state).
def question2_4():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,
        "discount_factor": 0.99,
        "living_reward": 0.05
    }


def question2_5():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 100
    }


def question2_6():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100
    }
