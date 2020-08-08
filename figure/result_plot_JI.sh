#!/bin/bash

rm gmt.* 

#bash /home/zez/test_deep_learning/u_net/figure/result_plot.sh /home/zez/data1/test16/grd/20090416.grd /home/zez/data1/test16/in_polygon_calving_front_Mar17/20090416.gmt 20090416 /home/zez/test_deep_learning/u_net/figure/result/20090416.ps
imagename=$1
calving_line=$2
date=$3
PS=$4
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-49.81/-49.5/69.11/69.26
J=M16



gmt psbasemap -J$J -R$R -K -V -P -Ba0 > $PS
gmt grdimage $imagename -R$R -J$J -Csar.cpt -K -O -Q >>$PS

gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS

gmt psbasemap -J$J -R$R -Lg-49.56/69.24+c-49.655+w4k+u+f -F+gwhite -O -K -V -P >> $PS

echo $date


echo -49.56 69.25 $date | gmt pstext -J$J -R$R -O -F+f30p,4,black -K -Wwhite -Gwhite -C20%/20% -TO >>$PS

gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSen >> $PS
