#!/bin/bash

rm gmt.* 
gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset FONT_ANNOT_PRIMARY = +20p,Helvetica,black
gmt gmtset FORMAT_GEO_OUT = ddd:mm:ssF	
gmt gmtset MAP_VECTOR_SHAPE=1.4
gmt gmtset PS_MEDIA = 120cx100c
gmt gmtset FONT_ANNOT_SECONDARY=+7p,Helvetica,black
gmt gmtset MAP_VECTOR_SHAPE=0
# gmt gmtset DIR_GSHHG=/Users/EnzeZhang/data/gshhg-gmt-2.3.7
path=/Users/EnzeZhang/data/calving_front_deep_learning/figure/intro_figure

file_result=$path/all_glacier.txt
PS=$path/intro_figure_Jul22.ps
velocity=$path/greenland_ice_surface_velocity_lola.grd
CPT=$path/velocity2.cpt
#Rg=-653000/879700/-3384500/-632600
#Rg=0/1000/0/1000


########################
#plot whole Greenland
R=-60/57/20/80r
J=B-42/76/90/60/8i 
gmt psbasemap -R$R -J$J -K -P -Ba0 -X2i -Y15i >$PS

# gmt grdimage -R$R -J$J -K -O -P $velocity -C$CPT -Q >>$PS
gmt pscoast -R$R -J$J -W1/0.5p,black -Dh -Gtan -Slightblue -Cl/royalblue -O -K >>$PS
# gmt psscale -R$R -J$J -K -C$CPT -DjBR+w10c/0.7c+o2.0c/0.4c -F+gwhite+c0.1 -O -Ba1 -By+l"m/day" -Q >>$PS
# cat $file_result | awk '{print $2,$1}'|gmt psxy -R$R -J$J -O -K -Sa0.5 -Gred >>$PS

echo -45 66.37 Helheim |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -59 70 Jakobshavn Isbr@e |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -32 70.4 Kangerdlugssuaq |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

# echo 69.214 -49.715 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1 -Gblack >>$PS
echo 69.157	-49.623 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1.5 -Gblack >>$PS
echo 68.574	-32.477 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1.5 -Gblack >>$PS
echo 66.356	-38.188 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1.5 -Gblack >>$PS

echo 4 81 \(a\) |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
gmt psbasemap -R$R -J$J -O -P -Ba0 -K>>$PS


# plot JI using TSX images
R=-49.81/-49.5/69.11/69.26
J=M8.5i
imagename=$path/20130828_JI_TSX.grd
calving_line=$path/20130828_JI_TSX.gmt
width_JI1=$path/width_JI_1.gmt
width_JI2=$path/width_JI_2.gmt
gmt psbasemap -J$J -R$R -K -V -P -Ba0 -X8.3i -O >> $PS

gmt grd2cpt -Cgray $imagename > sar.cpt
gmt grdimage $imagename -R$R -J$J -Csar.cpt -K -O -Q >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
#gmt psxy -R$R -J$J -A -W2p,blue $width_JI2 -K -O >>$PS
#gmt psxy -R$R -J$J -A -W2p,blue $width_JI1 -K -O >>$PS
gmt gmtset MAP_SCALE_HEIGHT=15p
gmt psbasemap -J$J -R$R -Lg-49.526/69.225+c-49.655+w4k+u+f+jMR -F+gwhite -O -K -V -P >> $PS

# gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
#gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
echo -49.51 69.235 20130828 |gmt pstext -J$J -R$R -O -F+f28p,0,black+jMR  -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.51 69.255 Jakobshavn Isbr@e |gmt pstext -J$J -R$R -O -F+f28p,0,black+jMR -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.51 69.245 TerraSAR-X|gmt pstext -J$J -R$R -O -F+f28p,0,black+jMR -Wwhite -Gwhite -C10%/10% -TO -K >>$PS
echo -49.77 69.2528 \(b\) |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.58 69.2 Glacier |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.75 69.17 Ice m'\351'lange |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

echo -49.717 69.187 0 2 |gmt psxy -R$R -J$J -Sv1.3c+ea -W10p,red -Gred -O -K >>$PS

echo -49.705 69.225 Northern Branch |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.63 69.155 Southern Branch |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
gmt psbasemap -J$J -R$R -O -V -P -K -Bxa -Bya -BES >> $PS




#plot Helheim using Landsat images
R=-38.28/-38.07/66.32/66.41
J=M8i
imagename=$path/20130820_231014_crop_landsat_Helheim_stretch.grd
calving_line=$path/20130820_231014_crop_landsat_Helheim_stretch.gmt
width_Helheim=$path/width_Helheim.gmt
gmt grd2cpt -Cgray $imagename > sar.cpt

gmt psbasemap -J$J -R$R -K -V -O -P -Ba0 -X-8.3i -Y-9.2i>> $PS

gmt grdimage $imagename -R$R -J$J -Csar.cpt -K -O -Q >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
#gmt psxy -R$R -J$J -A -W2p,blue $width_Helheim -K -O >>$PS

gmt psbasemap -J$J -R$R -Lg-38.23/66.388+c-38.175+w4k+u+f -F+gwhite -O -K -V -P >> $PS
# #gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
echo -38.23 66.378 20130820 |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.402 Helheim |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.395 Landsat-8|gmt pstext -J$J -R$R -O -F+f28p,0,black -Wwhite -Gwhite -C10%/10% -TO -K >>$PS

echo -38.092  66.402 \(c\)|gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.12 66.374 Ice m'\351'lange |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.23 66.368 Glacier |gmt pstext -J$J -R$R -O -F+f28p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -38.15 66.36 180 2 |gmt psxy -R$R -J$J -Sv1.3c+ea -W10p,red -Gred -O -K >>$PS
gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWS -K >> $PS


#plot Kanger using Sentinel-1 images


R=-32.97/-32.77/68.54/68.6133
J=M8.5i
imagename=$path/20150130_hh_GEE_sentinel_GRD_IW_kanger_stretch.grd
calving_line=$path/20150130_hh_GEE_sentinel_GRD_IW_kanger_stretch.gmt
width_Kanger=$path/width_Kanger.gmt
gmt grd2cpt -Cgray $imagename > sar.cpt

gmt psbasemap -J$J -R$R -K -V -O -P -Ba0 -X8.3i  >> $PS

gmt grdimage $imagename -R$R -J$J -Csar.cpt -K -O -Q >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
#gmt psxy -R$R -J$J -A -W2p,blue $width_Kanger -K -O >>$PS

gmt psbasemap -J$J -R$R -Lg-32.936/68.545+c-32.88+w4k+u+f -F+gwhite -O -K -V -P >> $PS


echo -32.965 68.56  Kangerlussuaq | gmt pstext -J$J -R$R -O -F+f28p,4,black+jML -K -Wwhite -Gwhite -C20%/20% -TO >>$PS
echo -32.965 68.555 20150130 | gmt pstext -J$J -R$R -O -F+f28p,4,black+jML -K -Wwhite -Gwhite -C20%/20% -TO >>$PS
echo -32.965 68.55 Sentinel-1 | gmt pstext -J$J -R$R -O -F+f28p,4,black+jML -K -Wwhite -Gwhite -C20%/20% -TO >>$PS

echo -32.84 68.58 Ice m'\351'lange |gmt pstext -J$J -R$R -O -F+f28p,0,black+jML -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -32.948 68.6 Glacier |gmt pstext -J$J -R$R -O -F+f28p,0,black+jML -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

# echo -32.894 68.59 148 2 |gmt psxy -R$R -J$J -Sv1.3c+ea -W10p,red -Gred -O -K >>$PS

echo -32.88 68.59 148 2 |gmt psxy -R$R -J$J -Sv1.3c+ea -W10p,red -Gred -O -K >>$PS

echo -32.95 68.607 \(d\) |gmt pstext -J$J -R$R -O -F+f28p,0,black+jML -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BES >> $PS






gmt psconvert -E300 -A+s50c -Tg $PS




