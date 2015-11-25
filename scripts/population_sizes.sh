#!/bin/bash

cd ..

for i in 20 50 100
do
    for city in eil51 berlin52
    do
        FILENAME=$(printf 'outputs/parametrized_1/population_sizes/%s_100_%d_a_population_sizes' $city $i)
        TITLE=$(printf 'Population sizes - %s 100 ants %d iterations' $city $i)
        gnuplot -e "TITLE='$TITLE'; FILENAME='$FILENAME.dat'; OUTPUTFILE='$FILENAME.pdf'; " scripts/plot/population_sizes.plt
    done
done