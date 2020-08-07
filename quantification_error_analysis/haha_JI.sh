#!/bin/bash
work_dir=$1
if [ -d $work_dir/polygon1 ];then
	echo "polygon1 exist"
	if [ -d $work_dir/polygon1/merge_two ];then
		echo "polygon1/merge_two exist"
	else
		mkdir $work_dir/polygon1/merge_two
	fi
else
	mkdir $work_dir/polygon1
	mkdir $work_dir/polygon1/merge_two
fi

if [ -d $work_dir/polygon2 ];then
	echo "polygon2 exist"
	if [ -d $work_dir/polygon2/merge_two ];then
                echo "polygon2/merge_two exist"
        else
                mkdir $work_dir/polygon2/merge_two
        fi
else
	mkdir $work_dir/polygon2
	mkdir $work_dir/polygon2/merge_two
fi

echo "bash /home/zez/data2/calving_front_deep_learning/script/separate_calving_front.sh $work_dir /home/zez/data2/calving_front_deep_learning/JI/cutting_polygon/saperate_polygon1.txt $work_dir/polygon1"
bash /home/zez/data2/calving_front_deep_learning/script/separate_calving_front.sh $work_dir /home/zez/data2/calving_front_deep_learning/JI/cutting_polygon/saperate_polygon1.txt $work_dir/polygon1

echo "bash /home/zez/data2/calving_front_deep_learning/script/separate_calving_front.sh $work_dir /home/zez/data2/calving_front_deep_learning/JI/cutting_polygon/saperate_polygon2.txt $work_dir/polygon2"
bash /home/zez/data2/calving_front_deep_learning/script/separate_calving_front.sh $work_dir /home/zez/data2/calving_front_deep_learning/JI/cutting_polygon/saperate_polygon2.txt $work_dir/polygon2



