import copy
import math
import random

from simulated_annealing.state import State
from decimal import Decimal


def simulated_annealing(init_state, equilibrium, init_temperature, cooling_coefficient, min_temperature):
    state = init_state
    temperature = init_temperature
    best_state = State(copy.deepcopy(state.bitmap), copy.deepcopy(state.instance_data), copy.deepcopy(state.cost_coef))
    fitness = [best_state.cost]
    weights = [best_state.weight_sum]
    sat_clauses = [best_state.get_satisfied_clauses()]
    best_states = [best_state]
    while not frozen(temperature, min_temperature):
        for e in range(equilibrium):
            if is_better(state, best_state):
                best_state = copy.deepcopy(state)
            state = get_neighbour(state, temperature)
            fitness.append(state.cost)
            weights.append(state.weight_sum)
            sat_clauses.append(state.get_satisfied_clauses())
            best_states.append(best_state)
        temperature = cool(temperature, cooling_coefficient)
    return best_state, fitness, weights, sat_clauses, success_rate(best_state), best_states


def success_rate(state):
    return state.satisifed_clauses/state.total_clauses


def print_iteration(iteration, temperature, satisfied_clauses):
    print("*"*40)
    print("Iteration number: " + str(iteration))
    print("Temperature: " + str(temperature))
    print("Satisfied clauses: " + str(satisfied_clauses))


def cool(temperature, cooling_coefficient):
    return temperature * cooling_coefficient


def frozen(temperature, min_temperature):
    return temperature < min_temperature


def solution_exists(state):
    """
    :param state: one possible solution - State class instance
    :return: True if all clauses from defined problem are satisfiable with variable setting of state
    """
    return all(state.is_clause_satisfiable(clause) for clause in state.sat.clauses)


def is_better(state, best_state):
    return state.cost > best_state.cost


def get_neighbour(state, temperature):
    new_state = get_random_neighbour(state)
    if is_better(new_state, state) or random.randint(1, 100) < 10:
        return new_state
    delta = how_much_worse(new_state, state)
    if 0.6 < math.exp(-delta/Decimal(temperature)):
        return new_state
    return state


def get_random_neighbour(state):
    new_state = State(copy.deepcopy(state.bitmap), copy.deepcopy(state.instance_data), copy.deepcopy(state.cost_coef))
    if not new_state.satisifed_clauses == len(new_state.instance_data.clauses):
        var_to_change = new_state.var_from_unsatisfied_clause()
    else:
        var_to_change = random.randint(0, len(new_state.bitmap) - 1)
    new_state.bitmap[var_to_change] = int(not (new_state.bitmap[var_to_change]))
    new_state.get_satisfied_clauses()
    new_state.get_cost()
    return new_state


def how_much_worse(new, state):
    return state.cost - new.cost
