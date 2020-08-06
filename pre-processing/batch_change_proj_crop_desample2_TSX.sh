#!/bin/bash 



work_path=/home/zez/data2/TSX/helheim
out_figure=/home/zez/data2/TSX/helheim/original_images
cd $work_path
filename=(`ls | grep "20[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9]"`)
count=${#filename[@]}

i=0
while (($i<$count))
do
    echo ${filename[i]}
	cd $work_path
	cd ${filename[i]}/TSX-1.SAR.L1B
	temp=(`ls`)
	echo "cd $temp/IMAGEDATA"
	cd $temp/IMAGEDATA
	data=(`ls IMAGE*.tif`)
	#rm haha.tif
	if [ -f haha.tif ];then
		echo "already change proj"
	else 
		echo "gdalwarp -t_srs EPSG:4326 $data haha.tif"		
		gdalwarp -t_srs EPSG:4326 $data haha.tif
	fi
	rm crop.tif
	if [ -f crop.tif ];then 
		echo "already crop"
	else
		gdalwarp -overwrite -te -38.23 66.32 -38.02 66.41 -ts 10780 4620  haha.tif crop.tif		
	fi
	
	rm medianblur.tif
	if [ -f medianblur.tif ];then 
		echo "already median blur"
	else 
		echo "python /home/zez/zez_code/medianBlur_16.py  --input $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/crop.tif --output $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/medianblur.tif"
		python /home/zez/zez_code/medianBlur_16.py  --input $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/crop.tif --output $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/medianblur.tif
		echo "python gdalcopyproj.py $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/crop.tif $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/medianblur.tif"

		gdalcopyproj.py $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/crop.tif $work_path/${filename[i]}/TSX-1.SAR.L1B/$temp/IMAGEDATA/medianblur.tif

	fi
	
	rm  desampled.tif
	if [ -f desampled.tif ];then
	    echo "already desampled"
	else
	    echo "gdal_translate -of Gtiff -b 1 -outsize 20% 20% -r average medianblur.tif desampled.tif"
	    gdal_translate -of Gtiff -b 1 -outsize 15% 15% -r average medianblur.tif desampled.tif
        fi
	cp desampled.tif $out_figure/${filename[i]}_TSX_Helheim.tif
    i=$[i+1]
done
	
	
