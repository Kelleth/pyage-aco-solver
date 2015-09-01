set datafile separator ";"
#set title TITLE font "Verdana,40"
set terminal pdf color linewidth 6 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
set tics scale 2
plot FILENAME u 1:2 w linespoints ls 1 pt 6 lc rgb "#900000ff" title 'awithout', \
     FILENAME2 u 1:2 w linespoints ls 1 pt 6 lc rgb "#90ff0000" title 'ca'
