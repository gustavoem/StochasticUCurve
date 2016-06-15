reset
set term png
set term png size 1024, 768
set output 'pc_evaluations_plot.png'

# color definitions
set border linewidth .5
set style line 1 lc rgb '#6699cc' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 2 lc rgb '#0e8466' lt 1 lw 2 pt 7 pi -1 ps 1
set style line 3 lc rgb '#c8b03e' lt 1 lw 2 pt 7 pi -1 ps 1
set pointintervalbox 1

# unset key
# set xrange [0:5]
# set yrange [0:4]

set title "Percentage of chain evaluated";
set xlabel "Max input size"
plot 'pc_evaluations_data.txt' using 1:2 title 'Pc = 0.70' with linespoints ls 1, \
    'pc_evaluations_data.txt' using 1:3 title 'Pc = 0.80' with linespoints ls 2, \
    'pc_evaluations_data.txt' using 1:4 title 'Pc = 0.90' with linespoints ls 3
unset multiplot
