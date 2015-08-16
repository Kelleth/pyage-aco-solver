set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
#set xrange [1:100]
#set yrange [7000:33000]
set autoscale y
set autoscale x
set title TITLE font "Verdana,40" 
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,25'
set output OUTPUTFILE
plot FILENAME u 1:2 every ::4 w l linetype 1 lc rgb 'red' notitle, \
     "" u 1:4 every ::4 w l linetype 2 lc rgb 'green' notitle, \
     "" u 1:6 every ::4 w l linetype 3 lc rgb 'black' notitle, \
     "" u 1:8 every ::4 w l linetype 4 lc rgb 'blue' notitle, \
     "" u 1:10 every ::4 w l linetype 5 lc rgb 'magenta' notitle, \
     "" u 1:2:3 every ::4 w yerrorbars linetype 1 lc rgb 'red', \
     "" u 1:4:5 every ::4 w yerrorbars linetype 2 lc rgb 'green', \
     "" u 1:6:7 every ::4 w yerrorbars linetype 3 lc rgb 'black', \
     "" u 1:8:9 every ::4 w yerrorbars linetype 4 lc rgb 'blue', \
     "" u 1:10:11 every ::4 w yerrorbars linetype 5 lc rgb 'magenta', \
     OPTIMAL+0 w l linetype 5 lc rgb 'gray' title "TSPLIB"
