#!/bin/bash
para_file=para.ini
para_py=./script/parameters.py
working_path=$(python2 ${para_py} -p ${para_file} working_root)

path=$1
network=$2
cd $path
dir=(`ls |grep "GID"`)
i=0
count=${#dir[@]}
while(($i<$count))
do
	cd $working_path
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
