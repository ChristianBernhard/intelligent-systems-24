import gym
import numpy as np


counter = 0
bestReward = 0
bestActionSeq = []

def oracle(actionSeq, n_calls=1000):

    global counter, bestReward, bestActionSeq

    env = gym.make('CartPole-v1')
    _, _ = env.reset(seed=0)
    sumRewards = 0
    for action in actionSeq:
        observation, reward, terminated, truncated, info = env.step(action)
        sumRewards += reward
        if terminated or truncated:
            break

    if sumRewards > bestReward:
        bestReward = sumRewards
        bestActionSeq = np.copy(actionSeq)

    counter += 1
    if counter == 1:
        play()
    if counter == n_calls:
        play()
        exit()
    print(counter, ": ", bestReward)

    return sumRewards


def play():
    for _ in range(3):
        global bestActionSeq
        env = gym.make('CartPole-v1', render_mode="human")
        _, _ = env.reset(seed=0)
        for action in bestActionSeq:
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                break
        print()
        env.close()
