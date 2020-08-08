#!/bin/bash

rm gmt.* 


imagename=/home/zez/data2/calving_front_deep_learning/figure/large_calving_event/20180602_hh_GEE_sentinel_GRD_IW_helheim_stretch.tif
calving_line=/home/zez/data2/calving_front_deep_learning/figure/large_calving_event/20180602_hh_GEE_sentinel_GRD_IW_helheim_stretch.gmt
calving_line1=$calving_line
date=20180602
PS=large_calving_event.ps
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-38.28/-38.07/66.32/66.41
J=M8.3



gmt psbasemap -J$J -R$R -K -V -P -Ba0 > $PS
pwd
#echo "gmt grd2cpt $imagename -R$R -Cgray -Z > sar1.cpt"
#rm sar1.cpt
#gmt makecpt -Cgray -T0/500/50 > sar1.cpt

gmt grd2cpt $imagename  -Cgray > sar1.cpt

gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS

gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
gmt psbasemap -J$J -R$R -Lg-38.23/66.388+c-38.175+w4k+u+f -F+gwhite -O -K -V -P >> $PS

echo $date

echo -38.27 66.405 \(a\) |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.378 $date |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.402 Helheim |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.395 Sentinel-1 |gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS

gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSen -K >> $PS


imagename=/home/zez/data2/calving_front_deep_learning/figure/large_calving_event/20180606_hh_GEE_sentinel_GRD_IW_helheim_stretch.tif
calving_line=/home/zez/data2/calving_front_deep_learning/figure/large_calving_event/20180606_hh_GEE_sentinel_GRD_IW_helheim_stretch.gmt
date=20180606

gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-38.28/-38.07/66.32/66.41
J=M8.3



gmt psbasemap -J$J -R$R -K -V -P -Ba0 -O -X3.5i >> $PS
pwd
#echo "gmt grd2cpt $imagename -R$R -Cgray -Z > sar1.cpt"
#rm sar1.cpt
#gmt makecpt -Cgray -T0/500/50 > sar1.cpt
gmt grd2cpt $imagename -Cgray > sar1.cpt

gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS

gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
gmt psxy -R$R -J$J -A -W2p,blue,- $calving_line1 -K -O >>$PS
gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
gmt psbasemap -J$J -R$R -Lg-38.23/66.388+c-38.175+w4k+u+f -F+gwhite -O -K -V -P >> $PS

echo $date

echo -38.27 66.405 \(b\) |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.378 $date |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.402 Helheim |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.395 Sentinel-1|gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.12 66.35 Tabular iceberg| gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BSwen >> $PS
gmt psconvert -E300 -A+s20c -Tg $PS
