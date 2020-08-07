#!/bin/bash
data=$1
dir=$2
out=$3

cd $dir
i=0
count=(`awk '{print NR}' $data|tail -n1`)
echo $count
while(($i<$count))
do 
	temp=(`sed -n ''$[i+1]'p' $data| awk '{print $4}'`)
	echo $temp
	file=(`ls ${temp}*.gmt`)
	flag=${#file[@]}
	if [ ${#file[@]} \> 1 ];then
		echo ${file[@]}
		echo "choose only one file"
		temp2=${file[0]}
		unset file
		file=$temp2
		echo ${file[@]}
	fi
	if [ "${file}" = ${file:0:15}_crop_landsat_Kangerdlugssuaq_stretch.gmt ];then
		echo "landsat8"
		sed -n ''$[i+1]'p' $data >> $out/Kanger_landsat8.txt
	elif [ "${file}" = ${temp}_hh_GEE_sentinel_GRD_IW_kanger_stretch.gmt ];then
		echo "sentinel1"
		sed -n ''$[i+1]'p' $data >> $out/Kanger_sentinel1.txt
	elif [ "${file}" = ${temp}_Kanger_ALOS1_stretch.gmt ];then
		echo "ALOS1"
		 sed -n ''$[i+1]'p' $data >> $out/Kanger_ALOS1.txt
	else 
		echo "error"
		sleep 5
	fi
	i=$[i+flag]
done
