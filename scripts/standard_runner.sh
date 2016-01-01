#!/bin/bash

#cd ~/pyage-aco-solver/
cd ..

CITIES=$1
for iterations in 1000
do
	for ants in 20 #10 20 50 100
	do
		for type in cs ca #la ha ca
		do
			TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d' $CITIES $type $iterations $ants)
			FILENAME=$(printf 'outputs/%s_%d_%d_%s' $CITIES $ants $iterations $type)
			PATHFILENAME=$(printf 'outputs/%s_%d_%d_%s_path' $CITIES $ants $iterations $type)

			python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type
		done
		for type in pc
		do
		    #clean populations
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 1.0 --altercentric 0.0 --goodConflict 0.0 --badConflict 0.0  --paremetrizedName egocentric
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.0 --altercentric 1.0 --goodConflict 0.0 --badConflict 0.0  --paremetrizedName altercentric
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.0 --altercentric 0.0 --goodConflict 1.0 --badConflict 0.0  --paremetrizedName goodAtConflict
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.0 --altercentric 0.0 --goodConflict 0.0 --badConflict 1.0  --paremetrizedName badAtConflict
		    #with bad at conflict
		    python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.25 --altercentric 0.25 --goodConflict 0.25 --badConflict 0.25  --paremetrizedName eq
		    python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.55 --altercentric 0.15 --goodConflict 0.15 --badConflict 0.15  --paremetrizedName ego
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.15 --altercentric 0.55 --goodConflict 0.15 --badConflict 0.15  --paremetrizedName alter
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.15 --altercentric 0.15 --goodConflict 0.55 --badConflict 0.15  --paremetrizedName good
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.15 --altercentric 0.15 --goodConflict 0.15 --badConflict 0.55  --paremetrizedName bad
		    #without bad at conflict
		    python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.34 --altercentric 0.33 --goodConflict 0.33 --badConflict 0.0  --paremetrizedName eqWithoutBad
		    python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.60 --altercentric 0.20 --goodConflict 0.20 --badConflict 0.0  --paremetrizedName egoWithoutBad
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.20 --altercentric 0.60 --goodConflict 0.20 --badConflict 0.0  --paremetrizedName alterWithoutBad
		    #python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 10 -t $type --egocentric 0.20 --altercentric 0.20 --goodConflict 0.60 --badConflict 0.0  --paremetrizedName goodWithoutBad
		done
	done
done
