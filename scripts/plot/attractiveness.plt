set datafile separator ","
set xlabel "Iteration"
set ylabel "Attractiveness Dispersion"
set autoscale x
set autoscale y
set tics scale 2
#set title TITLE font "Verdana,40"
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
plot FILENAME u 1:3 w l linetype 1 lc rgb 'red' title NAME, \
     FILENAME2 u 1:3 w l linetype 1 lc rgb 'blue' title "ca"
