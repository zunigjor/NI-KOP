# PILOT
run_solvers_pilot:
	rm -f ./pilot/gsat_results/gsat_results_*.csv
	rm -f ./pilot/probsat_results/probsat_results_*.csv
	cd pilot; ../venv/bin/python3 run_solvers.py

process_results_pilot:
	rm -f ./gsat_results/gsat_stats.txt
	rm -f ./probsat_results/probsat_stats.txt
	cd pilot; ../venv/bin/python3 process_results.py

# EXPERIMENT
run_solvers_experiment:
	rm -f ./experiment/gsat_results/gsat_results.csv
	rm -f ./experiment/probsat_results/probsat_results.csv
	cd experiment; ../venv/bin/python3 run_solvers.py

process_results_experiment:
	rm -f ./experiment/gsat_results/gsat_stats.csv
	rm -f ./experiment/probsat_results/probsat_stats.csv
	cd experiment; ../venv/bin/python3 process_results.py

