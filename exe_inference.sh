#!/bin/bash

export CUDA_VISIBLE_DEVICES=1
para_file=para.ini
para_py=./script/parameters.py
eo_dir=$(python2 ${para_py} -p ${para_file} codes_dir)
expr=${PWD}
testid=$(basename $expr)

#input_test_dir=$(python2 ${para_py} -p ${para_file} input_test_dir)


work_root=$(python2 ${para_py} -p ${para_file} working_root)
# data_dir is the list of images and label images
polygon=$1
network=$2
rm -r test_output
mkdir test_output


#python /home/zez/data2/pytorch_deeplab/pytorch-deeplab-xception/inference.py ${work_root} ${work_root}/para.ini ${work_root}/list/test.txt --backbone resnet --workers 1 --cuda --useBN --batchSize 1 --resume ${work_root}/resnet_no_stretch_ALOS1_Mar30.tar
#python /home/zez/data2/pytorch_deeplab/pytorch-deeplab-xception/inference.py ${work_root} ${work_root}/para.ini ${work_root}/list/test.txt --backbone mobilenet --workers 1 --cuda --useBN --batchSize 1 --resume ${work_root}/mobilenet_histeq_ALOS1_Mar15.tar
python ${work_root}/pytorch-deeplab-xception/inference.py ${work_root} ${work_root}/para.ini ${work_root}/list/test.txt --backbone drn --workers 1 --cuda --useBN --batchSize 1 --resume ${work_root}/$network


rm -r post_output
mkdir post_output
rm -r post_process_shape
mkdir post_process_shape
rm -r in_polygon_gmt
mkdir in_polygon_gmt
rm -r post_process_gmt
mkdir post_process_gmt

images=(`cat ./list/test.txt |awk -F '/' '{print $NF}'`)
i=0
cd ${work_root}/test_output
count=${#images[@]}

while (($i<$count))
    do
         test_img=${images[i]}
         echo $test_img
         temp1=$test_img
         echo $temp1
         temp2=(`echo ${images[i]}| cut -d '.' -f 1`)
         echo ${temp2}


        #merge
        python ${eo_dir}/gdal_merge_average.py -o ${work_root}/post_output/${temp2}_out_temp1.tif *${temp2}*.tif

        #seprate weight and result
        echo "gdal_translate -of Gtiff -b 1 ${work_root}/post_output/${temp2}_out_temp1.tif ${work_root}/post_output/${temp2}_out_result.tif"
        gdal_translate -of Gtiff -ot Float32 -b 1 ${work_root}/post_output/${temp2}_out_temp1.tif ${work_root}/post_output/${temp2}_out_result.tif
        echo "gdal_translate -of Gtiff -b 2 ${work_root}/post_output/${temp2}_out_temp1.tif ${work_root}/post_output/${temp2}_out_wight.tif"
        gdal_translate -of Gtiff -ot Float32 -b 2 ${work_root}/post_output/${temp2}_out_temp1.tif ${work_root}/post_output/${temp2}_out_wight.tif

        #calculate final results
        echo "gdal_calc.py -A ${work_root}/post_output/${temp2}_out_result.tif -B ${work_root}/post_output/${temp2}_out_wight.tif --outfile=${work_root}/post_output/${temp2}_out_temp.tif --calc=\"A/B\" --NoDataValue=0"
        gdal_calc.py -A ${work_root}/post_output/${temp2}_out_result.tif -B ${work_root}/post_output/${temp2}_out_wight.tif --outfile=${work_root}/post_output/${temp2}_out_temp.tif --type='Float64' --calc="A/B" --NoDataValue=0
        echo "gdal_calc.py -A ${work_root}/post_output/${temp2}_out_temp.tif --outfile=${work_root}/post_output/${temp2}_out.tif --calc=\"255*(A>0.5)\" --NoDataValue=0"
        gdal_calc.py -A ${work_root}/post_output/${temp2}_out_temp.tif --outfile=${work_root}/post_output/${temp2}_out.tif --calc="255*(A>0.5)" --NoDataValue=0

        #make polygon
        echo "gdal_polygonize.py -8 ${work_root}/post_output/${temp2}_out.tif -b 1 -f \"ESRI Shapefile\" ${work_root}/post_output/${temp2}_out.shp"
        gdal_polygonize.py -8 ${work_root}/post_output/${temp2}_out.tif -b 1 -f "ESRI Shapefile" ${work_root}/post_output/${temp2}_out.shp

        #remove small polygons
	echo "python ${eo_dir}/rm_small_polygon.py  --input_shape ${work_root}/post_output/${temp2}_out.shp --output_shape ${work_root}/post_process_shape/${temp2}_out_post.shp"
        python ${eo_dir}/rm_small_polygon.py  --input_shape ${work_root}/post_output/${temp2}_out.shp --output_shape ${work_root}/post_process_shape/${temp2}_out_post.shp

        #convert to gmtfile
        ogr2ogr -f 'GMT' ${work_root}/post_process_gmt/${temp2}.gmt ${work_root}/post_process_shape/${temp2}_out_post.shp
        sed -i 1,11d ${work_root}/post_process_gmt/${temp2}.gmt

	echo "python ${eo_dir}/point_in_polygon.py --input ${work_root}/post_process_gmt/${temp2}.gmt --polygon $polygon --output ${work_root}/in_polygon_gmt/${temp2}.gmt"
	python ${eo_dir}/point_in_polygon.py --input ${work_root}/post_process_gmt/${temp2}.gmt --polygon $polygon --output ${work_root}/in_polygon_gmt/${temp2}.gmt
	echo " gmt2kml -Fl ${work_root}/in_polygon_gmt/${temp2}.gmt >${work_root}/in_polygon_gmt/${temp2}.kml"
        gmt gmt2kml -Fl ${work_root}/in_polygon_gmt/${temp2}.gmt >${work_root}/in_polygon_gmt/${temp2}.kml
        echo "ogr2ogr -f \"ESRI Shapefile\" ${work_root}/in_polygon_gmt/${temp2}.shp ${work_root}/in_polygon_gmt/${temp2}.kml"
        ogr2ogr -f "ESRI Shapefile" ${work_root}/in_polygon_gmt/${temp2}.shp ${work_root}/in_polygon_gmt/${temp2}.kml

        #rm in-process files
        rm ${work_root}/post_output/${temp2}_out.tif
        rm ${work_root}/post_output/${temp2}_out_temp1.tif
        rm ${work_root}/post_output/${temp2}_out_result.tif
        rm ${work_root}/post_output/${temp2}_out_wight.tif
        #rm ${work_root}/post_output/${temp2}_out_temp.tif
        i=$[i+1]
    done
cd ..
