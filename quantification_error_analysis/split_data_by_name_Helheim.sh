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
	if [ ${#file[@]} \> 1 ];then
		echo ${file[@]}
		echo "choose only one file"
		temp2=${file[0]}
		unset file
		file=$temp2
		echo ${file[@]}
	fi
	if [ "${file}" = ${file:0:15}_crop_landsat_Helheim_stretch.gmt ];then
		echo "landsat8"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_landsat8.txt
	elif [ "${file}" = ${temp}_GEE_sentinel2_helheim_stretch.gmt ];then
		echo "sentinel2"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_sentinel2.txt
	elif [ "${file}" = ${temp}_hh_GEE_sentinel_GRD_IW_helheim_stretch.gmt ];then
		echo "sentinel1"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_sentinel1.txt
	elif [ "${file}" = ${temp}_???_TSX_Helheim_stretch.gmt ];then
		echo "TSX"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_TSX.txt
	elif [ "${file}" = ${temp}_ENVISAT_stretch.gmt ];then
		echo "ENVISAT"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_ENVISAT.txt
	elif [ "${file}" = ${temp}_ALOS1_helheim_stretch.gmt ];then
		echo "ALOS1"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_ALOS1.txt
	elif [ "${file}" = ${temp}_ALOS2_helheim_stretch.gmt ];then
		echo "ALOS2"
		sed -n ''$[i+1]'p' $data >> $out/Helheim_ALOS2.txt
	else 
		echo "error"
		sleep 5
	fi
 	
	i=$[i+1]
done
