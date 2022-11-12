import os
import sys
from multiprocessing import Process
import csv

# Pilot runs only on 100 instances from each dataset.
PILOT_SIZE = 100
# Trying to determine best amount of flips.
FLIPS = [300, 700, 1500, 3000, 6000]
INSTANCE_PATH = '../instance/'
# gSAT2
GSAT = '../gSAT2/gSAT2'
GSAT_ARGS = ' -p 0.4 -r time -i {f} {ip} 2>>'
GSAT_OUTPUT = './gsat_pilot_results/gsat_pilot_experiment_{f}.csv'
GSAT_RESULTS = './gsat_pilot_results/gsat_pilot_results_stats.txt'
# probSAT
PROBSAT = '../probSAT/probSAT'
PROBSAT_ARGS = ' --cb 0 --cm 2.3 -r time --maxflips {f} {ip} 2>>'
PROBSAT_OUTPUT = './probsat_pilot_results/probsat_pilot_experiment_{f}.csv'
PROBSAT_RESULTS = './probsat_pilot_results/probsat_pilot_results_stats.txt'


def run_SAT(SAT_solver, SAT_args, SAT_output):
    print(f'{os.path.basename(SAT_solver)} START')
    total_steps = len(FLIPS) * len(os.listdir(INSTANCE_PATH)) * PILOT_SIZE * PILOT_SIZE
    current_step = 1
    for flip in FLIPS:
        instance = os.listdir(INSTANCE_PATH)
        instance.sort()
        for instance_folder in instance:
            for i in range(1, PILOT_SIZE + 1):  # Pro pilotni verzi pouzivam pouze prvnich 100 instanci z datovych sad
                instance_path = f'{INSTANCE_PATH}{instance_folder}/{instance_folder[0:5]}0{i}.cnf'
                for j in range(PILOT_SIZE):  # Kazdou instanci zkusim 100x
                    command = SAT_solver + SAT_args.format(f=flip, ip=instance_path) + SAT_output.format(f=flip)
                    os.popen(command)
                    sys.stdout.write('\r{} {}/{}'.format(os.path.basename(SAT_solver), current_step, total_steps))
                    sys.stdout.flush()
                    current_step += 1
    print(f'\n{os.path.basename(SAT_solver)} DONE')


def process_results(SAT_output, SAT_stats):
    # Total stats
    total_solved = 0                  # Average amount of solutions found
    total_solved_per_flip = 0         # Average amount of solved/flip
    with open(SAT_stats, 'w') as stats:
        for flip in FLIPS:
            # Flip stats
            number_of_instances = 0     # total number of instances
            flips_equal_maxflips = 0    # SAT solver hit maximum flips
            solved = 0                  # SAT solver found a solution
            # Count the results
            with open(SAT_output.format(f=flip), newline='') as outputs_file:
                data_reader = csv.reader(outputs_file, delimiter=' ')
                for row in data_reader:
                    number_of_instances += 1
                    if row[0] == row[1]:
                        flips_equal_maxflips += 1
                    if row[2] == row[3]:
                        solved += 1
            # Add to totals
            total_solved += solved
            total_solved_per_flip += solved / flip
            # Output flip stats
            print(f'{flip}:', file=stats)
            print(f'  Total rows: {number_of_instances:>25}', file=stats)
            print(f'  Flips maxed: {flips_equal_maxflips:>24}', file=stats)
            print(f'  Solved: {solved:>29}', file=stats)
            print(f'  Solved/flips: {solved / flip:>23.4f}', file=stats)
        # Output total stats
        print(f'Total stats:', file=stats)
        print(f'  Average solved: {total_solved / len(FLIPS):>21.4f}', file=stats)
        print(f'  Average solved/flips: {total_solved_per_flip / len(FLIPS):>15.4f}', file=stats)


def run(SAT_solver, SAT_args, SAT_output, SAT_stats):
    run_SAT(SAT_solver, SAT_args, SAT_output)
    process_results(SAT_output, SAT_stats)


if __name__ == '__main__':
    gsat = Process(target=run, args=(GSAT, GSAT_ARGS, GSAT_OUTPUT, GSAT_RESULTS))
    probsat = Process(target=run, args=(PROBSAT, PROBSAT_ARGS, PROBSAT_OUTPUT, PROBSAT_RESULTS))
    gsat.start()
    probsat.start()
    gsat.join()
    probsat.join()
    exit()
