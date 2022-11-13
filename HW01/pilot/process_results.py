import csv
import os.path

import run_solvers as rs


FLIPS = rs.FLIPS
GSAT_OUTPUT = rs.GSAT_OUTPUT
GSAT_STATS = './gsat_results/gsat_stats.txt'
PROBSAT_OUTPUT = rs.PROBSAT_OUTPUT
PROBSAT_STATS = './probsat_results/probsat_stats.txt'


def process_results(SAT_output, SAT_stats):
    # Total stats
    total_solved = 0                  # Average amount of solutions found
    total_solved_per_flip = 0         # Average amount of solved/flip
    print(os.path.basename(SAT_stats))
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
                    if row[1] == row[2]:
                        flips_equal_maxflips += 1
                    if row[3] == row[4]:
                        solved += 1
            # Add to totals
            total_solved += solved
            total_solved_per_flip += solved / flip
            # Output flip stats
            print(
                f'{flip}:\n'
                f'  Total rows:{number_of_instances:>26}\n'
                f'  Flips maxed: {flips_equal_maxflips:>24}\n'
                f'  Solved: {solved:>29}\n'
                f'  Solved/flips: {solved / flip:>23.2f}',
                file=stats
            )
            print(
                f'{flip}:\n'
                f'  Total rows:{number_of_instances:>26}\n'
                f'  Flips maxed: {flips_equal_maxflips:>24}\n'
                f'  Solved: {solved:>29}\n'
                f'  Solved/flips: {solved / flip:>23.2f}',
            )
        # Output total stats
        print(
            f'Total stats:\n'
            f'  Average solved: {total_solved / len(FLIPS):>21.2f}\n'
            f'  Average solved/flips: {total_solved_per_flip / len(FLIPS):>15.2f}',
            file=stats
        )
        print(
            f'Total stats:\n'
            f'  Average solved: {total_solved / len(FLIPS):>21.2f}\n'
            f'  Average solved/flips: {total_solved_per_flip / len(FLIPS):>15.2f}'
        )


if __name__ == '__main__':
    print("======================================")
    process_results(GSAT_OUTPUT, GSAT_STATS)
    print("--------------------------------------")
    process_results(PROBSAT_OUTPUT, PROBSAT_STATS)
    print("======================================")
    exit()
