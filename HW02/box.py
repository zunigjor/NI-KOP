import math
from decimal import Decimal
########################################################################################################################
# Using:
def cost_function_0(state):
    return state.weight_sum - (state.cost_coef * state.max_weight) * (state.total_clauses - state.satisifed_clauses)
########################################################################################################################
def whitebox_0(instance_data):
    temperature = 10000  # 10 000
    equilibrium = 20
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_1(instance_data):
    temperature = 100000  # 100 000 -> better results compared to whitebox_0, needs to scale with instance
    equilibrium = 20
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_2(instance_data):
    temperature = 10000
    equilibrium = 50  # better results compared to whitebox_0, needs to scale with instance
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_3(instance_data):
    temperature = sum(instance_data.weights)  # worse
    equilibrium = len(instance_data.weights)
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_4(instance_data):
    temperature = sum(instance_data.weights)
    equilibrium = len(instance_data.weights) * 2  # better results
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3  # not best
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_5(instance_data):
    temperature = sum(instance_data.weights)
    equilibrium = len(instance_data.weights) * 2
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 1  # worse
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_6(instance_data):
    temperature = sum(instance_data.weights)
    equilibrium = len(instance_data.weights) * 2
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 5  # performed worse in easier instances but better in hard ones
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_7(instance_data):
    temperature = len(instance_data.weights) * max(instance_data.weights)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 5
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_8(instance_data):
    temperature = math.pow(10, len(instance_data.weights)/10)  # not a big difference
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 5
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef
########################################################################################################################
"""
Time to take a step in a new direction with new cost function:
"""
def cost_function_1(state):
    return Decimal(
        (state.weight_sum * state.cost_coef) + (state.satisifed_clauses * (1 - state.cost_coef))
    ) / Decimal(
        (state.instance_data.max_w_sum * state.cost_coef) + (len(state.instance_data.clauses) * (1 - state.cost_coef))
    )

########################################################################################################################
def whitebox_9(instance_data):
    temperature = math.pow(10, len(instance_data.weights)/10)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 0.1
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_10(instance_data):
    temperature = math.pow(10, len(instance_data.weights)/10)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 0.001
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_11(instance_data):
    temperature = math.pow(10, len(instance_data.weights)/10)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 0.00001
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

########################################################################################################################
# Final blackbox
########################################################################################################################
def blackbox(instance_data):
    temperature = math.pow(10, len(instance_data.weights)/10)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 0.00001
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef


