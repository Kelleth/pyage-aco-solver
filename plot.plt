set key autotitle columnheader
set datafile separator ";"
set xlabel "Iteration"
set ylabel "Path length"
set title TITLE
set terminal png linewidth 2 size 1366,720
set output OUTPUTFILE
plot FILENAME u 2 w l, \
     "" u 3 w l, \
     "" u 4 w l, \
     "" u 6 w l, \
     "" u 7 w l
