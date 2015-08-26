#!/bin/bash

probabilities=(0.0333333333 0.0666666667 0.1 0.1333333333 0.1666666667 0.2 0.2333333333 0.2666666667 0.3 0.3333333333 0.3666666667 0.4 0.4333333333 0.4666666667 0.5 0.5333333333 0.5666666667 0.6 0.6333333333 0.6666666667 0.7 0.7333333333 0.7666666667 0.8 0.8333333333 0.8666666667 0.9 0.9333333333 0.9666666667 1)
#move to outputs folder!!
for city in eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225
do
  for iterations in 20 50 100
  do
    for population in ca awithout
    do
      SORTED_DATA=()
      #read last iter fitness to array
      for no in {0..29}
      do
	FILENAME=$(printf '%s_100_%d_%s_%d.dat' $city $iterations $population $no)
	EACH=`tail -n-1 $FILENAME | awk -F";" '{min=9999999.0;if ($5!="" && $5<min)min=$5;if ($6!="" && $6<min)min=$6;if ($4!="" && $4<min)min=$4; print min}'`
	SORTED_DATA=(${SORTED_DATA[@]} $EACH)
      done
      #sort last iter fitness array
      SORTED_DATA=( $(
	for el in "${SORTED_DATA[@]}"
	do
	  echo "$el"
	done | sort) )
      #merge with probabilities
      OUTPUT=${SORTED_DATA[0]}"    "${probabilities[0]}
      for no in {1..29}
      do
	OUTPUT=$OUTPUT"\n"${SORTED_DATA[$no]}"    "${probabilities[$no]}
      done
      OUTPUT_FILE=$(printf '%s_100_%d_%s_last_iter_fitness.dat' $city $iterations $population)
      OUTPUT_PDF=$(printf '%s_100_%d_%s_last_iter_fitness.pdf' $city $iterations $population)
      echo -e $OUTPUT > $OUTPUT_FILE
      TITLE=$(printf 'CDF, File: %s, Type: %s, Iterations: %d, Ants: %d' $city $population $iterations 100)
      gnuplot -e "TITLE='$TITLE'; FILENAME='$OUTPUT_FILE'; OUTPUTFILE='$OUTPUT_PDF'" plot/plot_cdf.plt
    done
  done
done
