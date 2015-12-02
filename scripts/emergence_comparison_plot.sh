#!/bin/bash
#              0        1    2    3    4      5       6       7      8      9      10    11
cities_arr=(berlin52 eil51 eil76 pr76 st70 kroA100 kroE100 lin105 rat195 kroB200 ts225 att532)
optimum_arr=(7542 426 538 108159 675 21282 22068 14379 2323 29437 126643 27686)

cd ..

for i in 0 1 9
do
	CITIES=${cities_arr[i]}
	OPTIMAL=${optimum_arr[i]}
	for iterations in 100
	do
		for ants in 100
		do
			AVG_FILENAME=$(printf 'outputs/population_sizes/%s_%d_%d_a_avg_summary' $CITIES $ants $iterations)
			AVG_FILENAME2=$(printf 'outputs/population_sizes/%s_%d_%d_awithout_avg_summary' $CITIES $ants $iterations)
			AVG_FILENAME3=$(printf 'outputs/population_sizes/%s_%d_%d_ca_avg_summary' $CITIES $ants $iterations)
			gnuplot -e "TITLE='FITNESS WITH EMERGENCE'; FILENAME2='$AVG_FILENAME2.dat'; FILENAME3='$AVG_FILENAME3.dat'; FILENAME='$AVG_FILENAME.dat'; OUTPUTFILE='$AVG_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/emergence_comparison.plt
		done
	done
done
