#!/bin/bash

cd ../aco_solver/stats/

for city in kra30a
do
	for iteration in 100
	do
		for population in ca
		do
			echo $iteration, $city, $population
			python avg_summary_generator.py 20 $iteration $city ../../outputs/ $population
		done
	done
done