#!/bin/bash

work_dir=/home/zez/data2/sentinel_Helheim/GEE/GRD/Descending
dir=${work_dir}/original_images
#ref_dir=/home/zez/data2/sentinel_Helheim/GRD_IW
#his_modified=/home/zez/data2/sentinel_Helheim/GEE/histogram_modified
out_dir=${work_dir}/after_merge
temp_dir=${work_dir}/temp
cd $dir
file=(`ls *.tif`)
i=0
count=${#file[@]}
while (($i<$count))
do
	temp=${file[i]:17:8}
	echo ${temp}
	ref=${ref_dir}/${temp}_hh_sentinel_GRD_IW_helheim.tif
	#his_out=${his_modified}/${file[i]}
	temp_image=${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim.tif
	out_image=${out_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim.tif
	#if [ -f ${his_out} ];then
	#	echo "already match history"
	#else
	#	echo "python /home/zez/data1/Landsat8/Helheim/script/histogram_matching.py --input ${dir}/${file[i]} --reference ${ref} --output ${his_out}"
	#	python /home/zez/data1/Landsat8/Helheim/script/histogram_matching.py --input ${dir}/${file[i]} --reference ${ref} --output ${his_out}
	#	echo "gdalcopyproj.py ${dir}/${file[i]} ${his_out}"
	#	gdalcopyproj.py ${dir}/${file[i]} ${his_out}
	#fi
	if [ -f ${out_image} ];then
		echo "file exist"
	else 
		if [ -f ${temp_image} ];then
			echo "${temp_image} needs merge"
			rm ${temp_image}
			echo "gdalwarp -s_srs EPSG:32625 -t_srs EPSG:4326 ${file[i-1]} temp.tif"
			gdalwarp -s_srs EPSG:32625 -t_srs EPSG:4326 ${file[i-1]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_1.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_1.tif
			echo "gdal_calc.py -A temp_1.tif --outfile=${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_1.tif --calc=\"nan_to_num(A)\""
			gdal_calc.py -A temp_1.tif --outfile=${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_1.tif --calc="nan_to_num(A)"
			rm temp.tif temp_1.tif
			echo "gdalwarp -s_srs EPSG:32624 -t_srs EPSG:4326 ${file[i]} temp.tif"
			gdalwarp -s_srs EPSG:32624 -t_srs EPSG:4326 ${file[i]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_2.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_2.tif
			echo "gdal_calc.py -A temp_2.tif --outfile=${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_2.tif --calc=\"nan_to_num(A)\""
			gdal_calc.py -A temp_2.tif --outfile=${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_2.tif --calc="nan_to_num(A)"
			rm temp.tif temp_2.tif
			echo "/home/zez/zez_code/gdal_merge.py -n 0 -o ${temp_image} ${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_1.tif ${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_2.tif"
			/home/zez/zez_code/gdal_merge.py -n 0 -o ${temp_image} ${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_1.tif ${temp_dir}/${temp}_hh_GEE_sentinel_GRD_IW_helheim_2.tif
		else
	
			echo "gdalwarp -s_srs EPSG:32624 -t_srs EPSG:4326 ${file[i]} temp.tif"
			gdalwarp -s_srs EPSG:32624 -t_srs EPSG:4326 ${file[i]} temp.tif
			echo "gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_temp.tif"
			gdalwarp -overwrite -te -38.28 66.32 -38.07 66.41 -ts 1000 500 temp.tif temp_temp.tif
			gdal_calc.py -A temp_temp.tif --outfile=${temp_image} --calc="nan_to_num(A)"
		fi
	fi
	i=$[i+1]
	rm temp.tif temp_temp.tif
done
mv ${temp_dir}/* ${out_dir}/
rm  ${out_dir}/*_1*
rm  ${out_dir}/*_2*
cd ${out_dir}
	
