#!/bin/bash

rm gmt.* 

#bash /home/zez/data1/Landsat8/Helheim/script/result_plot.sh /home/zez/data1/Landsat8/Helheim/grd_non_stretch/20150411_232013_crop_landsat_Helheim.grd /home/zez/data1/test20/in_polygon_gmt_Helheim_test_Apr2/20150411_232013_crop_landsat_Helheim.gmt 20150411 /home/zez/data1/Landsat8/Helheim/figure/test_Apr2/20150411_232013_crop_landsat_Helheim.ps
imagename=$1
calving_line=$2
date=$3
PS=$4
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-38.28/-38.07/66.32/66.41
J=M16



gmt psbasemap -J$J -R$R -K -V -P -Ba0 > $PS
pwd
#echo "gmt grd2cpt $imagename -R$R -Cgray -Z > sar1.cpt"
#rm sar1.cpt
#gmt makecpt -Cgray -T0/500/50 > sar1.cpt
gmt grd2cpt $imagename -R$R -Cgray > sar1.cpt

gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS

gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS

gmt psbasemap -J$J -R$R -Lg-38.23/66.388+c-38.175+w4k+u+f -F+gwhite -O -K -V -P >> $PS

echo $date


echo -38.23 66.378 $date |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.402 Helheim |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.395 Sentinel-1|gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS
gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSen >> $PS
