#!/bin/bash
path=$1
out_path=$2
echo $out_path
if [ -d $out_path ];then
	echo "dir exist"
else 
	echo "mkdir $out_path"
	mkdir $out_path
fi
cd $path
#rm *.invert
file=(`ls *.gmt`)
#if [ -f ${file[0]}.invert ];then
#	echo "invert file exist"
#else 
#	python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/invert_data2.py --input ${file[0]} --output ${file[0]}.invert
#fi
#python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/invert_data2.py --input ${file[0]} --output ${file[0]}.invert

count=${#file[@]}
i=0
while(($i<$count))
do
	if [ -f $out_path/${file[i]} ];then
		echo "file exist"
	else	
		temp=(`echo ${file[i]}| cut -d '.' -f 1`)
			python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/invert_data2.py --input ${file[i]} --output ${file[i]}.invert
		if [ $i = 0 ];then
			echo "cat ${file[i]}.invert ${file[i]} > $out_path/${file[i]}"
			cat ${file[i]}.invert ${file[i]} > $out_path/${file[i]}
		else 
			echo "cat ${file[i-1]}.invert ${file[i]} > $out_path/${file[i]}" 
			cat ${file[i-1]}.invert ${file[i]} > $out_path/${file[i]}
		fi
		gmt2kml -Fp $out_path/${file[i]} > $out_path/$temp.kml
		ogr2ogr -f "ESRI Shapefile" $out_path/$temp.shp $out_path/$temp.kml  
	fi
	
	i=$[i+1]
done	
