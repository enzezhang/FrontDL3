#!/bin/bash
work_path=$1
stretch_new=$2
cd $work_path
file=(`ls *.tif`)
count=${#file[@]}
i=0
while(($i<$count))
do
	temp=(`echo ${file[i]}| cut -d '.' -f 1`)
	echo $temp
	if [ -f ${stretch_new}/${temp}_stretch.tif ];then
		echo "file exist"
	else
	gdal_contrast_stretch -histeq 100 ${work_path}/${file[i]} ${stretch_new}/${temp}_stretch.tif
	fi
	i=$[i+1]
done
