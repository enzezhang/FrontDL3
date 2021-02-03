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
		echo "cp -r $path/${dir[i]}/figure/$temp  /home/zez/data3/Greenland_Front_Mapping/figure_check/${dir[i]}_$temp"
		if [ -d /home/zez/data3/Greenland_Front_Mapping/figure_check/${dir[i]}_$temp ];then 
			echo "already move"
		else
			cp -r $path/${dir[i]}/figure/$temp  /home/zez/data3/Greenland_Front_Mapping/figure_check/${dir[i]}_$temp
		fi
	else
		echo "figure/$temp does not exist"
	fi
	i=$[i+1]
done
