#!/bin/bash

cd ~/Projekty/miss/pyage-aco-solver/

#              0        1    2    3    4      5       6       7      8      9      10    11
cities_arr=(berlin52 eil51 eil76 pr76 st70 kroA100 kroE100 lin105 rat195 kroB200 ts225 att532)
optimum_arr=(7542 426 538 108159 675 21282 22068 14379 2323 29437 126643 27686)

#            0      1   2  3 4    5      6      7   8       9    10 11
populations=(a awithout c ca cs cwithout d dwithout eq eqwithout ha la)
types=(pc pc pc ca cs pc pc pc pc pc ha la)

DIRNAME='outputs/zeus_wyniki_final'

for i in 0 1 9
do
	CITY=${cities_arr[i]}
	OPTIMAL=${optimum_arr[i]}

	for j in 0 1 2 3 4 5 6 7 8 9 10 11
	do
        POP=${populations[j]}
	    TYPE=${types[j]}

        for iterations in 20 50 100
        do
            for ants in 100
            do

                python aco_solver/stats/avg_summary_generator.py $ants $iterations $CITY $DIRNAME $TYPE $POP

                TITLE=$(printf 'File: %s, Iterations: %d, Ants: %d, Population: %s' $CITY $iterations $ants $POP)
				FITNESS_FILENAME=$(printf 'outputs/zeus_wyniki_final/%s_%d_%d_%s_avg' $CITY $ants $iterations $POP)
				FITNESS_FILENAME_BC=$(printf 'outputs/zeus_wyniki_final/%s_%d_%d_%s_avg_with_bc' $CITY $ants $iterations $POP)
				PATH_FILENAME=$(printf 'outputs/zeus_wyniki_final/%s_%d_%d_%s_path' $CITY $ants $iterations $POP)

                gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single.plt
				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME_BC.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single_bc.plt
				gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATH_FILENAME.dat'; OUTPUTFILE='$PATH_FILENAME.pdf'" scripts/plot/path.plt

				TITLE2=$(printf 'File: %s, Iterations: %d, Ants: %d, Population: %s' $CITY $iterations $ants $POP)
			    AVG_FILENAME=$(printf 'outputs/zeus_wyniki_final/%s_%d_%d_%s_avg_summary' $CITY $ants $iterations $POP)

			    gnuplot -e "TITLE='$TITLE2'; FILENAME='$AVG_FILENAME.dat'; OUTPUTFILE='$AVG_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/fitness_avg.plt
            done
        done
	done
done

