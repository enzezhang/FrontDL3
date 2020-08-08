#!/bin/bash

rm gmt.* 
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4
gmt gmtset PS_MEDIA = 60cx50c
gmt gmtset FONT_ANNOT_SECONDARY=+7p,Helvetica,black

path=/Users/EnzeZhang/data/figure_RGC/all_glacier_figure1

file_result=$path/all_glacier.txt
PS=$path/Kanger_result.ps



J=M8.3

R=-33.05/-32.71/68.52/68.63

imagename=$path/20150130_hh_GEE_sentinel_GRD_IW_kanger_stretch.grd
calving_line=$path/20150130_hh_GEE_sentinel_GRD_IW_kanger_stretch.gmt

gmt grd2cpt -Cgray $imagename > sar.cpt

gmt psbasemap -J$J -R$R -K -V  -P -Ba0 -Y3.87i > $PS

gmt grdimage $imagename -R$R -J$J -Csar.cpt -O -Q -K >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS

# gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
# gmt psbasemap -J$J -R$R -Lg-32.95/68.55+c-32.88+w4k+u+f -F+gwhite -O -K -V -P >> $PS
# #gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black

echo -32.95 68.623 Kangerdlugssuaq |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -32.95 68.61 Sentinel-1 |gmt pstext -J$J -R$R -O -F+f15p,0,black -Wwhite -Gwhite -C10%/10% -TO >>$PS

# gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSne >> $PS
gmt psconvert -E400 -A -Tg $PS




