from copy import deepcopy
from mcts import mcts
import oracle
import gym


class CartPole_State():

    def __init__(self):
        self.env = gym.make('CartPole-v1')
        self.observation = self.env.reset(seed=0)
        self.done = False
        self.reward = 0
        self.info = {}

    def getPossibleActions(self):
        return [0, 1]

    def takeAction(self, action):
        new_state = deepcopy(self)
        output = new_state.env.step(action)
        print(len(output))
        print(output)
        new_state.observation, new_state.reward, new_state.done, new_state.truncated, new_state.info = new_state.env.step(action)
        return new_state

    def isTerminal(self):
        return self.done

    def getReward(self):
        return self.reward


initialState = CartPole_State()
searcher = mcts(timeLimit=9999999999)
searcher.search(initialState=initialState)

