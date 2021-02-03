#!/bin/bash

work_dir=$1
xmin=$2
ymin=$3
xmax=$4
ymax=$5

x_size=$6
y_size=$7

dir=${work_dir}/original_image
out_dir=${work_dir}/after_merge
temp_dir=${work_dir}/temp
if [ -d $out_dir ];then
	echo "$out_dir exist"
else
	mkdir $out_dir
fi
if [ -d $temp_dir ];then
	echo "$temp_dir exist"
else
	mkdir $temp_dir
fi

flg=$8
cd $dir
file=(`ls *.tif`)
i=0
count=${#file[@]}
while (($i<$count))
do
	temp=${file[i]:0:8}
	echo ${temp}
	#his_out=${his_modified}/${file[i]}
	temp_image=${temp_dir}/${temp}_${flg}.tif
	out_image=${out_dir}/${temp}_${flg}.tif
	if [ -f ${out_image} ];then
		echo "file exist"
	else 
		if [ -f ${temp_image} ];then
			echo "${temp_image} needs merge"
			mv ${temp_image}  ${temp_dir}/${temp}_${flg}_1.tif
			echo "gdalwarp -t_srs EPSG:4326 -te $xmin $ymin $xmax $ymax -ts $x_size $y_size ${file[i]} temp_2.tif"
			gdalwarp -t_srs EPSG:4326 -te $xmin $ymin $xmax $ymax -ts $x_size $y_size ${file[i]} temp_2.tif
			gdal_translate -of Gtiff -b 1 temp_2.tif ${temp_dir}/${temp}_${flg}_2.tif
			rm temp_2.tif
			echo "gdal_merge.py -n 0 -o ${temp_image} ${temp_dir}/${temp}_${flg}_1.tif ${temp_dir}/${temp}_${flg}_2.tif"
			gdal_merge.py -n 0 -o ${temp_image} ${temp_dir}/${temp}_${flg}_1.tif ${temp_dir}/${temp}_${flg}_2.tif
		else
			echo "gdalwarp -t_srs EPSG:4326 -te $xmin $ymin $xmax $ymax -ts $x_size $y_size ${file[i]} temp.tif"
			gdalwarp -t_srs EPSG:4326 -te $xmin $ymin $xmax $ymax -ts $x_size $y_size ${file[i]} temp.tif
			gdal_translate -of Gtiff -b 1 temp.tif ${temp_image}
		fi
	fi
	i=$[i+1]
	rm temp.tif 
done
mv ${temp_dir}/* ${out_dir}/
rm  ${out_dir}/*_1*
rm  ${out_dir}/*_2*
cd ${out_dir}
	
