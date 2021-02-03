#!/bin/bash
path=$1
cd $path
dir=(`ls |grep "GID"`)
i=0
count=${#dir[@]}
while(($i<$count))
do
	cd ${dir[i]}
	pwd
	if [ -d original_image ];then
		echo "original_image exist"
	else
		echo "mkdir original_image"
		mkdir original_image
		echo "mv *.tif original_image"
		mv *.tif original_image
		
	fi
	if [ -d script ];then
		echo "script exist"
	else
		mkdir script
	fi
	if [ -d hist_eq ];then
                echo "hist_eq exist"
        else
                mkdir hist_eq
        fi
	if [ -d in_polygon_gmt ];then
                echo "in_polygon_gmt exist"
        else
                mkdir in_polygon_gmt
        fi
	if [ -d figure ];then
                echo "figure exist"
        else
                mkdir figure
        fi
	cd ../
	i=$[i+1]
done
