#!/bin/bash
cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)
optimum_arr=(426 7542 29437 538 21282 22068 14379 49135 108159 2323 675 126643)

cd ../

for i in 1
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
				PATH_FILENAME=$(printf 'outputs/zeus_wyniki_final2/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)
				PATH_FILENAME2=$(printf 'outputs/zeus_wyniki_final2/%s_%d_%d_ca_path' $CITIES $ants $iterations)
				OUTPUT_FILENAME=$(printf 'outputs/zeus_wyniki_final2/%s_%d_%d_mixed_path' $CITIES $ants $iterations)

				gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATH_FILENAME.dat'; FILENAME2='$PATH_FILENAME2.dat'; OUTPUTFILE='$OUTPUT_FILENAME.pdf'" scripts/plot/path_with_ca.plt
			done
		done
	done
done