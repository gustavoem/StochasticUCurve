reset
set term png
set term png size 1024, 768
set output 'image_plot.png'

# remove axis
unset border
unset xtics
unset ytics

# color definitions
set border linewidth .5
set style line 1 lc rgb '#19194d' lt 1 lw 2 pt 7 pi -1 ps 1
set pointintervalbox 1

# unset key

set xrange [1:7]
set yrange [0:10]

plot 'curve_data.txt' using 1:2 title 'Node value' with linespoints ls 1, \
     '' using 1:2:3 title '' with labels offset 0, -3, char 1
unset multiplot
