import pandas as pd
import run_solvers as rs

INSTANCE_RUNS = rs.INSTANCE_RUNS
GSAT_RESULTS = rs.GSAT_OUTPUT
GSAT_AVG_RESULTS = './gsat_results/gsat_avg_results.csv'
GSAT_STATS = './gsat_results/gsat_stats.txt'
PROBSAT_RESULTS = rs.PROBSAT_OUTPUT
PROBSAT_AVG_RESULTS = './probsat_results/probsat_avg_results.csv'
PROBSAT_STATS = './probsat_results/probsat_stats.txt'


def avg_results(SAT_results, SAT_avg_results):
    SAT_results_df = pd.read_csv(SAT_results, header=None)
    print(SAT_results_df)


def process_results(SAT_results, SAT_avg_results, SAT_stats):
    avg_results(SAT_results, SAT_avg_results)
    # number_of_instances = 0  # total number of instances
    # flips_equal_maxflips = 0  # SAT solver hit maximum flips
    # solved = 0  # SAT solver found a solution
    # with open(SAT_stats, 'w', newline='') as stats, open(SAT_results, 'r', newline='') as output_file:
    #     data_reader = csv.reader(output_file, delimiter=' ')
    #     for row in data_reader:
    #         number_of_instances += 1
    #         if row[0] == row[1]:
    #             flips_equal_maxflips += 1
    #         if row[2] == row[3]:
    #             solved += 1
    #     # Output stats to file
    #     print(f'Rows: {number_of_instances:>22}', file=stats)
    #     print(f'Flips maxed: {flips_equal_maxflips:>15}', file=stats)
    #     print(f'Solved: {solved:>20}', file=stats)
    #     # Output stats to terminal
    #     print(f'Rows: {number_of_instances:>22}')
    #     print(f'Flips maxed: {flips_equal_maxflips:>15}')
    #     print(f'Solved: {solved:>20}')


if __name__ == '__main__':
    print("======================================")
    process_results(GSAT_RESULTS, GSAT_AVG_RESULTS, GSAT_STATS)
    print("--------------------------------------")
    process_results(PROBSAT_RESULTS, PROBSAT_RESULTS, PROBSAT_STATS)
    print("======================================")
    exit()
