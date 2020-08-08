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
PS=$path/JI_result.ps
# velocity=$path/greenland_ice_surface_velocity_lola.grd
# CPT=$path/velocity2.cpt
#Rg=-653000/879700/-3384500/-632600
#Rg=0/1000/0/1000
Jg=x0.00000326i
R=-60/57/20/80r
J=B-42/76/90/60/8i 

# gmt psbasemap -R$R -J$J -K -P -Ba0 >$PS

# gmt grdimage -R$R -J$J -K -O -P $velocity -C$CPT -Q >>$PS

# gmt psscale -R$R -J$J -K -C$CPT -DjBR+w10c/0.7c+o2.0c/0.4c -F+gwhite+c0.1 -O -Ba1 -By+l"m/day" -Q >>$PS
# # cat $file_result | awk '{print $2,$1}'|gmt psxy -R$R -J$J -O -K -Sa0.5 -Gred >>$PS

# echo -43 66.37 Helheim |gmt pstext -J$J -R$R -O -F+f24p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
# echo -60 68.6 Jakobshavn Isbr@e |gmt pstext -J$J -R$R -O -F+f24p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
# echo -34 69.6 Kangerdlugssuaq |gmt pstext -J$J -R$R -O -F+f24p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

# # echo 69.214 -49.715 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1 -Gblack >>$PS
# echo 69.157	-49.623 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1 -Gblack >>$PS
# echo 68.574	-32.477 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1 -Gblack >>$PS
# echo 66.356	-38.188 | awk '{print $2,$1}' |gmt psxy -R$R -J$J -O -K -Sa1 -Gblack >>$PS
# gmt psbasemap -R$R -J$J -O -P -K -Ba0 >>$PS

# plot JI using TSX images
R=-49.81/-49.5/69.11/69.26
J=M8.3
imagename=$path/20130828_JI_TSX.grd
calving_line=$path/20130828_JI_TSX.gmt
gmt psbasemap -J$J -R$R -K -V -P -Ba0 -X8.2i  > $PS

gmt grd2cpt -Cgray $imagename > sar.cpt
gmt grdimage $imagename -R$R -J$J -Csar.cpt -O -Q -K >>$PS
gmt psxy -R$R -J$J -A -W2p,red $calving_line -K -O >>$PS
gmt gmtset FONT_ANNOT_PRIMARY = +8p,Helvetica,black

gmt gmtset MAP_SCALE_HEIGHT=5p
# gmt psbasemap -J$J -R$R -Lg-49.585/69.24+c-49.655+w4k+u+f -F+gwhite -O -K -V -P >> $PS

gmt gmtset FONT_ANNOT_PRIMARY = +10p,Helvetica,black
#gmt gmtset FONT_ANNOT_PRIMARY = +14p,Helvetica,black
echo -49.62 69.255 Jakobshavn Isbr@e |gmt pstext -J$J -R$R -O -F+f20p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS
echo -49.587 69.246 TerraSAR-X|gmt pstext -J$J -R$R -O -F+f20p,0,black -Wwhite -Gwhite -C10%/10% -TO >>$PS
# echo -49.79 69.25 \(c\) |gmt pstext -J$J -R$R -O -F+f15p,0,black -K -Wwhite -Gwhite -C10%/10% -TO >>$PS

# gmt psbasemap -J$J -R$R -O -V -P -Bxa -Bya -BWSne >> $PS

gmt psconvert -E300 -A -Tg $PS


