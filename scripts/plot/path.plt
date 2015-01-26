set datafile separator ";"
set title TITLE font "Verdana,40" 
set terminal pdf color linewidth 6 size 16,9 enhanced font 'Verdana,25'
set output OUTPUTFILE
plot FILENAME u 1:2 w linespoints ls 1 pt 6 notitle
