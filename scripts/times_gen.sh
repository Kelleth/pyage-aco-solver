#!/bin/bash
cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)

cd ../aco_solver/stats/

for i in 0 1
do
    CITIES=${cities_arr[i]}
    for iteration in 100
    do
        for ants in 100
        do
            python times_assembler.py 100 $iteration $CITIES ../../outputs/
        done
    done
done