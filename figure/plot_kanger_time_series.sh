#!/bin/bash
#rm gmt.conf
gmt gmtset PS_MEDIA = 90cx120c
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +22p,Helvetica,black
gmt gmtset FONT_ANNOT_SECONDARY = +22p,Helvetica,black
gmt gmtset FONT_LABEL = +22p,Helvetica,black

path=/Users/EnzeZhang/data/calving_front_deep_learning/Kanger/data_split_Jul24
area_change_Landsat8=$path/Kanger_landsat8.txt

area_change_sentinel1=$path/Kanger_sentinel1.txt


# area_change_combine=/Users/EnzeZhang/data/calving_front_deep_learning/Kanger/Kanger_combine_Nov14.txt

PS=/Users/EnzeZhang/data/calving_front_deep_learning/Kanger/Kanger_Jul24.ps

R=2013/2020/-2.8/3
J=X12i/4i
D=jTL+w1c+o0.2c/0.2c

gmt psbasemap -J$J -R$R -Ba1/a1f0.2WSne -K -P -X2i -Y5.5i> $PS


# transient=/Users/EnzeZhang/data/calving_front_deep_learning/Kanger/transient.txt

# cat $transient | awk '{print $1,$2}' |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS

# cat $area_change_combine | awk '{print $3,$1}' |gmt psxy -J$J -R$R -A -O -W1p -K >> $PS
echo 2019.7 2.7 \(a\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -O -K >>$PS
cat $area_change_Landsat8 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,red -K -O >> $PS

cat $area_change_sentinel1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,blue -K -O >> $PS
gmt psxy -J$J -R$R -O -K -W2p,black >> $PS <<EOF
2017.8 1.1
2018.202 1.1
2018.202 1.9
2017.8 1.9
2017.8 1.1
EOF

echo 2018.21 1 \(b\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -O -K >>$PS
gmt psxy -J$J -R$R -W3p,- -O -K <<EOF>> $PS
2015.8378 -2.8
2015.8378 3
EOF


Js=X3.5i/0.7i
Rs=0/2/0/2
gmt psbasemap -J$Js -R$Rs -Ba0 -B+gwhite -X0.2i -Y3i -K -O >>$PS

# gmt psxy -J$Js -R$Rs  -W1p -O -K <<EOF>> $PS

# 0.1 1.4
# 0.5 1.4
# EOF

echo 0.7 1.5 Landsat-8 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -K -O >>$PS

gmt psxy -J$Js -R$Rs -Sc0.3c -Gwhite -W2p,red	 -K -O <<EOF>> $PS
0.3 1.5
EOF
gmt psxy -J$Js -R$Rs -Sc0.3c -Gwhite -W2p,blue -K -O <<EOF>> $PS
0.3 0.5
EOF
echo 0.7 0.5 Sentinel-1 |gmt pstext -J$Js -R$Rs -F+f22p,0,black+jML -O -K >>$PS

R=2017.8/2018.202/1.1/1.9
J=X12i/4i
D=jTL+w1c+o0.2c/0.2c
gmt psbasemap -J$J -R$R -Ba0.2/a0.4f0.2WSne -O -K -P -X-0.2i -Y-7.7i>> $PS
echo 2018.18 1.8 \(b\) |gmt pstext -J$J -R$R -F+f22p,0,black+jML -O -K >>$PS
cat $area_change_Landsat8 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,red -K -O >> $PS

cat $area_change_sentinel1 | awk '{print $3,$1}' |gmt psxy -J$J -R$R -Sc0.3c  -W1p,blue -K -O >> $PS


# #20171019
# gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
# 2017.7967 1.4526
# 2017.7967 1.6526
# EOF

#20171106
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2017.8460 1.2319
2017.8460 1.5043
EOF
#20171206
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2017.928 1.2820
2017.928 1.6055
EOF
#20171230
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2017.9938 1.3521
2017.9938 1.6540
EOF
#20180204
gmt psxy -J$J -R$R -W3p,black -O -K <<EOF>> $PS
2018.0931 1.2845
2018.0931 1.6015
EOF




Jl=X2i/5i
Rl=0/1/0/1

echo 0.2 0.1 "Area change (10@+7@+ m@+2@+)"| gmt pstext -J$Jl -R$Rl -F+f22p,0,black+a90+jTL -O -X-1.5i -Y2.4i >>$PS

gmt psconvert -E300 -A+s50c $PS
# gmt psconvert -E400 -A $PS
