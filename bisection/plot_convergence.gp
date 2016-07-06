reset
set term png
set term png size 1024, 768
set output 'convergence_plot.png'

# color definitions
set border linewidth .5
set style line 1 lc rgb '#6699cc' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 2 lc rgb '#0e8466' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 3 lc rgb '#c8b03e' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 4 lc rgb '#9d64a2' lt 1 lw 2 pt 7 pi -1 ps 1
set pointintervalbox 1

# unset key
# set xrange [0:5]
# set yrange [0:4]

set title "Convergence for n = 1000 and sigma = 1";
set xlabel "Percentage of lg n as input size"
set ylabel "Average percentual distance to solution"
plot 'convergence_data.txt' using 1:2 title 'Traditional' with linespoints ls 1, \
    'convergence_data.txt' using 1:3 title 'Mid-neighbour' with linespoints ls 2, \
    'convergence_data.txt' using 1:4 title 'UPB' with linespoints ls 3, \
    'convergence_data.txt' using 1:5 title 'MUPB' with linespoints ls 4
unset multiplot
