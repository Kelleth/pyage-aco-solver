set datafile separator ";"
set xrange[-0.5:1.5]
#set yrange[0:1000]
#set autoscale x
set autoscale y
set xlabel "Population"
set ylabel "Fitness"
set tics scale 1.3
set xtics rotate by -45 #offset 0.0,-1.8
#set title TITLE font "Verdana,100" 
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE

# Data columns: X Min 1stQuartile Median 3rdQuartile Max Titles
set bars 4.0
set style fill empty
plot FILENAME using 1:5:4:7:6:xticlabels(2) with candlesticks title 'Quartiles' whiskerbars, \
	 '' using 1:8:8:8:8 with candlesticks lt -1 notitle, \
     OPTIMAL+0 w l linetype 5 lc rgb 'gray' title "TSPLIB"

