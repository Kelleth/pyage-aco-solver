set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
set autoscale y
set title TITLE font "Verdana,40" 
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,25'
set output OUTPUTFILE
plot FILENAME u 1:2 w l linetype 1 lc rgb 'red' notitle, \
     "" u 1:2:3 w yerrorbars linetype 1 lc rgb 'red' title "FITNESS", \
     OPTIMAL+0 w l linetype 6 lc rgb 'gray' title "TSPLIB"
