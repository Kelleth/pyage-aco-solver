set key autotitle columnheader
set datafile separator ","
set xlabel "Iteration"
set ylabel "Population Size"
#set xrange [1:100]
set yrange [0:100]
set autoscale x
set tics scale 2
set title TITLE font "Verdana,40"
set key left top
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
plot FILENAME u 1:2 w l linetype 1 lc rgb 'red' notitle, \
     "" u 1:4 w l linetype 2 lc rgb 'green' notitle, \
     "" u 1:6 w l linetype 3 lc rgb 'blue' notitle, \
     "" u 1:8 w l linetype 4 lc rgb 'magenta' notitle, \
     "" u 1:10 w l linetype 5 lc rgb 'black' notitle, \
     "" u 1:2:3 w yerrorbars linetype 1 lc rgb 'red' title 'AC', \
     "" u 1:4:5 w yerrorbars linetype 2 lc rgb 'green' title 'BC', \
     "" u 1:6:7 w yerrorbars linetype 3 lc rgb 'blue' title 'CA', \
     "" u 1:8:9 w yerrorbars linetype 4 lc rgb 'magenta' title 'EC', \
     "" u 1:10:11 w yerrorbars linetype 5 lc rgb 'black' title 'GC'