#!/bin/bash
path=$1
code_path=/home/zez/zez_code/polygon_complexity.py
cd $path
file=(`ls *.gmt`)
i=0
if [ -d $path/abandon ];then
	echo "abandon dir exist"
else
	mkdir $path/abandon
fi
count=${#file[@]}
while(($i<$count))
do
	date=${file[i]:0:8}
	#python $code_path --input ${file[i]} --date $date	
	a=(`python $code_path --input ${file[i]} --date $date `)
	echo ${a[0]} ${a[1]}
	if [ ${a[1]} \> 0.043 ];then
		echo "${file[i]} is abandon with complexity of ${a[1]}"
		temp=(`echo ${file[i]}| cut -d '.' -f 1`)
		mv *$temp* $path/abandon
	fi
	i=$[i+1]
done


