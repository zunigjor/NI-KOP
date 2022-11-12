import os
from multiprocessing import Process
import csv


INSTANCE_PATH = '../instance/'
# gSAT2
GSAT_PATH = '../gSAT2/'
GSAT_NAME = 'gSAT2'
GSAT_ARGS = ' -p 0.4 -r time -i 1500 {input_file} 2>>./gsat_results/gsat_results.csv'
GSAT_STATS = './gsat_pilot_results/gsat_experiment_stats.txt'
GSAT = GSAT_PATH + GSAT_NAME + GSAT_ARGS

# probSAT
PROBSAT_PATH = '../probSAT/'
PROBSAT_NAME = 'probSAT'
PROBSAT_ARGS = ' --cb 0 --cm 2.3 -r time --maxflips 1500 {input_file} 2>>./probsat_results/probsat_results.csv'
PROBSAT_STATS = './probsat_experiment_results/probsat_pilot_results_stats.txt'
PROBSAT = PROBSAT_PATH + PROBSAT_NAME + PROBSAT_ARGS

def run_SAT(SAT_solver_name, SAT_solver):
    print(f'{SAT_solver_name} START')
    instance = os.listdir(INSTANCE_PATH)
    instance.sort()
    for instance_folder in instance:
        for i in range()

def process_results(SAT_solver_name, SAT_stats):


def run(SAT_solver_name, SAT_solver, SAT_stats):
    run_SAT(SAT_solver_name, SAT_solver)
    process_results(SAT_solver_name, SAT_stats)


if __name__ == '__main__':
