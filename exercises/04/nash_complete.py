import numpy as np


nActions = 2
nPlayers = 3


def get_value(game, state, playerNr):
    index = 0
    for i, s in enumerate(state):
        index += s * (nActions ** (nPlayers - i - 1))
    return game[index][playerNr]

def test(game, state):
    print(game)
    for playerNr in range(nPlayers):
        alternativeRewards = []
        for a in range(nActions):
            alternativeState = np.copy(state)
            alternativeState[playerNr] = a
            alternativeRewards.append(get_value(game, alternativeState, playerNr))
        print()
        print("Player: ", playerNr)
        print("   Current action: ", state[playerNr])
        print("   Current reward: ", get_value(game, state, playerNr))
        print("   Alternative rewards: ", alternativeRewards)

def calculate_nash_equilibrium(game):
    state = np.random.choice(range(nActions), size=nPlayers)

    for iter in range(10_000):
        changed = False
        for playerNr in range(nPlayers):
            alternativeRewards = []
            for a in range(nActions):
                alternativeState = np.copy(state)
                alternativeState[playerNr] = a
                alternativeRewards.append(get_value(game, alternativeState, playerNr))
            if max(alternativeRewards) > get_value(game, state, playerNr):
                changed = True
                state[playerNr] = np.argmax(alternativeRewards)
                break
        if not changed:
            break
        if iter + 1 == 10_000:
            print("Did not converge after 10_000 iterations\n")

    return state


# create a random game
game = np.random.sample((nActions ** nPlayers, nPlayers))
# game with no nash equilibrium
#game = np.array([[1, 0, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0], [0, 1, 0], [0, 1, 1], [1, 1, 0], [1, 0, 1]])

state = calculate_nash_equilibrium(game)

test(game, state)
