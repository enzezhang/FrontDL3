#!/bin/bash

para_file=para.ini
para_py=./script/parameters.py
working_path=$(python2 ${para_py} -p ${para_file} working_root)
data_path=$(python2 ${para_py} -p ${para_file} data_path)

if [ -d $data_path/figure_check ];then
	echo "figure check exist"
else
	mkdir $data_path/figure_check
fi


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
		echo "cp -r $path/${dir[i]}/figure/$temp  $data_path/figure_check/${dir[i]}_$temp"
		if [ -d /home/zez/data3/Greenland_Front_Mapping/figure_check/${dir[i]}_$temp ];then 
			echo "already move"
		else
			cp -r $path/${dir[i]}/figure/$temp  $data_path/figure_check/${dir[i]}_$temp
		fi
	else
		echo "figure/$temp does not exist"
	fi
	i=$[i+1]
done
