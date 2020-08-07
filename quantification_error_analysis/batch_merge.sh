#!/bin/bash
work_dir=$1
if [ -d $work_dir/merge_two ];then
	echo "merge two exist"
else
	mkdir $work_dir/merge_two
fi

echo "bash /home/zez/data2/calving_front_deep_learning/script/merge_two_calving2.sh $work_dir $work_dir/merge_two"
bash /home/zez/data2/calving_front_deep_learning/script/merge_two_calving2.sh $work_dir $work_dir/merge_two



