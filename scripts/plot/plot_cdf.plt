set key autotitle columnheader
set xlabel "Final fitness"
set ylabel "Probability"
set autoscale y
set autoscale x
set title TITLE font "Verdana,40" 
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,25'
set output OUTPUTFILE
plot FILENAME u 1:(1./30.) smooth cumulative lc rgb 'red' notitle