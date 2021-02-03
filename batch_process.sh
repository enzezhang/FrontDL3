#!/bin/bash

GID=GID66
GID2=GID_66
xmin=-64.46
ymin=76.33
xmax=-64.21
ymax=76.39
x_size_L=450
y_size_L=460
x_size_S=680
y_size_S=690
echo "bash batch_process_Landsat-8_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8 $xmin $ymin $xmax $ymax $x_size_L $y_size_L Landsat8_${GID}"
echo "bash batch_process_Sentinel-2_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2 $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel2_${GID}"
echo "bash batch_process_Sentinel-1_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_D $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_D"
echo "bash batch_process_Sentinel-1_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_A $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_A"
echo "bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8/hist_eq"
echo "bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2/hist_eq"
echo "bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2_D/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2_D/hist_eq"
echo "bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2_A/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2_A/hist_eq"
#bash batch_process_Landsat-8_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8 $xmin $ymin $xmax $ymax $x_size_L $y_size_L Landsat8_${GID}
#bash batch_process_Sentinel-2_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2 $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel2_${GID}
#bash batch_process_Sentinel-1_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_D $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_D
#bash batch_process_Sentinel-1_images.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_A $xmin $ymin $xmax $ymax $x_size_S $y_size_S Sentinel1_${GID}_A
#bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Landsat-8/hist_eq
#bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-2/hist_eq
bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_D/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_D/hist_eq
bash batch_stretch.sh /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_A/after_merge /home/zez/data3/Greenland_Front_Mapping/$GID/${GID2}_Sentinel-1_A/hist_eq
