reset
set term png
set term png size 1024, 768
set output 'time_plot.png'

# color definitions
set border linewidth .5
set style line 1 lc rgb '#6699cc' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 2 lc rgb '#0e8466' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 3 lc rgb '#c8b03e' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 4 lc rgb '#9d64a2' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 5 lc rgb '#ff9933' lt 1 lw 2 pt 7 pi -1 ps 1
set pointintervalbox 1

# unset key
# set xrange [0:5]
# set yrange [0:4]

set title "Average Run Time (sigma = 10)";
set xlabel "Input size"
set ylabel "Average run time in seconds"
plot 'time_data.txt' using 1:2 title 'Traditional' with linespoints ls 1, \
    'time_data.txt' using 1:3 title 'Mid-neighbour' with linespoints ls 2, \
    'time_data.txt' using 1:6 title 'MBB' with linespoints ls 5, \
    #'time_data.txt' using 1:5 title 'MPB' with linespoints ls 4
    #'time_data.txt' using 1:4 title 'UPB' with linespoints ls 3, \
unset multiplot
