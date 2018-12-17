#!/bin/bash

if [ $# -ne 2 ]; then
    echo "***************************
Usage:                  
$0 input_file num_sites 
Example:		  
$0 output.txt 26	  
***************************"
else
    input_file=$1
    num_sites=$2


    grep -A $num_sites Initial $input_file | sed 's/: /,/g' | sed 's/, /,/g' | sed 's/ /,/g' | sed 's/,/	/g' > initial.tmp
    grep -A $num_sites Finished $input_file | sed 's/: /,/g' | sed 's/, /,/g' | sed 's/ /,/g' | sed 's/,/	/g'> finished.tmp

    echo "set xtics font 'Arial,18′
set terminal pdf solid font 'Arial,12' # pdf files are great for inkscape
set output 'plot.pdf'
set size square
unset label # Remove all labels
unset xtics; unset ytics # Remove all tics
set ytics nomirror # Only have tics on left
set xtics nomirror # Only have tics on bottom
set border 3 # Only have border on bottom and left
set xrange [0:360]
set yrange [0:360]
set xtics 0,30,360
set ytics 0,30,360
set xlabel \"Chi2\" offset -2
set ylabel \"Chi1\" offset 2
plot 'finished.tmp' using (\$6 <0 ? \$6+360 : \$6):(\$4 <0 ? \$4+360 : \$4):(sprintf(\"(N%d)\", \$2)) with labels point pt 7 ps 0.5 lt rgb \"red\" offset char 0.5,0.5 notitle" > gnuplot.in
gnuplot -p gnuplot.in
rm *.tmp gnuplot.in
    #plot 'finished.tmp' using 4:6 title \"\" with points lw 4 # lw = linewidth" > gnuplot.in

    # set ylabel \"Overlap (Å^2)\" offset 2
    # set xrange [-180:180]
fi 
