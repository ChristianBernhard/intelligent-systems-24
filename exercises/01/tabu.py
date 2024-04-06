import numpy as np


N = 50
max_strength = 10_000 # test: 10 and 10_000


numbers = np.random.choice(range(max_strength), size=N, replace=True)
def oracle(x):
    return -np.abs( np.dot(numbers, x) - np.dot(numbers, (1 - x)) )

def tabu(oracle):

    tabuList = []
    s = np.random.choice([0,1], size=N, replace=True)
    bestValue = oracle(s)

    for iteration in range(20):

        bestNeighbor = None
        bestNeighborValue = -np.inf

        for i in range(N):
            n = np.copy(s)
            n[i] = 1 - n[i]
            if n.tolist() not in tabuList:
                v = oracle(n)
                if v > bestNeighborValue:
                    bestNeighborValue = v
                    bestNeighbor = n

        if bestNeighborValue > bestValue:
            bestValue = bestNeighborValue
        s = bestNeighbor

        tabuList.append(bestNeighbor.tolist())
        tabuList = tabuList[-100:]

        print(iteration, ": ", bestValue)


tabu(oracle)
