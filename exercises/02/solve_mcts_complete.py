from copy import deepcopy
from mcts import mcts
import oracle_complete


class CartPole_State():

    def __init__(self):
        self.action_sequence = []

    def getPossibleActions(self):
        return [0, 1]

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.action_sequence.append(action)
        return newState

    def isTerminal(self):
        return len(self.action_sequence) == 200

    def getReward(self):
        return oracle_complete.oracle(self.action_sequence)


initialState = CartPole_State()
searcher = mcts(timeLimit=9999999999)
searcher.search(initialState=initialState)

