#!/bin/bash

#path=/home/zez/data1/Landsat8/Helheim/zip
path=/home/zez/zez_storage/Helheim/Landsat8/zip

crop=/home/zez/data1/Landsat8/Helheim/crop
stretch=/home/zez/data1/Landsat8/Helheim/stretch
temp=/home/zez/data1/Landsat8/Helheim/temp
cd $path

file=(`ls *.gz`)
count=${#file[@]}
i=0

while (($i<$count))
do 
	temp1=${file[i]:10:6}
	temp2=${file[i]:17:8}
	if [ -f ${temp}/${temp2}_${temp1}.tif ];then
		echo "temp file exist"
	else
		echo "tar -xvf ${file[i]}"
		tar -xvf ${file[i]}
		mv *B8.TIF ${temp}/${temp2}_${temp1}.tif
		rm *.TIF 
		rm *.txt
		
	fi
	if [ -f ${crop}/${temp2}_${temp1}_crop_landsat_Helheim.tif ];then
		echo "crop file exist"
	else 
		echo "gdalwarp -s_srs EPSG:32623 -t_srs EPSG:4326 ${temp}/${temp2}_${temp1}.tif temp.tif"
		gdalwarp -s_srs EPSG:32624 -t_srs EPSG:4326 ${temp}/${temp2}_${temp1}.tif temp.tif

		echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 860 350  temp.tif ${crop}/${temp2}_${temp1}_crop_landsat_Helheim.tif"
		gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 860 350 temp.tif ${crop}/${temp2}_${temp1}_crop_landsat_Helheim.tif
	fi
	rm temp.tif
	if [ -f ${stretch}/${temp2}_${temp1}_crop_stretch_landsat_Helheim.tif ];then
		echo "stretch exist"
	else
		echo "gdal_contrast_stretch -percentile-range 0.02 0.98 ${crop}/${temp2}_${temp1}_crop_landsat_Helheim.tif ${stretch}/${temp2}_${temp1}_crop_stretch_landsat_Helheim.tif"
		gdal_contrast_stretch -percentile-range 0.02 0.98 ${crop}/${temp2}_${temp1}_crop_landsat_Helheim.tif ${stretch}/${temp2}_${temp1}_crop_stretch_landsat_Helheim.tif
	fi	
	i=$[i+1]
done
