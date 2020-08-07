#!/bin/bash

# bash generate_error_polygon.sh /home/zez/data1/Landsat8/Helheim/in_polygon_gmt/resnet_based_all_data_JI_Kanger_0.007_Jul25 resnet_based_all_data_JI_Kanger_0.007_Jul25


error_path=/home/zez/data2/Helheim_test/error_analysis
#mkdir for label files

if [ -d $error_path/label_figure_255 ];then
	echo " label_figure_255 dir exist"
else 
	mkdir $error_path/label_figure_255
fi

if [ -d $error_path/label_gmt ];then
	echo " label_gmt dir exist"

else 
	mkdir $error_path/label_gmt
fi

if [ -d $error_path/label_in_polygon_gmt ];then
	echo "label_in_polygon_gmt dir exist"
else 
	mkdir $error_path/label_in_polygon_gmt
fi

if [ -d $error_path/label_in_polygon_gmt_invert ];then
	echo "label_in_polygon_gmt_invert dir exist"
else 
	mkdir $error_path/label_in_polygon_gmt_invert
fi

label_path=/home/zez/data2/Helheim_test/label_figure

data_path=$1
dir=$2

#this is the dir for the final error polygons 

if [ -d $error_path/$dir ];then
	echo "dir exist"
	rm $error_path/$dir/*
else 
	mkdir $error_path/$dir
fi


#this is the calving front data path

cd $label_path
file=(`ls *.tif`)
echo $count
count=${#file[@]}
i=0
echo "$count images in total"
while(($i<$count))
do 
	#temp=${file[i]:0:15}
	temp=(`echo ${file[i]}| cut -d '.' -f 1`)
	# generate 255 images
	if [ -f $error_path/label_figure_255/$temp.tif ];then
		echo "$label_path/$temp.tif exist"
	else
		echo "gdal_calc.py -A $label_path/${file[i]} --$error_path/label_figure_255/$temp.tif --NoDataValue=0 --calc="A*255""
		gdal_calc.py -A $label_path/${file[i]} --outfile=$error_path/label_figure_255/$temp.tif --NoDataValue=0 --calc="A*255"
	fi

	#generate label_gmt and label_shape
	if [ -f $error_path/label_in_polygon_gmt_invert/${temp}.gmt ];then
		echo "$error_path/label_in_polygon_gmt_invert/${temp}.gmt exist"
	else
		echo "gdal_polygonize.py -8 -b 1 -f "ESRI Shapefile" $error_path/label_figure_255/$temp.tif $error_path/label_gmt/$temp.shp"
		gdal_polygonize.py -8 -b 1 -f "ESRI Shapefile" $error_path/label_figure_255/$temp.tif $error_path/label_gmt/$temp.shp
		ogr2ogr -f 'GMT' $error_path/label_gmt/$temp.gmt $error_path/label_gmt/$temp.shp
		#gmt kml2gmt -Fp $error_path/label_gmt/$temp.kml > $error_path/label_gmt/$temp.gmt

		#echo "sed '/^> Next/d' $error_path/label_gmt/$temp.gmt > $error_path/label_gmt/${temp}_new.gmt"
		#sed '/^> Next/d' $error_path/label_gmt/$temp.gmt > $error_path/label_gmt/${temp}_new.gmt
		sed 1,11d $error_path/label_gmt/$temp.gmt > $error_path/label_gmt/${temp}_new.gmt
		python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/point_in_polygon.py --input $error_path/label_gmt/${temp}_new.gmt --polygon /home/zez/data2/pytorch_deeplab/test1/in_polygon_Helheim_new_Jul4.gmt --output $error_path/label_in_polygon_gmt/${temp}.gmt

		#gmt gmt2kml -Fl /home/zez/test_deep_learning/u_net/error_analysis/label_in_polygon_gmt/${temp}.gmt > /home/zez/test_deep_learning/u_net/error_analysis/label_in_polygon_gmt/${temp}.kml
		python /home/zez/data1/Landsat8/Helheim/script/invert_data2.py --input $error_path/label_in_polygon_gmt/${temp}.gmt --output $error_path/label_in_polygon_gmt_invert/${temp}.gmt
		#gmt gmt2kml -Fl /home/zez/test_deep_learning/u_net/error_analysis/label_in_polygon_gmt_invert/${temp}.gmt >/home/zez/test_deep_learning/u_net/error_analysis/label_in_polygon_gmt_invert/${temp}.kml
	fi
	if  [ -f $data_path/${temp}*.gmt ];then

		cat $error_path/label_in_polygon_gmt_invert/${temp}.gmt $data_path/${temp}*.gmt > $error_path/$dir/${temp}.gmt
		gmt gmt2kml -Fp  $error_path/$dir/${temp}.gmt >  $error_path/$dir/${temp}.kml
		ogr2ogr -f "ESRI Shapefile"  $error_path/$dir/${temp}.shp  $error_path/$dir/${temp}.kml
	else 
		echo "file doesn't exist"
	fi

	i=$[i+1]
done
