#!/bin/bash
cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)
optimum_arr=(426 7542 29437 538 21282 22068 14379 49135 108159 2323 675 126643)

cd ../

for i in 0 1 2 3 4 5 6 7 8 9 10 11
do
	CITIES=${cities_arr[i]}
	OPTIMAL=${optimum_arr[i]}
	for iterations in 20 50 100
	do
		for ants in 100
		do
			TITLE=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
			#AVG_GLOBAL_FILENAME=$(printf 'outputs/%s_%d_%d_avg_box_and_whiskers_global_merged' $CITIES $ants $iterations)
			#echo $AVG_GLOBAL_FILENAME
			AVG_LAST_ITER_FILENAME=$(printf 'outputs/%s_%d_%d_avg_box_and_whiskers_last_iter_merged' $CITIES $ants $iterations)
			echo $AVG_LAST_ITER_FILENAME
			#gnuplot -e "TITLE='$TITLE'; FILENAME='$AVG_GLOBAL_FILENAME.dat'; OUTPUTFILE='$AVG_GLOBAL_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/box_and_whiskers_global.plt
			gnuplot -e "TITLE='$TITLE'; FILENAME='$AVG_LAST_ITER_FILENAME.dat'; OUTPUTFILE='$AVG_LAST_ITER_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/box_and_whiskers_global.plt
		done
	done
done