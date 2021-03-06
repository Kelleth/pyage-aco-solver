#!/bin/bash

cd ..

CITIES=$1
for iterations in 100
do
	for ants in 100
	do
	    for type in pc
		do
            tests=1

            #### example parametrized entry - just copy and paste it below to run aditional entry with different params ####

            #quantities of ants
            egocentric=0.25
            altercentric=0.25
            goodConflict=0.25
            badConflict=0.25
            classic=0.00

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %f, Altercentic: %f, GoodConflict: %f, BadConflict: %f, Classic: %f' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --paremetrizedName a

            let 'tests++'

            #### example parametrized entry - end ####

	    done
	done
done
