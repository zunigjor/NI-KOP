import numpy as np
import random
from decimal import Decimal

from simulated_annealing.instance_parser import InstanceData


def get_random_bitmap(lenght):
    return np.random.randint(0, 2, lenght).tolist()


class State:
    def __init__(self, bitmap, instance_data, cost_coef, cost_function):
        self.bitmap = bitmap
        self.instance_data: InstanceData = instance_data
        self.cost_coef = cost_coef
        self.cost_function = cost_function
        self.max_weight = max(self.instance_data.weights)
        self.weight_sum = self.get_weight_sum()
        self.total_clauses = len(self.instance_data.clauses)
        self.satisifed_clauses = self.get_satisfied_clauses()
        self.cost = self.get_cost()

    def get_weight_sum(self):
        sum = 0
        for i in range(len(self.bitmap)):
            if self.bitmap[i] == 1:
                sum += self.instance_data.weights[i]
        return sum

    def get_satisfied_clauses(self):
        satisfied_clauses = 0
        for clause in self.instance_data.clauses:
            if self.is_clause_satisfied(clause):
                satisfied_clauses += 1
        return satisfied_clauses

    def is_clause_satisfied(self, clause):
        for var in clause:
            if self.is_variable_satisfied(var, self.bitmap[abs(var) - 1]):
                return True
        return False

    def is_variable_satisfied(self, var, setting):
        if var > 0 and setting == 1:
            return True
        elif var < 0 and setting == 0:
            return True
        else:
            return False

    def get_cost(self):
        return self.cost_function(self)

    def get_var_from_unsatisfied_clause(self):
        random_unsatisfied_clause = self.get_random_unsatisfied_clause()
        return abs(random.choice(random_unsatisfied_clause)) - 1

    def get_random_unsatisfied_clause(self):
        unsatisfied_clauses = [clause for clause in self.instance_data.clauses if not self.is_clause_satisfied(clause)]
        return random.choice(unsatisfied_clauses)

    def relative_error(self):
        return 1 - self.satisifed_clauses/len(self.instance_data.clauses)
