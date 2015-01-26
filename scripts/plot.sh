#!/bin/bash
#              0        1    2    3    4      5       6       7      8      9      10    11
cities_arr=(berlin52 eil51 eil76 pr76 st70 kroA100 kroE100 lin105 rat195 kroB200 ts225 att532)
optimum_arr=(7542 426 538 108159 675 21282 22068 14379 2323 29437 126643 27686)

cd ~/pyage-aco-solver/

for i in 0 1 2
do
	CITIES=${cities_arr[i]}
	OPTIMAL=${optimum_arr[i]}
	for iterations in 100
	do
		for ants in 20 50 100
		do
			for type in cs la ha
			do
				TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
				FITNESS_FILENAME=$(printf 'outputs/%s_%d_%d_%s_avg' $CITIES $ants $iterations $type)
				FITNESS_FILENAME_BC=$(printf 'outputs/%s_%d_%d_%s_avg_with_bc' $CITIES $ants $iterations $type)
				PATH_FILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)

				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single.plt
				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME_BC.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single_bc.plt
				gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATH_FILENAME.dat'; OUTPUTFILE='$PATH_FILENAME.pdf'" scripts/plot/path.plt
			done
			TITLE2=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
			AVG_FILENAME=$(printf 'outputs/%s_%d_%d_avg_summary' $CITIES $ants $iterations)
			gnuplot -e "TITLE='$TITLE2'; FILENAME='$AVG_FILENAME.dat'; OUTPUTFILE='$AVG_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/fitness_avg.plt
		done
	done
done
