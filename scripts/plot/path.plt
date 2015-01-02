set datafile separator ";"
set terminal png linewidth 2 size 1366,720
set title TITLE
set output OUTPUTFILE
plot FILENAME u 1:2 w linespoints ls 1 pt 6 notitle
