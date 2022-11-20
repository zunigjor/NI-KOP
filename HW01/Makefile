# PILOT
run_solvers_pilot:
	# Remove previous results
	rm -f ./pilot/gsat2_results/gsat2_results_*.csv
	rm -f ./pilot/probsat_results/probsat_results_*.csv
	# Run solvers
	cd pilot; ../venv/bin/python3 run_solvers.py

process_results_pilot:
	# Remove stats
	rm -f ./gsat_results/gsat2_stats.txt
	rm -f ./probsat_results/probsat_stats.txt
	# Process results
	cd pilot; ../venv/bin/python3 process_results.py

# EXPERIMENT
run_solvers_experiment:
	# Remove previous results
	rm -f ./experiment/gsat2_results/gsat2_results.csv
	rm -f ./experiment/probsat_results/probsat_results.csv
	# Run solvers
	cd experiment; ../venv/bin/python3 run_solvers.py

process_results_experiment:
	# Remove stats
	rm -f ./experiment/gsat2_results/gsat2_stats.csv
	rm -f ./experiment/probsat_results/probsat_stats.csv
	rm -f ./results/xing_winner.csv
	rm -f ./results/final_stats.csv
	rm -f ./results/*.png
	# Process results
	cd experiment; ../venv/bin/python3 process_results.py

