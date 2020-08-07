#!/bin/bash

export CUDA_VISIBLE_DEVICES=1
para_file=para.ini
para_py=/home/hlc/codes/PycharmProjects/DeeplabforRS/parameters.py
eo_dir=$(python2 ${para_py} -p ${para_file} codes_dir)
expr=${PWD}
testid=$(basename $expr)

#input_test_dir=$(python2 ${para_py} -p ${para_file} input_test_dir)


work_root=$(python2 ${para_py} -p ${para_file} working_root)
# data_dir is the list of images and label images


rm -r test_output
mkdir test_output
#python /home/zez/data2/pytorch_deeplab/pytorch-deeplab-xception/inference.py ${work_root} ${work_root}/para.ini ${work_root}/list/test.txt --backbone resnet --workers 1 --cuda --useBN --batchSize 1 --resume ${work_root}/resnet_based_all_data_JI_Kanger_TSX_Landsat_sentinel_0.005_all_histeq_8bit_Nov12.tar
python /home/zez/data2/pytorch_deeplab/pytorch-deeplab-xception/inference.py ${work_root} ${work_root}/para.ini ${work_root}/list/test.txt --backbone drn --workers 1 --cuda --useBN --batchSize 1 --resume ${work_root}/drn_default_hist_eq_ALOS1_JI_Kanger_Jun22.tar
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
        python /home/zez/zez_code/gdal_merge_average.py -o ${work_root}/post_output/${temp2}_out_temp1.tif *${temp2}*.tif

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
        echo "python ${eo_dir}/rm_small_polygon.py --input_shape ${work_root}/post_output/${temp2}_out.shp --output_shape ${work_root}/post_process_shape/${temp2}_out_post.shp"
        python ${eo_dir}/rm_small_polygon.py --threshold 500 --input_shape ${work_root}/post_output/${temp2}_out.shp --output_shape ${work_root}/post_process_shape/${temp2}_out_post.shp

        #convert to gmtfile
        ogr2ogr -f 'GMT' ${work_root}/post_process_gmt/${temp2}.gmt ${work_root}/post_process_shape/${temp2}_out_post.shp
        sed -i 1,11d ${work_root}/post_process_gmt/${temp2}.gmt

        #find the calving front with in the cut polygon
        echo "python /users/s1155083077/code/point_in_polygon.py --input ${work_root}/post_process_gmt/${temp2}.gmt --polygon ${work_root}/cut_polygon.gmt --output ${work_root}/in_polygon_gmt/${temp2}.gmt"
        python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/point_in_polygon.py --input ${work_root}/post_process_gmt/${temp2}.gmt --polygon ${work_root}/post-processing/polygon_for_truncation/in_polygon_Kanger.gmt --output ${work_root}/in_polygon_gmt/${temp2}.gmt
        echo "gmt2kml -Fl ${work_root}/in_polygon_gmt/${temp2}.gmt >${work_root}/in_polygon_gmt/${temp2}.kml"
        gmt2kml -Fl ${work_root}/in_polygon_gmt/${temp2}.gmt >${work_root}/in_polygon_gmt/${temp2}.kml
        echo "ogr2ogr -f \"ESRI Shapefile\" ${work_root}/in_polygon_gmt/${temp2}.shp ${work_root}/in_polygon_gmt/${temp2}.kml"
        ogr2ogr -f "ESRI Shapefile" ${work_root}/in_polygon_gmt/${temp2}.shp ${work_root}/in_polygon_gmt/${temp2}.kml

        #rm in-process files
        rm ${work_root}/post_output/${temp2}_out.tif
        rm ${work_root}/post_output/${temp2}_out_temp1.tif
        rm ${work_root}/post_output/${temp2}_out_result.tif
        rm ${work_root}/post_output/${temp2}_out_wight.tif
        rm ${work_root}/post_output/${temp2}_out_temp.tif
        i=$[i+1]
    done
cd ..
