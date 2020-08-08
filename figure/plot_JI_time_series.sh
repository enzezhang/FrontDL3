#!/bin/bash
#rm gmt.conf
gmt gmtset PS_MEDIA = 90cx120c
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +22p,Helvetica,black
gmt gmtset FONT_ANNOT_SECONDARY = +22p,Helvetica,black
gmt gmtset FONT_LABEL = +22p,Helvetica,black

path_1=/Users/EnzeZhang/data/calving_front_deep_learning/JI/split_data_polygon1_Apr24
path_2=/Users/EnzeZhang/data/calving_front_deep_learning/JI/split_data_polygon2_Apr24
area_change_TSX_p1=$path_1/JI_TSX.txt
area_change_TSX_p2=$path_2/JI_TSX.txt
area_change_Landsat8_p1=$path_1/JI_landsat8.txt
area_change_Landsat8_p2=$path_2/JI_landsat8.txt
area_change_sentinel1_A_p1=$path_1/JI_sentinel1.txt
area_change_sentinel1_A_p2=$path_2/JI_sentinel1.txt
area_change_ALOS1_p1=$path_1/JI_ALOS1.txt
area_change_ALOS1_p2=$path_2/JI_ALOS1.txt
# transient_1=/Users/EnzeZhang/data/calving_front_deep_learning/JI/transient_polygon1.txt
# transient_2=/Users/EnzeZhang/data/calving_front_deep_learning/JI/transient_polygon2.txt


PS=/Users/EnzeZhang/data/calving_front_deep_learning/JI/JI_combine_Jun17.ps

R=2009/2020/-1/4
J=X12i/4i
D=jTL+w1c+o0.2c/0.2c

gmt psbasemap -J$J -R$R -Ba1/a1f0.2Wsne -K -P -X2i -Y5.5i> $PS



# cat $area_change_combine_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS
# cat $transient_1 |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS
cat $area_change_TSX_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c   -W1p,black  -K -O >> $PS
cat $area_change_Landsat8_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,red -K -O >> $PS

cat $area_change_sentinel1_A_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,blue -K -O >> $PS




echo 2018.5 -0.5 Southern Branch  | gmt pstext -R$R -J$J -F+f22p,1,black -K -O >>$PS

echo 2019.6 3.7 \(a\) | gmt pstext -R$R -J$J -F+f22p,1,black+jTL -O -K >>$PS


gmt psxy -J$J -R$R -W3p,- -O -K <<EOF>> $PS 
2012.3012 -1 
2012.3012 4
EOF

gmt psxy -J$J -R$R -A -W3p,- -O -K <<EOF>> $PS 
2016.2546 -1
2016.2546 4
EOF

R=2009/2020/-1/4
gmt psbasemap -J$J -R$R -Ba1/a1f0.2WSne -K -P -O -Y-4.5i >> $PS

# cat $area_change_combine_p2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -A -K -O -W1p >> $PS
# cat $transient_2 |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS
cat $area_change_TSX_p2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c   -W1p,black -K -O >> $PS
cat $area_change_Landsat8_p2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,red -K -O >> $PS
cat $area_change_sentinel1_A_p2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,blue -K -O >> $PS



echo 2018.5 -0.5 Northern Branch | gmt pstext -R$R -J$J -F+f22p,1,black -K -O >>$PS

echo 2019.6 3.7 \(b\) | gmt pstext -R$R -J$J -F+f22p,1,black+jTL -O -K >>$PS


gmt psxy -J$J -R$R -W3p,- -O -K <<EOF>> $PS 
2012.3012 -1 
2012.3012 4
EOF

gmt psxy -J$J -R$R -A -W3p,- -O -K <<EOF>> $PS 
2016.2546 -1
2016.2546 4
EOF

Jl=X2i/5i
Rl=0/1/0/1

echo 0.2 0.3 "Area change (10@+7@+ m@+2@+)"| gmt pstext -J$Jl -R$Rl -F+f22p,0,black+a90+jTL -K -O -X-1.5i -Y1.5i  >>$PS

Js=X3.5i/1i
# Js=X3.5i/1.3i
Rs=0/2/0/2
gmt psbasemap -J$Js -R$Rs -Ba0 -B+gwhite -X1.7i -Y5.95i -K -O >>$PS




gmt psxy -J$Js -R$Rs -Sc0.3c -Gwhite -W1p,black	 -K -O <<EOF>> $PS
0.3 1.6
EOF
echo 0.7 1.6 TerraSAR-X |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -K -O >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c -Gwhite -W1p,red -K -O <<EOF>> $PS
0.3 1
EOF
echo 0.7 1 Landsat-8 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c -Gwhite -W1p,blue -K -O <<EOF>> $PS
0.3 0.4
EOF
echo 0.7 0.4 Sentinel-1 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O >>$PS



gmt psconvert -E300 -A+s50c -Tg $PS
# gmt psconvert -E400 -A $PS
