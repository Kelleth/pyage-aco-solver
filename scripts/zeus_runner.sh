#!/bin/bash

module load libs/boost/1.52.0
module load gnuplot
cd ~/io/

CITIES=$1
for iterations in 100
do
	for ants in 20
	do
		for type in cs ac gc
		do
			TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
			FILENAME=$(printf 'outputs/%s_%d_%d_%s' $CITIES $ants $iterations $type)
			PATHFILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 12 -t $type -q 1
			gnuplot -e "TITLE='$TITLE'; FILENAME='$FILENAME.dat'; OUTPUTFILE='$FILENAME.png'" scripts/plot/fitness.plt
			gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATHFILENAME.dat'; OUTPUTFILE='$PATHFILENAME.png'" scripts/plot/path.plt
		done

		for type in ca
		do
			TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
			FILENAME=$(printf 'outputs/%s_%d_%d_%s' $CITIES $ants $iterations $type)
			PATHFILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 12 -t $type -q 1
			gnuplot -e "TITLE='$TITLE'; FILENAME='$FILENAME.dat'; OUTPUTFILE='$FILENAME.png'" scripts/plot/fitness_ca.plt
			gnuplot -e "TITLE='Path for: $TITLE'; FILENAME='$PATHFILENAME.dat'; OUTPUTFILE='$PATHFILENAME.png'" scripts/plot/path.plt
		done
	done
done
