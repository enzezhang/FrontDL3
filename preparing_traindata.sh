#!/usr/bin/env bash


para_file=para.ini
#plase modify this according to user's direction
para_py=./script/parameters.py


root=$(python2 ${para_py} -p ${para_file} working_root)
echo $root

mkdir ${root}/list
find ${root}/train/*.tif > list/image_list.txt
find ${root}/ground_truth/*.tif > list/label_list.txt

paste list/image_list.txt list/label_list.txt | awk ' { print $1 " " $2 }' > list/temp.txt
cp list/temp.txt list/train_aug.txt

