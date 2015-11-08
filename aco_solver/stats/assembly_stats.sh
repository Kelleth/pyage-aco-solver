#!/bin/bash

for city in eil76 kroA100 kroE100 pr76 st70 lin105 rat195 ts225 pr264 eil51 berlin52 kroB200
do
	for iteration in 20 50 100
	do
		echo $iteration, $city
		python box_and_whiskers_data_assembler.py 100 $iteration $city ../../outputs/
	done
done