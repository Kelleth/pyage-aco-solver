#!/bin/bash

module load libs/python-numpy
cd ~/pyage-aco-solver/

CITIES=$1
for iterations in 20 50 100
do
	for ants in 100
	do
		for type in ca
		do
            tests=1

            #### example parametrized entry - just copy and paste it below to run aditional entry with different params ####

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %f, Altercentic: %f, GoodConflict: %f, BadConflict: %f, Classic: %f' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 30 -t $type -q 1 -o $DIRNAME


            let 'tests++'

            #### example parametrized entry - end ####
		done
	done
done
