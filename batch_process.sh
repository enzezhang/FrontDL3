#!/bin/bash
path=/home/henry/data/Greenland_Front_Mapping
GID=GID51
GID2=GID_51
xmin=-59.93
ymin=75.96
xmax=-59.60
ymax=76.03
x_size_L=620
y_size_L=550
x_size_S=940
y_size_S=830
echo "bash batch_process_Landsat-8_images.sh $path/$GID/${GID2}_Landsat-8 $xmin $ymin $xmax $ymax $x_size_L $y_size_L Landsat8_${GID}"
echo "bash batch_process_Sentinel-2_images.sh $path/$GID/${GID2}_Sentinel-2 $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel2_${GID}"
echo "bash batch_process_Sentinel-1_images.sh $path/$GID/${GID2}_Sentinel-1_D $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_D"
echo "bash batch_process_Sentinel-1_images.sh $path/$GID/${GID2}_Sentinel-1_A $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_A"
echo "bash batch_stretch.sh $path/$GID/${GID2}_Landsat-8/after_merge $path/$GID/${GID2}_Landsat-8/hist_eq"
echo "bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-2/after_merge $path/$GID/${GID2}_Sentinel-2/hist_eq"
echo "bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-2_D/after_merge $path/$GID/${GID2}_Sentinel-2_D/hist_eq"
echo "bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-2_A/after_merge $path/$GID/${GID2}_Sentinel-2_A/hist_eq"
bash batch_process_Landsat-8_images.sh $path/$GID/${GID2}_Landsat-8 $xmin $ymin $xmax $ymax $x_size_L $y_size_L Landsat8_${GID}
bash batch_process_Sentinel-2_images.sh $path/$GID/${GID2}_Sentinel-2 $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel2_${GID}
bash batch_process_Sentinel-1_images.sh $path/$GID/${GID2}_Sentinel-1_D $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_D
bash batch_process_Sentinel-1_images.sh $path/$GID/${GID2}_Sentinel-1_A $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_A
bash batch_stretch.sh $path/$GID/${GID2}_Landsat-8/after_merge $path/$GID/${GID2}_Landsat-8/hist_eq
bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-2/after_merge $path/$GID/${GID2}_Sentinel-2/hist_eq
bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-1_D/after_merge $path/$GID/${GID2}_Sentinel-1_D/hist_eq
bash batch_stretch.sh $path/$GID/${GID2}_Sentinel-1_A/after_merge $path/$GID/${GID2}_Sentinel-1_A/hist_eq
