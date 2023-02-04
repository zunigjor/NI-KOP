import os.path


class InstanceData:
    def __init__(self, instance_name, weights, clauses):
        self.instance_name = instance_name
        self.weights = weights
        self.clauses = clauses
        self.max_w_sum = sum(weights)


def read_weights(file):
    # extracts weights from instance file
    # 10th line in file looks like this
    # w 272 39 39 194 1 194 1 78 117 156 39 1 233 311 311 1 311 39 39 311 0
    weights_line = file[9].split(' ')
    weights_line.pop(0)
    weights_line.pop()
    return [eval(weight) for weight in weights_line]


def split_clause(line):
    plop = line.split(' ')
    plop.pop()
    return [eval(i) for i in plop]


def read_clauses(file):
    # extracts clauses from instance file
    # clauses start at line 12 and look like this
    #  4 -18 19 0
    return [split_clause(line) for line in file[11:]]


def parse_instance(instance_path):
    file = []
    with open(instance_path) as instance_file:
        file = [line.strip() for line in instance_file]
    instance_name = os.path.basename(os.path.normpath(instance_path))[:-6]
    weights = read_weights(file)
    clauses = read_clauses(file)
    return InstanceData(instance_name, weights, clauses)
