#!/bin/bash 


image_path=/home/zez/data1/Landsat8/Helheim/crop_histeq
calving_path=$1
grd_path=/home/zez/data1/Landsat8/Helheim/grd_non_stretch
out_path=$2
cd $calving_path
calving_file=(`ls *.gmt`)


count=${#calving_file[@]}

i=0
#cd /home/zez/test_deep_learning/u_net/figure
while(($i<$count))
do	
	temp=(`echo ${calving_file[i]}| cut -d '.' -f 1`)
	#temp2=${temp:0:36}
	temp2=${temp}_adeq
	temp2=${temp}
	echo $temp
	date=${temp:0:8}
	if [ -f $grd_path/$temp2.grd ];then
		echo "grd exist"
	else
		gdal_translate -of GMT $image_path/${temp2}.tif $grd_path/$temp2.grd
	fi
	
	#gmt grd2cpt $grd_path/$temp.grd -Cgray > sar.cpt

	echo "bash /home/zez/data1/Landsat8/Helheim/script/result_plot.sh $grd_path/$temp2.grd $calving_path/$temp.gmt $date $out_path/$temp.ps"		
	bash /home/zez/data1/Landsat8/Helheim/script/result_plot_landsat.sh $grd_path/$temp2.grd $calving_path/$temp.gmt $date $out_path/$temp.ps
	#bash /home/zez/test_deep_learning/u_net/figure/result_plot_without_stretch.sh $grd_path/$temp.grd $temp $out_path/$temp.ps 
	#echo "bash /home/zez/test_deep_learning/u_net/figure/result_plot_without_stretch.sh $grd_path/$temp.grd $temp $out_path/$temp.ps"
	gmt psconvert -E300 -A+s20c -Tg $out_path/$temp.ps
	i=$[i+1]
done
	
	

