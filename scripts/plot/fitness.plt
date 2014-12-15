set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
set title TITLE
set terminal png linewidth 2 size 1366,720
set output OUTPUTFILE
plot FILENAME u 1:2 every ::4 w l, \
     "" u 1:3 every ::4 w l, \
     "" u 1:4 every ::4 w l, \
     "" u 1:6 every ::4 w l, \
     "" u 1:7 every ::4 w l
