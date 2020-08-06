#!/bin/bash
#bash batch_unzip.sh /home/zez/zez_storage/Helheim/sentinel/zip /home/zez/data2/sentinel_Helheim/temp /home/zez/data2/sentinel_Helheim/GRD_IW sentinel_GRD_IW_helheim
path=$1

cd $path
file=(`ls *.zip`)

count=${#file[@]}

i=0
while(($i<$count))
do 
		cd $path
		unzip ${path}/${file[i]}
	i=$[i+1]
done


