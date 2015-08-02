#!/bin/bash

cd ../aco_solver/stats/

for city in eil51 berlin52 kroB200
do
	for iteration in 20 50 100
	do
		for population in a awithout eq eqwithout c cwithout d dwithout ca cs la ha
		do
			echo $iteration, $city, $population
			python avg_summary_generator.py 100 $iteration $city ../../outputs/ $population
		done
	done
done