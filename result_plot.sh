#!/bin/bash

rm gmt.* 

imagename=$1
calving_line=$2
date=$3
PS=$4
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-64.46/-64.21/76.33/76.39
J=M16



gmt psbasemap -J$J -R$R -K -V -P -Ba0 > $PS
pwd
#echo "gmt grd2cpt $imagename -R$R -Cgray -Z > sar1.cpt"
#rm sar1.cpt
#gmt makecpt -Cgray -T0/500/50 > sar1.cpt

gmt grd2cpt $imagename -R$R -Cgray > sar1.cpt

gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS



echo $date


echo -64.25 76.387 $date |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

gmt psbasemap -J$J -R$R -Lg-64.25/76.384+c-67.483+w2k+u+f -F+gwhite -O -K -V -P >> $PS

echo -64.25 76.380 GID_66 |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -64.25 76.377 Sentinel-2 |gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS

gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS


gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSen >> $PS
#gmt psconvert -E400 -A+s20c -Tg $PS
