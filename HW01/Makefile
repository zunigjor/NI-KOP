# PILOT
pilot_all:
	make pilot_clean
	make pilot_run

pilot_clean:
	rm -f ./pilot/gsat_pilot_results/*.csv
	rm -f ./pilot/gsat_pilot_results/*.txt
	rm -f ./pilot/probsat_pilot_results/*.csv
	rm -f ./pilot/probsat_pilot_results/*.txt

pilot_run:
	cd pilot; python3 run_pilot.py
