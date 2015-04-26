#!/bin/bash
cities_arr=(berlin52)
optimum_arr=(7542)



for i in 3 4 5 6 7
do
	CITIES=${cities_arr[0]}
	OPTIMAL=${optimum_arr[0]}
	for iterations in 100
	do
		for ants in 100
		do
			for type in cs la ha ca
			do
				TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
				FITNESS_FILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_avg' $i $CITIES $ants $iterations $type)
				FITNESS_FILENAME_BC=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_avg_with_bc' $i $CITIES $ants $iterations $type)
				PATH_FILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $i $CITIES $ants $iterations $type)

				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single.plt
				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME_BC.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single_bc.plt
				gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATH_FILENAME.dat'; OUTPUTFILE='$PATH_FILENAME.pdf'" scripts/plot/path.plt
			done
			TITLE2=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
			AVG_FILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_avg_summary' $i $CITIES $ants $iterations)
			echo $AVG_FILENAME
			gnuplot -e "TITLE='$TITLE2'; FILENAME='$AVG_FILENAME.dat'; OUTPUTFILE='$AVG_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/fitness_avg.plt
		done
	done
done