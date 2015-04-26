#!/bin/bash

#cd ..

CITIES=$1
for iterations in 100
do
	for ants in 100
	do
	    for type in cs la ha ca
		do
            tests=3

            #### example parametrized entry - just copy and paste it below to run aditional entry with different params ####

            #quantities of ants
            egocentric=0.22
            altercentric=0.15
            goodConflict=0.45
            badConflict=0.18
            classic=0.00

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %s, Altercentic: %s, GoodConflict: %s, BadConflict: %s, Classic: %s' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --ecPheromoneFactor 14.0 --acPheromoneFactor 2.0 --gcPheromoneFactor 2.5 --bcPheromoneFactor 0.5
            #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic
            let 'tests++'

            #### example parametrized entry - end ####

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %s, Altercentic: %s, GoodConflict: %s, BadConflict: %s, Classic: %s' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --ecPheromoneFactor 14.0 --acPheromoneFactor 2.0 --gcPheromoneFactor 2.5 --bcPheromoneFactor 0.5
            #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic
            let 'tests++'

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %s, Altercentic: %s, GoodConflict: %s, BadConflict: %s, Classic: %s' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --ecPheromoneFactor 14.0 --acPheromoneFactor 2.0 --gcPheromoneFactor 2.5 --bcPheromoneFactor 0.5
            #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic
            let 'tests++'

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %s, Altercentic: %s, GoodConflict: %s, BadConflict: %s, Classic: %s' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --ecPheromoneFactor 14.0 --acPheromoneFactor 2.0 --gcPheromoneFactor 2.5 --bcPheromoneFactor 0.5
            #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic
            let 'tests++'

            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %s, Altercentic: %s, GoodConflict: %s, BadConflict: %s, Classic: %s' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)
            FILENAME=$(printf '%s%s_%d_%d_%s' $DIRNAME $CITIES $ants $iterations $type)
            PATHFILENAME=$(printf 'outputs/parametrized_%d/%s_%d_%d_%s_path' $tests $CITIES $ants $iterations $type)

            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic --ecPheromoneFactor 14.0 --acPheromoneFactor 2.0 --gcPheromoneFactor 2.5 --bcPheromoneFactor 0.5
            #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 4 -t $type -q 1 -o $DIRNAME --egocentric $egocentric --altercentric $altercentric --goodConflict $goodConflict --badConflict $badConflict --classic $classic
            let 'tests++'

	    done
	done
done
