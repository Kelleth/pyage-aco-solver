#!/bin/bash
#cities_arr=(eil51 berlin52 kroB200 eil76 kroA100 kroE100 lin105 pr264 pr76 rat195 st70 ts225)
#optimum_arr=(426 7542 29437 538 21282 22068 14379 49135 108159 2323 675 126643)
cities_arr=(kra30a nug7 nug8 nug12 nug5 nug6 wil50 tai5a tai10a tai10b tai12a tai12b tai15a tai15b)
optimum_arr=(88900 148 214 578 50 86 48816 12902 135028 1183760 224416 39464925 388214 51765268)

cd ../
for population in ca #cs ca ego eq egoWithoutBad eqWithoutBad #cs la ha ca egocentric altercentric goodAtConflict badAtConflict eq ego alter good bad eqWithoutBad egoWithoutBad alterWithoutBad goodWithoutBad
do
    for i in 6 #8 9 10 11 12 13 # 7 #1 2 3 4 5 #4 7 #2 3
    do
        CITIES=${cities_arr[i]}
        OPTIMAL=${optimum_arr[i]}
        for iterations in 100
        do
            for ants in 20 #1 2 3 4 5 #50 100
            do
                #for j in {5..6}
                #do
                    TITLE=$(printf 'File: %s, Iterations: %d, Ants: %d' $CITIES $iterations $ants)
                    AVG_GLOBAL_FILENAME=$(printf 'outputs/%s_%d_%d_%s_avg_summary' $j $CITIES $ants $iterations $population)
                    BAW_THROUGH_FILENAME=$(printf 'outputs/%s_%d_%d_%s_baw_summary' $j $CITIES $ants $iterations $population)
                    #AVG_LAST_ITER_FILENAME=$(printf 'outputs/%s_%d_%d_avg_box_and_whiskers_last_iter_merged' $CITIES $ants $iterations)
                    #echo $AVG_LAST_ITER_FILENAME
                    gnuplot -e "TITLE='$TITLE'; FILENAME='$AVG_GLOBAL_FILENAME.dat'; OUTPUTFILE='$BAW_THROUGH_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/box_and_whiskers_through.plt
                    #gnuplot -e "TITLE='$TITLE'; FILENAME='$AVG_LAST_ITER_FILENAME.dat'; OUTPUTFILE='$AVG_LAST_ITER_FILENAME.pdf'; OPTIMAL='$OPTIMAL'" scripts/plot/box_and_whiskers_global.plt
                #done
            done
        done
    done
done