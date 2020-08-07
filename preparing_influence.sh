#!/usr/bin/env bash


#
#find /home/zez/data1/Landsat8/JI/crop_merge/20160724_082233_crop_landsat.tif > list/test.txt
#find /home/zez/data1/Landsat8/JI/crop_histeq_merge/*.tif > list/test.txt 
#find /home/zez/data1/Landsat8/Helheim/crop_merge/*.tif > list/test.txt
#find /home/zez/data1/Landsat8/Helheim/crop_histeq_merge/*.tif > list/test.txt
#find /home/zez/data1/Landsat8/Helheim/linear_stretch_merge/*.tif > list/test.txt
#find /home/zez/data1/Landsat8/Helheim/gee_saved/merge/*.tif > list/test.txt
#find /home/zez/data1/Landsat8/Helheim/crop_adeq_merge/*.tif > list/test.txt

#find /home/zez/data1/Landsat8/Kangerdlugssuaq/crop_merge/*.tif > list/test.txt 
#find /home/zez/data1/Landsat8/Kangerdlugssuaq/crop_histeq_merge/*.tif >list/test.txt

####sentinel######
#find /home/zez/data2/sentinel_JI/GEE/GRD/Ascending/hist_eq_8bit_merge/*.tif >list/test.txt
#find /home/zez/data2/sentinel_JI/GEE/GRD/Descending/hist_eq_8bit_merge/*.tif >list/test.txt
#find /home/zez/data2/sentinel_JI/GEE/GRD/Descending/hist_eq_8bit_merge/abandon/*.tif >list/test.txt
#find /home/zez/data2/sentinel_Helheim/GEE/GRD/Descending/hist_eq_8bit_merge/*.tif > list/test.txt
#find /home/zez/data2/sentinel_Helheim/GEE/GRD/Ascending/hist_eq_8bit_merge/*.tif > list/test.txt
#find /home/zez/data2/sentinel_Helheim/GEE/GRD/Descending/linear_stretch_merge/*.tif > list/test.txt
#find /home/zez/data2/sentinel_Helheim/GEE/GRD/Descending/after_merge_merge/*.tif  > list/test.txt
#find /home/zez/data2/sentinel_Kanger/GEE/GRD/Descending/hist_eq_8bit_merge/*.tif > list/test.txt
#find /home/zez/data2/sentinel_Kanger/GEE/GRD/Ascending/hist_eq_8bit_merge/*.tif > list/test.txt


#####sentinel2#####
#find /home/zez/data1/sentinel-2_Helheim/hist_eq_three_color/*.tif > list/test.txt
#find /home/zez/data1/sentinel-2_Helheim/hist_eq_green_merge/*.tif > list/test.txt
#find /home/zez/data1/sentinel-2_Helheim/linear_stretch_green_merge/*.tif > list/test.txt
#find /home/zez/data1/sentinel2_TOA_Helheim/hist_eq_red_merge/*.tif > list/test.txt
#find /home/zez/data1/sentinel2_TOA_Helheim/linear_stretch_red_merge/*.tif > list/test.txt
#find /home/zez/data1/sentinel2_TOA_Helheim/red_merge/*.tif > list/test.txt

#####ALOS#######
#find /home/zez/data1/ALOS/helheim/crop_desample_medianblur_merge/*.tif >list/test.txt
#find /home/zez/data1/ALOS/helheim/stretch_hist_merge/*.tif >list/test.txt
#find /home/zez/data1/ALOS/helheim/stretch_linear_merge/*.tif > list/test.txt
#find /home/zez/data1/ALOS/test/hist_eq/merge/*.tif > list/test.txt
#find /home/zez/data1/ALOS/JI/hist_eq_merge/*.tif > list/test.txt
#find /home/zez/data1/ALOS/kanger/hist_eq_merge/*.tif > list/test.txt
####ENIVSAT
#find /home/zez/data1/ENVISAT/hist_eq_merge/*.tif > list/test.txt
#find /home/zez/data1/ENVISAT/change_window/hist_eq_merge/*.tif > list/test.txt
#find /home/zez/data1/ENVISAT/change_window/linear_stretch_merge/*.tif > list/test.txt
#find /home/zez/data1/ENVISAT/change_window/crop_merge/*.tif > list/test.txt
#find /home/zez/data1/ENVISAT/crop_merge/*.tif > list/test.txt 
#find /home/zez/data1/ENVISAT/linear_stretch_merge/*.tif > list/test.txt 


####TSX
#find /home/zez/data2/TSX/helheim/hist_eq_new_merge/*.tif > list/test.txt
#find /home/zez/data2/TSX/helheim/hist_eq_merge/20140404_003_TSX_Helheim_stretch.tif > list/test.txt
#find /home/zez/data2/TSX/helheim/hist_eq_merge/*.tif > list/test.txt
#find /home/zez/data2/TSX/helheim/linear_stretch_merge/*.tif > list/test.txt
#find /home/zez/data2/TSX/helheim/image_change_position/hist_eq_merge/*.tif > list/test.txt
find /home/zez/data2/TSX/JI/hist_eq_merge/2013*.tif > list/test.txt
#while read image <&3 && read label <&4
#do
#    #echo $image
#  #  echo $label
#    size_image=$(gdalinfo ${image} | grep "Size is" )
#    width_image=$(echo $size_image | cut -d' ' -f 3 )
#    width_image=${width_image::-1}
#    height_image=$(echo $size_image | cut -d' ' -f 4 )
#   # echo "*****width,height of image *****:" $width_image , $height_image
#    size_label=$(gdalinfo ${label} | grep "Size is" )
#    width_label=$(echo $size_label | cut -d' ' -f 3 )
#    width_label=${width_label::-1}
#    height_label=$(echo $size_label | cut -d' ' -f 4 )
#   # echo "*****width,height of label *****:" $width_label , $height_label
#    if [ "$width_image" -ne "$width_label" -o "$height_image" -ne "$height_label" ];then
#    echo "gdal_translate -srcwin 0 0 $width_image $height_image -a_nodata 0 $label ${root}/train/label_figure/temp.tif"
#    gdal_translate -srcwin 0 0 $width_image $height_image -a_nodata 0 $label ${root}/train/label_figure/temp.tif
#    echo "mv ${root}/train/label_figure/temp.tif $label"
#    mv ${root}/train/label_figure/temp.tif $label
#    fi
##        echo $img
##        gdal_translate -srcwin 0 0 $out_w $out_h -a_nodata 0 $img temp.tif
##        mv temp.tif $img
##
#
#done 3<"list/image_list.txt" 4<"list/label_list.txt"

