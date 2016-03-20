#!/bin/bash
cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)

cd ../

for i in 0 1
do
	CITIES=${cities_arr[i]}
	for iterations in 100
	do
		for ants in 100
		do
			    TITLE=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
			    TIMES_FILENAME=$(printf 'outputs/%s_%d_%d_merged_times' $CITIES $ants $iterations)
			    echo $TIMES_FILENAME
			    gnuplot -e "TITLE='$TITLE'; FILENAME='$TIMES_FILENAME.dat'; OUTPUTFILE='$TIMES_FILENAME.pdf';" scripts/plot/times.plt
		done
	done
done