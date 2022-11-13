import os
import subprocess
import sys
import time


INSTANCE_RUNS = 1000
INSTANCE_PATH = '../instance/'
# gSAT2
GSAT = '../gSAT2/gSAT2'
GSAT_ARGS = ' -p 0.4 -r time -i 1500 {input}'
GSAT_OUTPUT = './gsat_results/gsat_results.csv'
# probSAT
PROBSAT = '../probSAT/probSAT'
PROBSAT_ARGS = ' --cb 2.3 --cm 0 -r time --maxflips 1500 {input}'
PROBSAT_OUTPUT = './probsat_results/probsat_results.csv'


def run_SAT(SAT_solver, SAT_args, SAT_output):
    print(f'{os.path.basename(SAT_solver):<8}{"START":>20}')
    # Measure time
    SAT_start_time = time.time()
    # Calculate total steps
    total_steps = 0
    current_step = 1
    for instance_folder in os.listdir(INSTANCE_PATH):
        total_steps += len(os.listdir(INSTANCE_PATH + instance_folder))
    total_steps *= INSTANCE_RUNS

    # Main loop
    instance_path = os.listdir(INSTANCE_PATH)
    instance_path.sort()
    with open(SAT_output, 'w') as output_file:
        for instance_folder in instance_path:
            instance_folder_len = len(os.listdir(INSTANCE_PATH + instance_folder))
            for i in range(1, instance_folder_len + 1):
                input_path = f'{INSTANCE_PATH}{instance_folder}/{instance_folder[0:5]}0{i}.cnf'
                for j in range(INSTANCE_RUNS):
                    # Run command
                    command = SAT_solver + SAT_args.format(input=input_path)
                    result = subprocess.run([command], shell=True, capture_output=True).stderr
                    print(f'{os.path.basename(input_path)} {result.decode("utf-8")}', end='', file=output_file)

                    # Print steps
                    step = f'{current_step}/{total_steps}'
                    sys.stdout.write(f'\r{os.path.basename(SAT_solver):<8}{step:>20}')
                    sys.stdout.flush()
                    current_step += 1

    # Print measured time
    SAT_end_time = time.time()
    print(f'\n{os.path.basename(SAT_solver):<8}{"DONE":>20}')
    print(f'{os.path.basename(SAT_solver) + " time":<13} {str(round(SAT_end_time - SAT_start_time))+"s":>14}')


if __name__ == '__main__':
    print("======================================")
    start_time = time.time()
    run_SAT(GSAT, GSAT_ARGS, GSAT_OUTPUT)
    print("--------------------------------------")
    run_SAT(PROBSAT, PROBSAT_ARGS, PROBSAT_OUTPUT)
    end_time = time.time()
    print("--------------------------------------")
    print(f"Total time: {round(end_time - start_time)}s")
    print("======================================")
    exit()
