set datafile separator ";"
set xrange[0:101]
set autoscale y
set xlabel "Iteration"
set ylabel "Fitness"
#set xtics rotate by -90 #offset 0.0,-1.8
set terminal pdf color linewidth 3 size 16,9 enhanced font 'Verdana,40'
set output OUTPUTFILE

# Data columns: X Min 1stQuartile Median 3rdQuartile Max Titles
set bars 1.0
set style fill empty

plot FILENAME using 1:5:4:8:6:xticlabels(1) with candlesticks title 'Quartiles' whiskerbars, \
    ''         using 1:7:7:7:7 with candlesticks lt -1 notitle, \
     OPTIMAL+0 w l linetype 5 lc rgb 'gray' title "QAPLIB"
