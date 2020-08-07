#!/usr/bin/env bash


data_path=$1
#output=$2


ref_path=$2
cd $ref_path
ref=(`ls *.gmt`)
cd $data_path
file=(`ls *.gmt`)

count=${#file[@]}
#rm $output
i=0
while(($i<$count))
do
    temp1=(`ls ${file[i]}| cut -d '_' -f 5`)
    temp=${file[i]:0:8}
  
    #echo $temp
    #echo "python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/calculate_area.py --input ${file[i]} --date $temp"
	#echo "python /home/zez/data2/calving_front_existing_data/scirpt/calculate_area.py --input ${file[i]} --reference $ref_path/${ref[i]} --date $temp"
	python /home/zez/data2/calving_front_deep_learning/script/calculate_area.py --input ${file[i]} --reference $ref_path/${ref[i]} --date $temp
	#python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/calculate_area_length.py --input ${file[i]} --calving /home/zez/data1/test20/seperate_in_polygon_calving_front_Oct9/polygon2/$temp.gmt --date $temp
    i=$[i+1]
done

