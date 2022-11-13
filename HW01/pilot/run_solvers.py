import os
import subprocess
import sys
import time


# Pilot runs only on 100 instances 100 times from each dataset.
PILOT_SIZE = 100
PILOT_RUNS = 100
# Trying to determine best amount of flips.
FLIPS = [300, 700, 1500, 3000, 6000]
INSTANCE_PATH = '../instance/'
# gSAT2
GSAT = '../gSAT2/gSAT2'
GSAT_ARGS = ' -p 0.4 -r time -i {f} {input}'
GSAT_OUTPUT = './gsat_results/gsat_results_{f}.csv'
# probSAT
PROBSAT = '../probSAT/probSAT'
PROBSAT_ARGS = ' --cb 2.3 --cm 0 -r time --maxflips {f} {input}'
PROBSAT_OUTPUT = './probsat_results/probsat_results_{f}.csv'


def run_SAT(SAT_solver, SAT_args, SAT_output):
    print(f'{os.path.basename(SAT_solver):<8}{"START":>20}')
    # Measure time
    SAT_start_time = time.time()
    # Measure steps
    total_steps = len(FLIPS) * len(os.listdir(INSTANCE_PATH)) * PILOT_SIZE * PILOT_RUNS
    current_step = 1

    for flip in FLIPS:
        with open(SAT_output.format(f=flip), 'w') as output_file:
            instance = os.listdir(INSTANCE_PATH)
            instance.sort()
            for data_set in instance:
                for i in range(1, PILOT_SIZE + 1):
                    input_path = f'{INSTANCE_PATH}{data_set}/{data_set[0:5]}0{i}.cnf'
                    for j in range(PILOT_RUNS):
                        # Run command
                        command = SAT_solver + SAT_args.format(f=flip, input=input_path)
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
    print(f'{os.path.basename(SAT_solver) + " time":<13} {str(round(SAT_end_time - SAT_start_time)) + "s":>14}')


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
