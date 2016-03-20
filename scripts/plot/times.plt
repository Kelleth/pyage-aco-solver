set datafile separator ";"
set xlabel "Method"
set ylabel "Time"
#set xrange [1:100]
#set yrange [7000:14500]
set autoscale y
set xrange[-0.5:12.5]
set tics scale 1.3
set xtics rotate by -45 #offset 0.0,-1.8
#set title TITLE font "Verdana,40"
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE
plot FILENAME u 2:xticlabels(1) w l linetype 1 lc rgb 'red' notitle, \
     "" u 2:3 w yerrorbars linetype 1 lc rgb 'red' title "Time"