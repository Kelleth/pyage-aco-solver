#!/bin/bash

cd ~/pyage-aco-solver/

CITIES=$1
for iterations in 100
do
	for ants in 20 50 100
	do
		for type in cs ac gc ca
		do
			TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
			FILENAME=$(printf 'outputs/%s_%d_%d_%s' $CITIES $ants $iterations $type)
			PATHFILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1
		done
	done
done
