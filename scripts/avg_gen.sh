#!/bin/bash

cd ../

for city in wil50
do
	for iteration in 1000
	do
		for population in ca #cs la ha ca egocentric altercentric goodAtConflict badAtConflict eq ego alter good bad eqWithoutBad egoWithoutBad alterWithoutBad goodWithoutBad
		do
		    for ants in 20
		    do
		        for j in {5..6}
		        do
                    echo $ants, $iteration, $city, $population, $j
                    python -m aco_solver.stats.avg_summary_generator $ants $iteration $city outputs/parametrized_$j/ $population
                done
            done
		done
	done
done