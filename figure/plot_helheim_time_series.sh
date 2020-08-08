#!/bin/bash
#rm gmt.conf
gmt gmtset PS_MEDIA = 90cx120c
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +22p,Helvetica,black
gmt gmtset FONT_ANNOT_SECONDARY = +22p,Helvetica,black
gmt gmtset FONT_LABEL = +22p,Helvetica,black

path=/Users/EnzeZhang/data/calving_front_deep_learning/Helheim/split_combine_Apr23
Landsat8=$path/Helheim_landsat8.txt

sentinel1=$path/Helheim_sentinel1.txt

TSX=$path/Helheim_TSX.txt
Sentinel2=$path/Helheim_sentinel2.txt
Envisat=$path/Helheim_ENVISAT.txt
ALOS1=$path/Helheim_ALOS1.txt
ALOS2=$path/Helheim_ALOS2.txt
combine=/Users/EnzeZhang/data/calving_front_deep_learning/Helheim/Helheim_combine_Apr20_accu.txt
PS=/Users/EnzeZhang/data/calving_front_deep_learning/Helheim/Helheim_Jul14.ps

R=2002/2020/-0.6/4
J=X16i/4i
D=jTL+w1c+o0.2c/0.2c

gmt psbasemap -J$J -R$R -Ba2/a1f0.2WSne -K -P -X2i -Y5.5i> $PS

echo 2002.2 3.6 \(a\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -K -O >>$PS
# cat $two_year_cycle | awk '{print $1,$2}' |gmt psxy -J$J -R$R -A -O -W1p,black -K >> $PS
# cat $area_change_combine_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS
# cat $area_change_TSX_p1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sa0.4c  -Gblack -K -O >> $PS
# cat $combine | awk '{print $3,$1}' |gmt psxy -J$J -R$R -A -W1p,black -K -O >> $PS

cat $Landsat8 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,red -K -O >> $PS
cat $sentinel1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,blue -K -O >> $PS
cat $TSX | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,black -K -O >> $PS
cat $Sentinel2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,magenta -K -O >> $PS
cat $Envisat | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,purple -K -O >> $PS
cat $ALOS1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,green -K -O >> $PS
cat $ALOS2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,cyan -K -O >> $PS

gmt psxy -J$J -R$R -O -K -W2p,black >> $PS <<EOF
2018.2 1.2
2018.2 3
2019 3
2019 1.2
2018.2 1.2
EOF
echo 2019.1 1 \(b\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -K -O >>$PS

gmt psxy -J$J -R$R -W3p,- -O -K <<EOF>> $PS
2012 -0.6
2012 4
EOF

Jl=X2i/5i
Rl=0/1/0/1



#ps legend #####################
Js=X7i/1.33i
Rs=0/4/0/2.4
gmt psbasemap -J$Js -R$Rs -Ba0 -B+gwhite -X4.5i -Y2.65i -K -O >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c   -W3p,red	 -K -O <<EOF>> $PS
0.3 2.1
EOF
echo 0.7 2.1 Landsat-8 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -K -O >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c   -W3p,magenta -K -O <<EOF>> $PS
0.3 1.5
EOF
echo 0.7 1.5 Sentinel-2 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c  -W3p,blue -K -O <<EOF>> $PS
0.3 0.9
EOF
echo 0.7 0.9 Sentinel-1 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c   -W3p,black -K -O <<EOF>> $PS
0.3 0.3
EOF
echo 0.7 0.3 TerraSAR-X |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c  -W3p,purple	 -K -O <<EOF>> $PS
2.3 2.1
EOF
echo 2.7 2.1 Envisat |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -K -O >>$PS



gmt psxy -J$Js -R$Rs -Sc0.3c   -W3p,green -K -O <<EOF>> $PS
2.3 1.5
EOF
echo 2.7 1.5 ALOS |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS


gmt psxy -J$Js -R$Rs -Sc0.3c   -W3p,cyan -K -O <<EOF>> $PS
2.3 0.9
EOF
echo 2.7 0.9 ALOS-2 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS





R=2018.2/2019/1.2/3
J=X16i/4i
D=jTL+w1c+o0.2c/0.2c

gmt psbasemap -J$J -R$R -Ba0.2/a0.4f0.2WSne -O -K -P -X-4.5i -Y-7.35i>> $PS
echo 2018.21 2.8 \(b\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -K -O >>$PS
cat $Landsat8 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.4c  -W2p,red -K -O >> $PS
cat $sentinel1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.4c  -W2p,blue -K -O >> $PS
cat $Sentinel2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.4c  -W2p,magenta -K -O >> $PS
cat $ALOS2 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.4c  -W2p,cyan -O  -K>> $PS
# echo 2017.1615 2.3344  |gmt psxy -J$J -R$R -Sc0.4c  -W1p,blue -Gblue -K -O >> $PS
echo 2018.4271 1.9237 |gmt psxy -J$J -R$R -Sc0.7c  -W1p,blue -Gblue -K -O  >> $PS

gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.0219 1.8810
2018.0219 2.1810
EOF

gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.3614 1.3474
2018.3614 1.6474
EOF

gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.4162 1.5549
2018.4162 1.8549
EOF

gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.4654 1.7039
2018.4654 2.0039
EOF
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.5339 1.9304
2018.5339 2.2304
EOF
#20180930
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.7447 2.1607
2018.7447 2.4607
EOF
#20181030
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.8268 2.4425
2018.8268 2.7225
EOF

gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.9555 2.0495
2018.9555 2.3295
EOF



Jl=X2i/5i
Rl=0/1/0/1

echo 0.2 0.1 "Area change (10@+7@+ m@+2@+)"| gmt pstext -J$Jl -R$Rl -F+f22p,0,black+a90+jTL -O -X-1.5i -Y2.4i>>$PS
# Js=X3.5i/0.7i
# Rs=0/2/0/2
# gmt psbasemap -J$Js -R$Rs -Ba0 -B+gwhite -X1.7i -Y3i -K -O >>$PS

# # gmt psxy -J$Js -R$Rs  -W1p -O -K <<EOF>> $PS

# # 0.1 1.4
# # 0.5 1.4
# # EOF

# echo 0.7 1.4 Landsat8 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -K -O >>$PS

# gmt psxy -J$Js -R$Rs -St0.4c -Gwhite -W1p,red -K -O <<EOF>> $PS
# 0.3 1.4
# EOF
# gmt psxy -J$Js -R$Rs -Sd0.4c -Gwhite -W1p,blue -K -O <<EOF>> $PS
# 0.3 0.58
# # EOF
# echo 0.7 0.6 Sentinel-1 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O >>$PS

gmt psconvert -E300 -A+s50c -Tg $PS
# gmt psconvert -E400 -A $PS
