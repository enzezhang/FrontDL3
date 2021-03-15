#!/bin/bash


para_file=para.ini
para_py=./script/parameters.py
working_path=$(python2 ${para_py} -p ${para_file} working_root)
path=$1
polygon=$2
network=$3
cd $path
dir=(`ls |grep "GID"`)
i=0
count=${#dir[@]}
while(($i<$count))
do
	cd $working_path
        echo "bash preparing_influence.sh $path/${dir[i]}/hist_eq"
	bash preparing_influence.sh $path/${dir[i]}/hist_eq
	if [ -f $working_path/list/test.txt ];then
		echo "succeed"
	else
		echo "error! no test.txt"
		exit
	fi
	echo "bash exe_inference.sh $polygon $network"
	bash exe_inference.sh $polygon $network
	rm $working_path/list/test.txt
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
