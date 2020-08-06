#!/bin/bash
crop=/home/zez/data1/ALOS/crop_desample_medianblur
original_dir=/home/zez/data1/ALOS/original_image
cd $original_dir
file=$1
date=$2
i=0
count=${#file[@]}
while (($i<$count))
do
	 
	echo $date
	if [ -f $crop/${date}_ALOS1.tif ];then
		echo "file exist"
	else
	echo "gdalwarp -overwrite -t_srs EPSG:4326 -r near -tps -co COMPRESS=NONE $original_dir/${file[i]} temp.tif"
	gdalwarp -overwrite -t_srs EPSG:4326 -r near -tps -co COMPRESS=NONE $original_dir/${file[i]} temp.tif
	echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 6261 2683 temp.tif crop.tif"	
	gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 6261 2683 temp.tif crop.tif 
	echo "python ~/zez_code/medianBlur_16.py --input crop.tif --output crop_desample.tif"
	python ~/zez_code/medianBlur_16.py --input crop.tif --output crop_desample.tif 
	echo "gdalcopyproj.py crop.tif crop_desample.tif"
	gdalcopyproj.py crop.tif crop_desample.tif
	echo "gdal_translate -of Gtiff -b 1 -outsize 30% 30% crop_desample.tif $crop/${date}_ALOS1.tif"
	gdal_translate -of Gtiff -b 1 -outsize 30% 30% crop_desample.tif $crop/${date}_ALOS1.tif
	rm crop.tif temp.tif crop_desample.tif
	fi
	i=$[i+1]

done
