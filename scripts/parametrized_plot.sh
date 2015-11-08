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
			for type in awithout
			do
				TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
				FITNESS_FILENAME=$(printf 'outputs/%s_%d_%d_%s_avg' $CITIES $ants $iterations $type)
				FITNESS_FILENAME_BC=$(printf 'outputs/%s_%d_%d_%s_avg_with_bc' $CITIES $ants $iterations $type)
				PATH_FILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)
				NAME='awithout'
				
				DIVERSITY_FILENAME=$(printf 'outputs/parametrized_1/%s_%d_%d_%s_diversity' $CITIES $ants $iterations $type)
				DIVERSITY_FILENAME2=$(printf 'outputs/parametrized_1/%s_%d_%d_ca_diversity' $CITIES $ants $iterations)
				gnuplot -e "NAME='$NAME'; TITLE='Diversity'; FILENAME='$DIVERSITY_FILENAME.dat'; FILENAME2='$DIVERSITY_FILENAME2.dat'; OUTPUTFILE='$DIVERSITY_FILENAME.pdf';" scripts/plot/diversity.plt
				
				AVG_ATTRACTIVENESS_FILENAME=$(printf 'outputs/parametrized_1/%s_%d_%d_%s_attractiveness_avg_std' $CITIES $ants $iterations $type)
				AVG_ATTRACTIVENESS_FILENAME2=$(printf 'outputs/parametrized_1/%s_%d_%d_ca_attractiveness_avg_std' $CITIES $ants $iterations)
				gnuplot -e "NAME='$NAME'; TITLE='Attractiveness'; FILENAME='$AVG_ATTRACTIVENESS_FILENAME.dat'; FILENAME2='$AVG_ATTRACTIVENESS_FILENAME2.dat'; OUTPUTFILE='$AVG_ATTRACTIVENESS_FILENAME.pdf';" scripts/plot/attractiveness.plt

				ATTRACTIVENESS_RATIO_FILENAME=$(printf 'outputs/parametrized_1/%s_%d_%d_%s_attractiveness_ratio' $CITIES $ants $iterations $type)
				ATTRACTIVENESS_RATIO_FILENAME2=$(printf 'outputs/parametrized_1/%s_%d_%d_ca_attractiveness_ratio' $CITIES $ants $iterations)
				gnuplot -e "NAME='$NAME'; TITLE='Attractiveness ratio'; FILENAME='$ATTRACTIVENESS_RATIO_FILENAME.dat'; FILENAME2='$ATTRACTIVENESS_RATIO_FILENAME2.dat'; OUTPUTFILE='$ATTRACTIVENESS_RATIO_FILENAME.pdf';" scripts/plot/attractiveness_ratio.plt
				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single.plt
				gnuplot -e "TITLE='$TITLE'; FILENAME='$FITNESS_FILENAME.dat'; OUTPUTFILE='$FITNESS_FILENAME_BC.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/avg_single_bc.plt
				gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATH_FILENAME.dat'; OUTPUTFILE='$PATH_FILENAME.pdf'" scripts/plot/path.plt
			done
			TITLE2=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
			AVG_FILENAME1=$(printf 'outputs/%s_%d_%d_ca_avg_summary' $CITIES $ants $iterations)
			AVG_FILENAME2=$(printf 'outputs/%s_%d_%d_awithout_avg_summary' $CITIES $ants $iterations)
			AVG_FILENAME=$(printf 'outputs/%s_%d_%d_avg_summary' $CITIES $ants $iterations)
			gnuplot -e "TITLE='$TITLE2'; FILENAME='$AVG_FILENAME1.dat'; OUTPUTFILE='$AVG_FILENAME1.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/fitness_avg.plt
			gnuplot -e "TITLE='$TITLE2'; FILENAME1='$AVG_FILENAME1.dat'; FILENAME2='$AVG_FILENAME2.dat'; OUTPUTFILE='$AVG_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/fitness2_avg.plt
		done
	done
done