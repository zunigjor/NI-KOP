
class InstanceOptimumData:
    # Simple class holding instance optimum name, weight and bitmap
    def __init__(self, name, weights, bitmap):
        self.name = name
        self.weights = weights
        self.bitmap = bitmap


def parse_optimum(filename) -> dict:
    # Extract optimum data into a dict for ease of searching
    optimum = {}
    with open(filename) as file:
        for line in file:
            line.strip()
            line_list = line.split(' ')
            line_list.pop()
            instance_name = "w" + line_list.pop(0)
            instance_weights = eval(line_list.pop(0))
            instance_bitmap = [0 if eval(i)<0 else 1 for i in line_list]
            optimum[instance_name] = InstanceOptimumData(instance_name, instance_weights, instance_bitmap)
    return optimum
