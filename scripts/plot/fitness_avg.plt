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
     "" u 1:9 w l linetype 2 lc rgb 'green' notitle, \
     "" u 1:16 w l linetype 3 lc rgb 'blue' notitle, \
     "" u 1:23 w l linetype 4 lc rgb 'magenta' notitle, \
     "" u 1:2:3 w yerrorbars linetype 1 lc rgb 'red', \
     "" u 1:9:10 w yerrorbars linetype 2 lc rgb 'green', \
     "" u 1:16:17 w yerrorbars linetype 3 lc rgb 'blue', \
     "" u 1:23:24 w yerrorbars linetype 4 lc rgb 'magenta', \
     OPTIMAL+0 w l linetype 6 lc rgb 'gray' title "TSPLIB"
