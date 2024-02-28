from copy import deepcopy
from mcts import mcts
import oracle


class CartPole_State():

    def __init__(self):
        pass # TODO

    def getPossibleActions(self):
        pass # TODO

    def takeAction(self, action):
        pass # TODO

    def isTerminal(self):
        pass # TODO

    def getReward(self):
        pass # TODO


initialState = CartPole_State()
searcher = mcts(timeLimit=9999999999)
searcher.search(initialState=initialState)

