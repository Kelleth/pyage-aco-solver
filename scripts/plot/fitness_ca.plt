set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
set title TITLE
set terminal png linewidth 2 size 1366,720
set output OUTPUTFILE
plot FILENAME u 4 every ::4 w l, \
     "" u 5 every ::4 w l
