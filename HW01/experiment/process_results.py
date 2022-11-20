import sys
import os
import math
import time
import pandas as pd
import numpy as np
import run_solvers as rs
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


INSTANCE_PATH = rs.INSTANCE_PATH
INSTANCE_RUNS = rs.INSTANCE_RUNS
MAX_FLIPS = rs.MAX_FLIPS
GSAT_RESULTS = rs.GSAT_OUTPUT
GSAT = rs.GSAT
GSAT_NAME = os.path.basename(GSAT)
GSAT_STATS = './gsat2_results/gsat2_stats.csv'
PROBSAT = rs.PROBSAT
PROBSAT_NAME = os.path.basename(PROBSAT)
PROBSAT_RESULTS = rs.PROBSAT_OUTPUT
PROBSAT_STATS = './probsat_results/probsat_stats.csv'
RESULTS_PATH = './results/'
XING_WINNER = './results/xing_winner.csv'
FINAL_STATS = './results/final_stats.csv'


def instance_name(instance_df):
    return instance_df['inst'].values[0]


def successful_runs(instance_df):
    return len(instance_df[instance_df['satisfied'] == instance_df['max_satisfied']].values)


def total_runs(instance_df):
    return instance_df.shape[0]


def average_flips(instance_df):
    return instance_df['flips'].mean()


def fined_average_flips(instance_df):
    flips = instance_df['flips'].values
    satisfied = instance_df['satisfied'].values
    max_satisfied = instance_df['max_satisfied'].values
    penalty = 10
    fin_avg = 0
    for i in instance_df.index:
        if satisfied[i] < max_satisfied[i]:
            fin_avg += (flips[i] * penalty)
        else:
            fin_avg += flips[i]
    return fin_avg / flips.size


def mu(instance_df):
    instance_df = instance_df[instance_df['satisfied'] == instance_df['max_satisfied']]
    instance_df = instance_df[instance_df['flips'] != 0]
    instance_df['log_flips'] = np.log(instance_df['flips'])
    return instance_df['log_flips'].mean()


def sigma_squared(instance_df):
    mu_ = mu(instance_df)
    instance_df = instance_df[instance_df['satisfied'] == instance_df['max_satisfied']]
    instance_df = instance_df[instance_df['flips'] != 0]
    sigma_sum = 0
    for i in instance_df.index:
        sigma_sum += math.pow(math.log(instance_df['flips'][i]) - mu_, 2)
    return sigma_sum / (successful_runs(instance_df) - 1)


def process_results(sat_solver, sat_results, sat_stats):
    start = time.time()
    sat_name = os.path.basename(sat_solver)
    sat_results_df = pd.read_csv(
        sat_results,
        header=None,
        delimiter=' ',
        names=['inst', 'flips', 'max_flips', 'satisfied', 'max_satisfied'],
    )
    with open(sat_stats, 'w') as stats_file:
        print(f'inst,succ {sat_name},of,steps {sat_name},awg fined {sat_name},mu {sat_name},sig^2 {sat_name}', file=stats_file)
        for i in range(0, sat_results_df.shape[0], INSTANCE_RUNS):
            instance_df = sat_results_df[i:i + INSTANCE_RUNS]
            instance_df.reset_index(drop=True, inplace=True)
            sys.stdout.write(f'\r{int(i/INSTANCE_RUNS)+1}/{int(sat_results_df.shape[0]/INSTANCE_RUNS)}')
            sys.stdout.flush()
            inst = instance_name(instance_df)
            succ = successful_runs(instance_df)
            of = total_runs(instance_df)
            avg_flips = round(average_flips(instance_df), 3)
            avg_fined = round(fined_average_flips(instance_df), 3)
            mu_ = round(mu(instance_df), 5)
            sig2 = round(sigma_squared(instance_df), 5)
            print(f'{inst},{succ},{of},{avg_flips},{avg_fined},{mu_},{sig2}', file=stats_file)
    end = time.time()
    print(f'\n{round(end - start)}s')


def cdf(instance_df):
    instance_df = instance_df[instance_df['satisfied'] == instance_df['max_satisfied']]
    ecdf = ECDF(instance_df['flips'].values.tolist())
    return ecdf(list(range(1, MAX_FLIPS + 1)))


def corrected_cdf(instance_df):
    instance_cdf = cdf(instance_df)
    tries = instance_df.shape[0]
    succ = successful_runs(instance_df)
    return [cdf_val * (succ / tries) for cdf_val in instance_cdf]


def ccdf_comparison(gsat_ccdf, probsat_ccdf):
    for index in range(len(probsat_ccdf) - 1, -1, -1):
        if probsat_ccdf[index] != gsat_ccdf[index]:
            return PROBSAT_NAME if probsat_ccdf[index] > gsat_ccdf[index] else GSAT_NAME


def xing(winner, gsat_ccdf, probsat_ccdf):
    if winner == PROBSAT_NAME:
        for index in range(len(probsat_ccdf) - 1, -1, -1):
            if probsat_ccdf[index] < gsat_ccdf[index]:
                return index
    else:
        for index in range(len(probsat_ccdf) - 1, -1, -1):
            if probsat_ccdf[index] > gsat_ccdf[index]:
                return index


def xing_and_winner(gsat_results_file, probsat_results_file, xing_winner_file):
    start = time.time()
    gsat_results_df = pd.read_csv(
        gsat_results_file,
        header=None,
        delimiter=' ',
        names=['inst', 'flips', 'max_flips', 'satisfied', 'max_satisfied'],
    )
    probsat_results_df = pd.read_csv(
        probsat_results_file,
        header=None,
        delimiter=' ',
        names=['inst', 'flips', 'max_flips', 'satisfied', 'max_satisfied'],
    )
    with open(xing_winner_file, 'w') as x_w_file:
        print('inst,xing,winner', file=x_w_file)
        for i in range(0, gsat_results_df.shape[0], INSTANCE_RUNS):
            sys.stdout.write(f'\r{int(i / INSTANCE_RUNS) + 1}/{int(gsat_results_df.shape[0] / INSTANCE_RUNS)}')
            sys.stdout.flush()
            # gsat2
            gsat_instance_df = gsat_results_df[i:i + INSTANCE_RUNS]
            gsat_instance_df.reset_index(drop=True, inplace=True)
            gsat_ccdf = corrected_cdf(gsat_instance_df)
            # probsat
            probsat_instance_df = probsat_results_df[i:i + INSTANCE_RUNS]
            probsat_instance_df.reset_index(drop=True, inplace=True)
            probsat_ccdf = corrected_cdf(probsat_instance_df)
            # calc results
            name = instance_name(gsat_instance_df)
            winner = ccdf_comparison(gsat_ccdf, probsat_ccdf)
            xing_ = xing(winner, gsat_ccdf, probsat_ccdf)
            print(f'{name},{xing_},{winner}', file=x_w_file)
    end = time.time()
    print(f'\n{round(end - start)}s')


def final_results(gsat_stats, probsat_stats, xing_winner, final_stats):
    gsat_stats_df = pd.read_csv(gsat_stats)
    probsat_stats_df = pd.read_csv(probsat_stats)
    xing_winner_df = pd.read_csv(xing_winner)
    final_stats_df = pd.DataFrame()
    # inst
    final_stats_df['inst'] = gsat_stats_df['inst']
    # succ
    final_stats_df['succ gSAT2'] = gsat_stats_df['succ gSAT2']
    final_stats_df['succ probSAT'] = probsat_stats_df['succ probSAT']
    # of
    final_stats_df['of'] = gsat_stats_df['of']
    # steps
    final_stats_df['steps gSAT2'] = gsat_stats_df['steps gSAT2']
    final_stats_df['steps probSAT'] = probsat_stats_df['steps probSAT']
    # awg fined
    final_stats_df['awg fined gSAT2'] = gsat_stats_df['awg fined gSAT2']
    final_stats_df['awg fined probSAT'] = probsat_stats_df['awg fined probSAT']
    # mu sig
    final_stats_df['mu gSAT2'] = gsat_stats_df['mu gSAT2']
    final_stats_df['sig^2 gSAT2'] = gsat_stats_df['sig^2 gSAT2']
    final_stats_df['mu probSAT'] = probsat_stats_df['mu probSAT']
    final_stats_df['sig^2 probSAT'] = probsat_stats_df['sig^2 probSAT']
    # xing
    final_stats_df['xing'] = xing_winner_df['xing']
    # winner
    final_stats_df['winner'] = xing_winner_df['winner']
    final_stats_df.to_csv(final_stats, index=False)


def plot_histogram_comparison(data_set, df, col1, col2, file_suffix):
    fig, ax = plt.subplots()
    ax.hist(df[col1], label=col1, histtype="step", density=True)
    ax.hist(df[col2], label=col2, histtype="step", density=True)
    ax.set_title(f'{data_set} - {file_suffix}')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
    plt.savefig(f"{RESULTS_PATH}{data_set}_{file_suffix}.png")

def plot_bars(data_set, df, col, file_suffix):
    fig, ax = plt.subplots()
    values = df[col].value_counts().keys().tolist()
    counts = df[col].value_counts().tolist()
    ax.bar(values, counts)
    ax.set_title(f'{data_set} - {file_suffix}')
    plt.savefig(f"{RESULTS_PATH}{data_set}_{file_suffix}.png")

def plot_results(final_stats):
    final_stats_df = pd.read_csv(final_stats)

    instance_path = os.listdir(INSTANCE_PATH)
    instance_path.sort()
    lengthts = []
    for data_set in instance_path:
        lengthts.append(len(os.listdir(INSTANCE_PATH + data_set)))

    data_set_dfs = []
    for data_set_length in lengthts:
        dat_set_df = final_stats_df.head(data_set_length)
        dat_set_df.reset_index(drop=True, inplace=True)
        final_stats_df = final_stats_df.tail(final_stats_df.shape[0] - data_set_length)
        data_set_dfs.append(dat_set_df)

    for data_set, df in zip(instance_path, data_set_dfs):
        # succ
        plot_histogram_comparison(data_set, df, 'succ gSAT2', 'succ probSAT', 'succ')
        # steps
        plot_histogram_comparison(data_set, df, 'steps gSAT2', 'steps probSAT', 'steps')
        # awg fined
        plot_histogram_comparison(data_set, df, 'awg fined gSAT2', 'awg fined probSAT', 'awg_fined')
        # mu
        plot_histogram_comparison(data_set, df, 'mu gSAT2', 'mu probSAT', 'mu')
        # sig^2
        plot_histogram_comparison(data_set, df, 'sig^2 gSAT2', 'sig^2 probSAT', 'sig^2')
        # winner
        plot_bars(data_set, df, 'winner', 'winner')


if __name__ == '__main__':
    print("======================================")
    print(GSAT_STATS)
    process_results(GSAT, GSAT_RESULTS, GSAT_STATS)
    print("--------------------------------------")
    print(PROBSAT_STATS)
    process_results(PROBSAT, PROBSAT_RESULTS, PROBSAT_STATS)
    print("--------------------------------------")
    print(XING_WINNER)
    xing_and_winner(GSAT_RESULTS, PROBSAT_RESULTS, XING_WINNER)
    print("--------------------------------------")
    print(FINAL_STATS)
    final_results(GSAT_STATS, PROBSAT_STATS, XING_WINNER, FINAL_STATS)
    print("--------------------------------------")
    print("generating plots...")
    plot_results(FINAL_STATS)
    print("======================================")
    exit()
