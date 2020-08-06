#!/bin/bash

work_dir=/home/zez/data1/sentinel2_TOA_Helheim
dir=${work_dir}/original_images
#ref_dir=/home/zez/data2/sentinel_Helheim/GRD_IW
#his_modified=/home/zez/data2/sentinel_Helheim/GEE/histogram_modified
out_dir=${work_dir}/red
temp_dir=${work_dir}/temp
cd $dir
file=(`ls *.tif`)
i=0
count=${#file[@]}
while (($i<$count))
do
	temp=${file[i]:0:8}
	echo ${temp}
	#his_out=${his_modified}/${file[i]}
	temp_image=${temp_dir}/${temp}_GEE_sentinel2_helheim.tif
	out_image=${out_dir}/${temp}_GEE_sentinel2_helheim.tif
	if [ -f ${out_image} ];then
		echo "file exist"
	else 
		if [ -f ${temp_image} ];then
			echo "${temp_image} needs merge"
			rm ${temp_image}
			echo "gdalwarp -t_srs EPSG:4326 ${file[i-1]} temp.tif"
			gdalwarp -t_srs EPSG:4326 ${file[i-1]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_1.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_1.tif
			echo "gdal_translate -of Gtiff -b 1 temp_1.tif ${temp_dir}/${temp}_GEE_sentinel2_helheim_1.tif"
			gdal_translate -of Gtiff -b 1 temp_1.tif ${temp_dir}/${temp}_GEE_sentinel2_helheim_1.tif
			rm temp.tif temp_1.tif
			echo "gdalwarp -t_srs EPSG:4326 ${file[i]} temp.tif"
			gdalwarp -t_srs EPSG:4326 ${file[i]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_2.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_2.tif
			gdal_translate -of Gtiff -b 1 temp_2.tif ${temp_dir}/${temp}_GEE_sentinel2_helheim_2.tif
			rm temp.tif temp_2.tif
			/home/zez/zez_code/gdal_merge.py -n 0 -o ${temp_image} ${temp_dir}/${temp}_GEE_sentinel2_helheim_1.tif ${temp_dir}/${temp}_GEE_sentinel2_helheim_2.tif
		else
	
			echo "gdalwarp -t_srs EPSG:4326 ${file[i]} temp.tif"
			gdalwarp -t_srs EPSG:4326 ${file[i]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_temp.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 950 1050 temp.tif temp_temp.tif
			gdal_translate -of Gtiff -b 1 temp_temp.tif ${temp_image}
		fi
	fi
	i=$[i+1]
	rm temp.tif temp_temp.tif
done
mv ${temp_dir}/* ${out_dir}/
rm  ${out_dir}/*_1*
rm  ${out_dir}/*_2*
cd ${out_dir}
	
