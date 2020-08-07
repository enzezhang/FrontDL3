#!/usr/bin/env bash

#bash batch_error_analysis.sh /home/zez/data1/Landsat8/Helheim/error_analysis/resnet_based_all_data_JI_Kanger_0.007_Jul25 /home/zez/data1/Landsat8/Helheim/error_analysis/label_in_polygon_gmt

#rm -r label_in_polygon_gmt_invert label_in_polygon_gmt merged_two_calving label_gmt label_gmt_new

#mkdir label_in_polygon_gmt merged_two_calving label_gmt label_gmt_new label_in_polygon_gmt_invert
#cd /home/zez/test_deep_learning/u_net/error_analysis/label_figure
#file=(`ls *Mar17.tif`)


#dir=merged_two_calving_test20_Oct9

dir=$1
cd $dir
label_dir=$2
file=(`ls *.gmt`)
count=${#file[@]}
i=0

while(($i<$count))
do
	#temp=${file[i]:0:15}
	temp=(`echo ${file[i]}| cut -d '.' -f 1`)
	temp2=${file[i]:0:8}
    	#echo "python /home/zez/data1/error_analysis/estimate_error.py --input $dir/${temp}.shp --label $label_dir/${temp}.gmt --date $temp2"
	python /home/zez/data1/error_analysis/estimate_error.py --input $dir/${temp}.shp --label $label_dir/${temp}.gmt --date $temp2
	i=$[i+1]
done
