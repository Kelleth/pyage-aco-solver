set datafile separator ","
set xlabel "Iteration"
set ylabel "Pheromone Ratio"
set autoscale x
set autoscale y
set tics scale 2
#set title TITLE font "Verdana,40"
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
plot FILENAME u 1:2 w l linetype 1 lc rgb 'red' notitle, \
     "" u 1:2:3 every ::1 w yerrorbars linetype 1 lc rgb 'red' title NAME, \
     FILENAME2 u 1:2 w l linetype 1 lc rgb 'blue' notitle, \
     "" u 1:2:3 every ::1 w yerrorbars linetype 1 lc rgb 'blue' title "ca"
