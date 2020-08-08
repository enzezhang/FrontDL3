#!/bin/bash

rm gmt.* 

#bash /home/zez/data1/Landsat8/Helheim/script/result_plot.sh /home/zez/data1/Landsat8/Helheim/grd_non_stretch/20150411_232013_crop_landsat_Helheim.grd /home/zez/data1/test20/in_polygon_gmt_Helheim_test_Apr2/20150411_232013_crop_landsat_Helheim.gmt 20150411 /home/zez/data1/Landsat8/Helheim/figure/test_Apr2/20150411_232013_crop_landsat_Helheim.ps
imagename=/home/zez/data2/calving_front_deep_learning/figure/artifact/20140404_003_TSX_Helheim_stretch.grd
calving_line=/home/zez/data2/calving_front_deep_learning/figure/artifact/20140404_003_TSX_Helheim_stretch.gmt
date=20140404
PS=artifact.ps
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4

R=-38.23/-38.02/66.32/66.41
J=M8.3



gmt psbasemap -J$J -R$R -K -V -P -Ba0 > $PS
pwd
#echo "gmt grd2cpt $imagename -R$R -Cgray -Z > sar1.cpt"
#rm sar1.cpt
#gmt makecpt -Cgray -T0/500/50 > sar1.cpt
gmt grd2cpt $imagename -R$R -Cgray > sar1.cpt

gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS

#gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
gmt psbasemap -J$J -R$R -Lg-38.18/66.33+c-38.175+w4k+u+f -F+gwhite -O -K -V -P >> $PS

echo $date

echo -38.22 66.405 \(a\) |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.18 66.388 $date |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.18 66.402 Helheim |gmt pstext -J$J -R$R -O -F+f14p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.18 66.395 TerraSAR-X |gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS
#echo -38.0835 66.394 Fig b |gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
gmt psxy -J$J -R$R -O -K -W2p,blue >> $PS <<EOF
-38.107 66.368
-38.057 66.368
-38.057 66.3895
-38.107 66.3895
-38.107 66.368
EOF

gmt psxy -J$J -R$R -O -K -W2p,blue >> $PS <<EOF
-38.057 66.368
-38.02 66.32
EOF
gmt psxy -J$J -R$R -O -K -W2p,blue >> $PS <<EOF
-38.057 66.3895
-38.02 66.41
EOF


gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSen -K >> $PS



R=-38.107/-38.057/66.368/66.38935
J=M8.33

gmt psbasemap -J$J -R$R -K -V -P -Ba0 -O -X3.29i >> $PS
#gmt grd2cpt $imagename -R$R -Cgray > sar1.cpt
gmt grdimage $imagename -R$R -J$J -Csar1.cpt -K -O -Q >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
echo -38.061 66.388 \(b\) |gmt pstext -J$J -R$R -O -F+f14p,0,black -Wwhite -Gwhite -C10%/10% -TO >>$PS
gmt psconvert -E300 -A+s20c -Tg $PS
