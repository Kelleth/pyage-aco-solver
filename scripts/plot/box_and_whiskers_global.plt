set datafile separator ";"
set xrange[-0.5:11.5]
#set yrange[0:1000]
#set autoscale x
set autoscale y
set xlabel "Population"
set ylabel "Fitness"
set title TITLE font "Verdana,40" 
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,25'
set output OUTPUTFILE

# Data columns: X Min 1stQuartile Median 3rdQuartile Max Titles
set bars 4.0
set style fill empty
plot FILENAME using 1:4:5:8:6:xticlabels(2) with candlesticks title 'Quartiles' whiskerbars, \
	 '' using 1:7:7:7:7 with candlesticks lt -1 notitle, \
     OPTIMAL+0 w l linetype 5 lc rgb 'gray' title "TSPLIB"