#!/bin/bash
path=$1
polygon=$2
network=$3
cd $path
dir=(`ls |grep "GID"`)
i=0
count=${#dir[@]}
while(($i<$count))
do
	cd /home/zez/data3/pytorch_deeplab_running/running_dir
        echo "bash preparing_influence.sh $path/${dir[i]}/hist_eq"
	bash preparing_influence.sh $path/${dir[i]}/hist_eq
	if [ -f /home/zez/data3/pytorch_deeplab_running/running_dir/list/test.txt ];then
		echo "succeed"
	else
		echo "error! no test.txt"
		exit
	fi
	echo "bash exe_inference.sh $polygon $network"
	bash exe_inference.sh $polygon $network
	rm /home/zez/data3/pytorch_deeplab_running/running_dir/list/test.txt
	if [ -d $path/${dir[i]}/in_polygon_gmt ];then
		echo "in_polygon_gmt exist"
	else
		mkdir $path/${dir[i]}/in_polygon_gmt
	fi
	temp=${network%.tar*}
	echo "mv in_polygon_gmt $path/${dir[i]}/in_polygon_gmt/$temp"
	mv in_polygon_gmt $path/${dir[i]}/in_polygon_gmt/$temp
	i=$[i+1]
done
