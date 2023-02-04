import os
import shutil

import pandas as pd
from multiprocessing import Process
from datetime import datetime

from simulated_annealing.instance_opt_parser import parse_optimum
from simulated_annealing.instance_parser import parse_instance
from simulated_annealing.state import State
from simulated_annealing.state import get_random_bitmap
from simulated_annealing.simulated_annealing import simulated_annealing, success_rate
from simulated_annealing.fitness_plot import plot_fitnesses


### Whitebox runs
def whitebox_0(instance_data):
    temperature = 10000
    equilibrium = 20
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_1(instance_data):
    temperature = 100000
    equilibrium = 20
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_2(instance_data):
    temperature = 100000
    equilibrium = 50
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_3(instance_data):
    temperature = 100000
    equilibrium = 200
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 2
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_4(instance_data):
    temperature = len(instance_data.weights) * max(instance_data.weights)
    equilibrium = len(instance_data.weights) * 2
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef

def whitebox_5(instance_data):
    temperature = len(instance_data.weights) * max(instance_data.weights)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef


### Blackbox run
def blackbox(instance_data):
    temperature = len(instance_data.weights) * max(instance_data.weights)
    equilibrium = len(instance_data.weights) * 4
    min_tepmerature = 0.0001
    cooling_coef = 0.9
    cost_coef = 3
    return temperature, equilibrium, min_tepmerature, cooling_coef, cost_coef


# Sim functions
def fill_in_fitnesses(fitness_list):
    max_len = max(map(len, fitness_list))
    for list in fitness_list:
        if len(list) < max_len:
            last = list[-1]
            list.extend(last for _ in range(max_len - len(list)))
    return fitness_list


def is_solution_optimal(solution, optimum):
    return solution.weight_sum == optimum[solution.instance_data.instance_name].weights


def run_sim(whitebox=True, params_function=whitebox_0):
    run_name = params_function.__name__
    csv_output_path = f"results/{run_name}/"
    plots_output_path = f"results/{run_name}/plots/"
    try:
        os.mkdir(csv_output_path)
    except:
        print(f"Directory {csv_output_path} already exists")
    try:
        os.mkdir(plots_output_path)
    except:
        print(f"Directory {plots_output_path} already exists")
    # Measure time
    start_time = datetime.now()
    print(f"{os.getpid()} {run_name} start: {start_time.strftime('%H:%M:%S')}")

    instances_path = "./instances"
    instance_dir: list = os.listdir(instances_path)
    instance_dir.sort()
    # iterate ./instance = wuf20-91, wuf50-218 ...
    for wufX_X in instance_dir:
        wufX_X_path = instances_path + "/" + wufX_X
        wufX_X_dir = os.listdir(wufX_X_path)
        wufX_X_X_opt_dats = [opt for opt in wufX_X_dir if opt.endswith("-opt.dat")]
        wufX_X_X_opt_dats.sort()
        wufX_X_X_dir = list(set(wufX_X_dir) - set(wufX_X_X_opt_dats))
        wufX_X_X_dir.sort()
        # metrics
        succ = []
        results = pd.DataFrame(columns=['instance',
                                        'init_temperature',
                                        'min_temperature',
                                        'cooling_coefficient',
                                        'equilibrium',
                                        'cost_coefficient',
                                        'relative_absolute_error',
                                        'is_instance_optimal',
                                        'cost',
                                        'weight',
                                        'is_solution'
                                        ])
        # iterate ./instance/wufX-X  = wuf20-91-M, wuf20-91-N ...
        # WHITEBOX run chooses only -M folders
        for i in range(1) if whitebox else range(len(wufX_X_X_dir)):
            wufX_X_X_dir_path = wufX_X_path + "/" + wufX_X_X_dir[i]
            wufX_X_X_dir_instances = os.listdir(wufX_X_X_dir_path)
            wufX_X_X_opt_dat_path = wufX_X_path + "/" + wufX_X_X_opt_dats[i]
            # save optimums in dict
            optimum = parse_optimum(wufX_X_X_opt_dat_path)
            # metric
            optimal_rate = 0
            solutions = []
            # iterate ./instance/wufX-X/wufX-X-X := wuf20-01, wuf20-02, wuf20-03 ...
            for j in range(25) if whitebox else range(len(wufX_X_X_dir_instances)):
                instance_name = wufX_X_X_dir[i][0:6] + "0" + str(j + 1)
                instance_path = wufX_X_X_dir_path + "/" + instance_name + ".mwcnf"
                # metric
                fitnesses = []
                for k in range(10) if whitebox else range(30):
                    instance_start = datetime.now()
                    instance_data = parse_instance(instance_path)
                    is_solution = False
                    # parameters
                    temperature, equilibrium, min_temperature, cooling_coef, cost_coef = params_function(instance_data)
                    # get init state
                    init_state = State(get_random_bitmap(len(instance_data.weights)), instance_data, cost_coef)
                    # simulate annealing
                    solution, fitness, weights, sat_clauses, success, best_states = simulated_annealing(init_state,
                                                                                                        equilibrium,
                                                                                                        temperature,
                                                                                                        cooling_coef,
                                                                                                        min_temperature)
                    # metrics
                    optimal = is_solution_optimal(solution, optimum)
                    if optimal:
                        optimal_rate += 1
                    solutions.append(solution)
                    fitnesses.append(fitness)
                    succ.append(success)
                    fitnesses = fill_in_fitnesses(fitnesses)
                    if success_rate(solution) == 1:
                        is_solution = True
                    results.loc[len(results.index)] = [instance_name,
                                                       temperature,
                                                       min_temperature,
                                                       cooling_coef,
                                                       equilibrium,
                                                       cost_coef,
                                                       solution.relative_error(),
                                                       optimal,
                                                       solution.cost,
                                                       solution.weight_sum,
                                                       is_solution]
                    instance_end = datetime.now()
                    instance_took = instance_end - instance_start
                    inst_std_out = f"{run_name} {str(instance_name)}, {str(k+1)}, sol: {str(is_solution)[0]}, opt: {str(optimal)[0]}, took: {instance_took}"
                    print(inst_std_out)
                    if k == 0:
                        plot_fitnesses(plots_output_path, fitnesses, instance_name, weights, sat_clauses, best_states)
            print(f"{run_name} average success rate: " + str(sum(succ) / len(succ)))
            print(f"{run_name} optimal weights reached: " + str(optimal_rate / len(solutions)))
            results.to_csv(f"{csv_output_path}{str(wufX_X_X_dir[i])}_{run_name}.csv")
    # Measure time
    end_time = datetime.now()
    elapsed_total = end_time - start_time
    out_strarted_at = f"Start: {start_time.strftime('%H:%M:%S')}"
    out_took = "Took: %02d:%02d:%02d:%02d" % (elapsed_total.days, elapsed_total.seconds // 3600, elapsed_total.seconds // 60 % 60, elapsed_total.seconds % 60)
    out_end_at = f"End: {end_time.strftime('%H:%M:%S')}"
    print(f"{run_name} {out_strarted_at} {out_took} {out_end_at}")


if __name__ == '__main__':
    def rm_r(path):
        if not os.path.exists(path):
            return
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)

    rm_r("./results")
    try:
        os.mkdir("results")
    except:
        print(f"Directory ./results already exists")

    w_0 = Process(target=run_sim, args=(True, whitebox_0))
    w_1 = Process(target=run_sim, args=(True, whitebox_1))
    w_2 = Process(target=run_sim, args=(True, whitebox_2))
    w_3 = Process(target=run_sim, args=(True, whitebox_3))
    w_4 = Process(target=run_sim, args=(True, whitebox_4))
    w_5 = Process(target=run_sim, args=(True, whitebox_5))
    bbx = Process(target=run_sim, args=(False, blackbox))

    w_0.start()
    w_1.start()
    w_2.start()
    w_3.start()
    w_4.start()
    w_5.start()
    bbx.start()

    w_0.join()
    w_1.join()
    w_2.join()
    w_3.join()
    w_4.join()
    w_5.join()
    bbx.join()
