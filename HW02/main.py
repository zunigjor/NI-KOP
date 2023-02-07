import os
import shutil
import pandas as pd
from multiprocessing import Process
from datetime import datetime

import box
from simulated_annealing.instance_opt_parser import parse_optimum
from simulated_annealing.instance_parser import parse_instance
from simulated_annealing.state import State
from simulated_annealing.state import get_random_bitmap
from simulated_annealing.simulated_annealing import simulated_annealing, success_rate
from simulated_annealing.fitness_plot import plot_fitnesses


def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)


def fill_in_fitnesses(fitness_list):
    max_len = max(map(len, fitness_list))
    for list in fitness_list:
        if len(list) < max_len:
            last = list[-1]
            list.extend(last for _ in range(max_len - len(list)))
    return fitness_list


def is_solution_optimal(solution, optimum):
    return solution.weight_sum == optimum[solution.instance_data.instance_name].weights


def run_sim(params_function, cost_function, whitebox=False):
    # Create folders
    run_name = params_function.__name__
    rm_r(f"results/{run_name}")
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
    # Go trough instances
    instances_path = "./instances"
    instance_dir: list = os.listdir(instances_path)
    instance_dir.sort()
    # iterate ./instance = wuf20-91, wuf50-218 ...
    for wufX_X in instance_dir:
        wufX_X_path = instances_path + "/" + wufX_X
        wufX_X_dir = os.listdir(wufX_X_path)
        # Extract optimums
        wufX_X_X_opt_dats = [opt for opt in wufX_X_dir if opt.endswith("-opt.dat")]
        wufX_X_X_opt_dats.sort()
        wufX_X_X_dir = list(set(wufX_X_dir) - set(wufX_X_X_opt_dats))
        wufX_X_X_dir.sort()
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
        for i in range(len(wufX_X_X_dir)):
            wufX_X_X_dir_path = wufX_X_path + "/" + wufX_X_X_dir[i]
            wufX_X_X_dir_instances = os.listdir(wufX_X_X_dir_path)
            wufX_X_X_opt_dat_path = wufX_X_path + "/" + wufX_X_X_opt_dats[i]
            # save optimums in dict
            optimum = parse_optimum(wufX_X_X_opt_dat_path)
            # metric
            optimal_rate = 0
            is_solution_rate = 0
            solutions = []
            succ = []
            # iterate ./instance/wufX-X/wufX-X-X := wuf20-01, wuf20-02, wuf20-03 ...
            for j in range(10) if whitebox else range(100):
                instance_name = wufX_X_X_dir[i][0:6] + "0" + str(j + 1)
                instance_path = wufX_X_X_dir_path + "/" + instance_name + ".mwcnf"
                # metric
                fitnesses = []
                for k in range(5) if whitebox else range(10):
                    # Measure instance time
                    instance_start = datetime.now()
                    instance_data = parse_instance(instance_path)
                    is_solution = False
                    # parameters
                    temperature, equilibrium, min_temperature, cooling_coef, cost_coef = params_function(instance_data)
                    # get init state
                    init_state = State(get_random_bitmap(len(instance_data.weights)), instance_data, cost_coef, cost_function)
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
                        is_solution_rate += 1
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
                    # Measure instance time
                    instance_end = datetime.now()
                    instance_elapsed_took = instance_end - instance_start
                    instance_took = "%02d:%02d:%02d" % (instance_elapsed_took.seconds // 3600, instance_elapsed_took.seconds // 60 % 60, instance_elapsed_took.seconds % 60)
                    instance_took = instance_took + f".{str(instance_elapsed_took.microseconds)[:1]}"
                    instance_elapsed_since_start = instance_end - start_time
                    instance_since_start = "%02d:%02d:%02d:%02d" % (instance_elapsed_since_start.days, instance_elapsed_since_start.seconds // 3600, instance_elapsed_since_start.seconds // 60 % 60, instance_elapsed_since_start.seconds % 60)
                    print(f"{run_name}, {wufX_X_X_dir[i]}, {str(instance_name)}, {str(k+1)}, s: {str(is_solution)[0]}, o: {str(optimal)[0]}, {instance_took}, {instance_since_start}")
                    # plot first run
                    if k == 0:
                        plot_fitnesses(plots_output_path, fitnesses, f"{wufX_X_X_dir[i]}{instance_name[5:]}", weights, sat_clauses, best_states)
            # Print and save instanceset results
            str_stars = "*"*100
            str_run_identification = f"{run_name}, {wufX_X_X_dir[i]}, "
            str_success_rate = f"{sum(succ)}/{len(succ)}={sum(succ)/len(succ)}, "
            str_solution_rate = f"s: {is_solution_rate}/{len(solutions)}={is_solution_rate/len(solutions)}, "
            str_optimum_rate = f"o: {optimal_rate}/{len(solutions)}={optimal_rate/len(solutions)}"
            print(f"{str_stars}\n{str_run_identification}{str_success_rate}{str_solution_rate}{str_optimum_rate}\n{str_stars}")
            with open("results/stats.csv", 'a') as out_file:
                out_file.write(f"{run_name}, {wufX_X_X_dir[i]}, {len(succ)}, {sum(succ)}, {sum(succ) / len(succ)}, {is_solution_rate}, {is_solution_rate / len(solutions)}, {optimal_rate}, {optimal_rate / len(solutions)}\n")
            results.to_csv(f"{csv_output_path}{str(wufX_X_X_dir[i])}_{run_name}.csv")
    # Measure total time
    end_time = datetime.now()
    elapsed_total = end_time - start_time
    out_strarted_at = f"Start: {start_time.strftime('%H:%M:%S')}"
    out_took = "Took: %02d:%02d:%02d:%02d" % (elapsed_total.days, elapsed_total.seconds // 3600, elapsed_total.seconds // 60 % 60, elapsed_total.seconds % 60)
    out_end_at = f"End: {end_time.strftime('%H:%M:%S')}"
    print(f"{run_name} {out_strarted_at} {out_took} {out_end_at}")


if __name__ == '__main__':
    try:
        os.mkdir("results")
    except:
        pass
    with open("results/stats.csv", 'w') as out_file:
        out_file.write("name, instances, runs, satisfied_clauses, satisfied_clauses_rate, solutions_found, solutions_found rate, optimums_reached, optimums_reached_rate\n")

    w_0 = Process(target=run_sim, args=(box.whitebox_0, box.cost_function_0, True))
    w_1 = Process(target=run_sim, args=(box.whitebox_1, box.cost_function_0, True))
    w_2 = Process(target=run_sim, args=(box.whitebox_2, box.cost_function_0, True))
    w_3 = Process(target=run_sim, args=(box.whitebox_3, box.cost_function_0, True))
    w_4 = Process(target=run_sim, args=(box.whitebox_4, box.cost_function_0, True))
    w_5 = Process(target=run_sim, args=(box.whitebox_5, box.cost_function_0, True))
    w_6 = Process(target=run_sim, args=(box.whitebox_6, box.cost_function_0, True))
    w_7 = Process(target=run_sim, args=(box.whitebox_7, box.cost_function_0, True))
    w_8 = Process(target=run_sim, args=(box.whitebox_8, box.cost_function_0, True))
    w_9 = Process(target=run_sim, args=(box.whitebox_9, box.cost_function_1, True))
    w_10 = Process(target=run_sim, args=(box.whitebox_10, box.cost_function_1, True))
    w_11 = Process(target=run_sim, args=(box.whitebox_11, box.cost_function_1, True))
    blackbox = Process(target=run_sim, args=(box.blackbox, box.cost_function_1, False))

    w_0.start()
    w_1.start()
    w_2.start()
    w_3.start()
    w_4.start()
    w_5.start()
    w_6.start()
    w_7.start()
    w_8.start()
    w_9.start()
    w_10.start()
    w_11.start()
    blackbox.start()

    w_0.join()
    w_1.join()
    w_2.join()
    w_3.join()
    w_4.join()
    w_5.join()
    w_6.join()
    w_7.join()
    w_8.join()
    w_9.join()
    w_10.join()
    w_11.join()
    blackbox.join()
