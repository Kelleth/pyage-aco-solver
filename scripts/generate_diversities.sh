#!/bin/bash
cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)
optimum_arr=(426 7542 29437 538 21282 22068 14379 49135 108159 2323 675 126643)

cd ../

for i in 0 1
do
	CITIES=${cities_arr[i]}
	OPTIMAL=${optimum_arr[i]}
	for iterations in 100
	do
		for ants in 100
		do
			for type in eq
			do
			    for k in 2
			    do
                    TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
                    NAME='eq'

                    DIVERSITY_FILENAME=$(printf 'outputs/parametrized_probability/%s_%d_%d_%s_diversity' $CITIES $ants $iterations $type)
                    DIVERSITY_FILENAME2=$(printf 'outputs/ca_results/%s_%d_%d_ca_diversity' $CITIES $ants $iterations)
                    gnuplot -e "NAME='$NAME'; TITLE='Diversity'; FILENAME='$DIVERSITY_FILENAME.dat'; FILENAME2='$DIVERSITY_FILENAME2.dat'; OUTPUTFILE='$DIVERSITY_FILENAME.pdf';" scripts/plot/diversity.plt

                    AVG_ATTRACTIVENESS_FILENAME=$(printf 'outputs/parametrized_probability/%s_%d_%d_%s_attractiveness_avg_std' $CITIES $ants $iterations $type)
                    AVG_ATTRACTIVENESS_FILENAME2=$(printf 'outputs/ca_results/%s_%d_%d_ca_attractiveness_avg_std' $CITIES $ants $iterations)
                    gnuplot -e "NAME='$NAME'; TITLE='Attractiveness'; FILENAME='$AVG_ATTRACTIVENESS_FILENAME.dat'; FILENAME2='$AVG_ATTRACTIVENESS_FILENAME2.dat'; OUTPUTFILE='$AVG_ATTRACTIVENESS_FILENAME.pdf';" scripts/plot/attractiveness.plt

                    ATTRACTIVENESS_RATIO_FILENAME=$(printf 'outputs/parametrized_probability/%s_%d_%d_%s_attractiveness_ratio' $CITIES $ants $iterations $type)
                    ATTRACTIVENESS_RATIO_FILENAME2=$(printf 'outputs/ca_results/%s_%d_%d_ca_attractiveness_ratio' $CITIES $ants $iterations)
                    gnuplot -e "NAME='$NAME'; TITLE='Attractiveness ratio'; FILENAME='$ATTRACTIVENESS_RATIO_FILENAME.dat'; FILENAME2='$ATTRACTIVENESS_RATIO_FILENAME2.dat'; OUTPUTFILE='$ATTRACTIVENESS_RATIO_FILENAME.pdf';" scripts/plot/attractiveness_ratio.plt
			    done
			done
		done
	done
done