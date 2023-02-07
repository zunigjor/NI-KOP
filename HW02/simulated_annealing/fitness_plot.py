from matplotlib import pyplot as plt
import time


def plot_fitnesses(output_path, fitness_list, instance_name, weights, satc, solutions):
    fig, a = plt.subplots(3)
    fig.suptitle(instance_name)
    best_costs = [state.cost for state in solutions]
    for fit in fitness_list:
        a[0].plot(fit, label="all states")
    a[0].plot(best_costs, label="best state")
    a[0].set_xlabel('State number')
    a[0].set_ylabel('Fitness')
    filename = output_path + str(instance_name) + '.png'
    a[1].plot(weights)
    a[1].set_xlabel('State number')
    a[1].set_ylabel('Weights')
    a[2].plot(satc)
    a[2].set_xlabel('State number')
    a[2].set_ylabel('Satisfied clauses')
    plt.savefig(filename)
    plt.close()
