#!/bin/bash

#module load libs/python-numpy
cd ..

CITIES=$1
for iterations in 100
do
	for ants in 20
	do
		for type in ca
		do
            tests=1
            for alpha in 3.0
            do
                for beta in 2.0
                do
                    for rho in 0.05
                    do
                        for Q in 2.0
                        do
                            #### example parametrized entry - just copy and paste it below to run aditional entry with different params ####

                            TITLE=$(printf 'File: %s, Type: %s, Iterations: %d, Ants: %d, Egocentic: %f, Altercentic: %f, GoodConflict: %f, BadConflict: %f, Classic: %f' $CITIES $type $iterations $ants $egocentric $altercentric $goodConflict $badConflict $classic)
                            DIRNAME=$(printf 'outputs/parametrized_%d/' $tests)

                            python -m aco_solver.runner.parallel_runner $ants $iterations $CITIES -p 8 -t $type -o $DIRNAME -a $alpha -b $beta -r $rho -q $Q
                            echo "test_no: $tests, alpha: $alpha, beta: $beta, rho: $rho, Q: $Q" > outputs/parametrized_$tests/parameters.conf


                            let 'tests++'
                        done
                    done
                done
            done
            #### example parametrized entry - end ####
		done
	done
done
