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
			FILENAME=$(printf 'outputs/%s_%d_%d_%s.dat' $CITIES $ants $iterations $type)
			OUTPUTFILE=$(printf 'outputs/%s_%d_%d_%s.png' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 12 -t $type -q 1
			gnuplot -e "TITLE='$TITLE'; FILENAME='$FILENAME'; OUTPUTFILE='$OUTPUTFILE'" plot.plt
		done

		for type in ca
		do
			TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
			FILENAME=$(printf 'outputs/%s_%d_%d_%s.dat' $CITIES $ants $iterations $type)
			OUTPUTFILE=$(printf 'outputs/%s_%d_%d_%s.png' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 12 -t $type -q 1
			gnuplot -e "TITLE='$TITLE'; FILENAME='$FILENAME'; OUTPUTFILE='$OUTPUTFILE'" plot_ca.plt
		done
	done
done
