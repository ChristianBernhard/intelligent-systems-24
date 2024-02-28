import numpy as np
# np.random.seed(0)

N = 50
max_strength = 10 # test: 10 and 10000
strengths = np.random.choice(range(max_strength), size=N, replace=True)
# objective function ->a calculates the quality of a given solution: Strength difference between two teams
def oracle(x):
    """
        Calculate the difference in strength between two teams.
        The function is negated to convert it into a minimization problem.
        Input: x is a binary vector, representing the team assignment of each player {0, 1}
        Return:
        """
    team_1_strength = np.dot(strengths, x)
    team_2_strength = np.dot(strengths, 1 - x) #flips the binary values
    return -np.abs(team_1_strength - team_2_strength)


def tabu(oracle, iterations=1000, tabu_size=10, neighbors=100):
    """
    :param oracle: objective function
    :param iterations: how often tabu search will be done
    :param tabu_size: represents the number of solutions to keep in the tabu list
    :param neighbors: how many candidate solutions you generate in each iteration to explore the solution space around the current solution
    :return: best_solution of team division, best_objective_value
    """
    #Init Setup
    current_solution = np.random.choice([0, 1], size=N)
    best_solution = np.copy(current_solution)
    best_objective_value = oracle(best_solution)
    initial_team_1_strength = np.dot(strengths, current_solution)
    initial_team_2_strength = np.dot(strengths, 1 - current_solution)
    print(f"Initial Team 1 Strength: {initial_team_1_strength}, Initial Team 2 Strength: {initial_team_2_strength}")

    #Init Tabu List
    # matrix to keep track of the solutions that have been visited recently and should be avoided to prevent cycling back to previous solutions
    tabu_list = np.empty((tabu_size, N))
    tabu_list[:] = np.nan

    #Tabu Search Loop
    for it in range(iterations):
        # Generate neighbor solutions by swapping one players team assignment
        neighbor_solutions = np.array([current_solution.copy() for _ in range(neighbors)])
        for neighbor in neighbor_solutions:
            flip_index = np.random.randint(0, N) # Flip one random bit (player changes team)
            neighbor[flip_index] = 1 - neighbor[flip_index]

            # Make sure the new solution is not in the tabu list
            if any(np.all(neighbor == tabu_row) for tabu_row in tabu_list):
                neighbor[flip_index] = 1 - neighbor[flip_index]  # Revert the change if in tabu list

        # Evaluate all neighbors
        neighbor_values = np.array([oracle(neighbor) for neighbor in neighbor_solutions])
        # Select the best neighbor
        best_neighbor_index = np.argmin(neighbor_values) #see objective function: -
        best_neighbor = neighbor_solutions[best_neighbor_index]
        best_neighbor_value = neighbor_values[best_neighbor_index]

        # If the best neighbor is better than the best known solution, update the best solution
        if best_neighbor_value < best_objective_value:
            best_solution = best_neighbor
            best_objective_value = best_neighbor_value

        # Update the current solution
        current_solution = best_neighbor

        # Update the tabu list
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_solution, best_objective_value

best_solution, best_objective_value = tabu(oracle)

# Display results
print("Best solution:", best_solution)
print("Best objective value:", -best_objective_value)  # Negate back to original problem context (maximization)
print("Team 1 strength:", np.dot(strengths, best_solution))
print("Team 2 strength:", np.dot(strengths, 1 - best_solution))