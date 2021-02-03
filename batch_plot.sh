#!/bin/bash
path=$1
network=$2
cd $path
dir=(`ls |grep "GID"`)
i=0
count=${#dir[@]}
while(($i<$count))
do
	cd /home/zez/data3/pytorch_deeplab_running/running_dir
	temp=${network%.tar*}
	if [ -d $path/${dir[i]}/figure ];then
		echo "figure exist"
	else 
		mkdir $path/${dir[i]}/figure
	fi
	if [ -d $path/${dir[i]}/figure/$temp ];then
		echo "figure/$temp exist"
	else
		mkdir $path/${dir[i]}/figure/$temp 
	fi
	echo "bash batch_plot_result.sh $path/${dir[i]} $path/${dir[i]}/in_polygon_gmt/$temp  $path/${dir[i]}/figure/$temp"
	bash batch_plot_result.sh $path/${dir[i]} $path/${dir[i]}/in_polygon_gmt/$temp  $path/${dir[i]}/figure/$temp
	i=$[i+1]
done
