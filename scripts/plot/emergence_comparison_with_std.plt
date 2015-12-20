set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
#set xrange [1:100]
#set yrange [7000:14500]
set autoscale y
set autoscale x
set tics scale 2
#set title TITLE font "Verdana,40"
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
plot FILENAME u 1:2 w l linetype 1 lc rgb 'red' notitle, \
     "" u 1:2:3 every ::1 w yerrorbars linetype 1 lc rgb 'red' title 'emergenced', \
     FILENAME2 u 1:2 w l linetype 1 lc rgb 'blue' notitle, \
     "" u 1:2:3 every ::1 w yerrorbars linetype 1 lc rgb 'blue' title 'egoWithoutBad', \
     FILENAME3 u 1:2 w l linetype 1 lc rgb 'green' notitle, \
     "" u 1:2:3 every ::1 w yerrorbars linetype 1 lc rgb 'green' title 'ca', \
     OPTIMAL+0 w l linetype 6 lc rgb 'gray' title "TSPLIB"