#!/bin/bash
#crop=/home/zez/data1/ALOS/crop_desample_medianblur
crop=/home/zez/data1/ENVISAT/change_window
original_dir=/home/zez/data1/ENVISAT/original_image
cd $original_dir
file=(`ls *.N1`)
i=0
count=${#file[@]}
while (($i<$count))
do
	 
	temp=(`echo ${file[i]} |cut -d '_' -f 3`)
	echo $temp
	date=${temp:6:8}
	echo $date
	if [ -f $crop/${date}_ALOS2.tif ];then
		echo "file exist"
	else
		echo "gdalwarp -overwrite -t_srs EPSG:4326 -r near -tps -co COMPRESS=NONE $original_dir/${file[i]} temp.tif"
		gdalwarp -overwrite -t_srs EPSG:4326 -r near -tps -co COMPRESS=NONE $original_dir/${file[i]} temp.tif
		echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 857 367 temp.tif crop.tif"	
		gdalwarp -overwrite -te -38.23 66.32 -38.02 66.41 -ts 857 367 temp.tif crop.tif 
		
		#echo "python ~/zez_code/medianBlur_16.py --input crop.tif --output crop_desample.tif"
		#python ~/zez_code/medianBlur_16.py --input crop.tif --output crop_desample.tif 
		#echo "gdalcopyproj.py crop.tif crop_desample.tif"
		#gdalcopyproj.py crop.tif crop_desample.tif
		#echo "gdal_translate -of Gtiff -b 1 -outsize 30% 30% crop_desample.tif $crop/${date}_ALOS2.tif"
		#gdal_translate -of Gtiff -b 1 -outsize 30% 30% crop_desample.tif $crop/${date}_ALOS2.tif
		mv crop.tif $crop/${date}_ENVISAT.tif
		rm temp.tif
	fi
	i=$[i+1]

done
