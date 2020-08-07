#!/bin/bash
source ~/.bashrc
para_file=para.ini
para_py=./script/parameters.py
work_root=$(python2 ${para_py} -p ${para_file} working_root)
#rm train_out.txt
#python ${work_root}/pytorch-deeplab-xception/train.py ${work_root} ${work_root}/${para_file} ${work_root}/list/train_aug.txt --backbone resnet --lr 0.005 --workers 1 --epochs 70 --patience 5 --batch-size 16 --gpu-ids 0,1,2,3,4,5,6,7 --resume resnet_no_stretch_ALOS1_Mar30.tar --ft --checkname resnet_no_stretch_ALOS1_JI_Kanger_May27.tar  --eval-interval 1 

#echo "python ${work_root}/pytorch-deeplab-xception/train.py ${work_root} ${work_root}/${para_file} ${work_root}/list/train_aug.txt --backbone drn  --lr 0.005 --workers 1 --epochs 30 --patience 4 --batch-size 8 --gpu-ids 0,1,2,3,4,5,6,7 --checkname drn_default_hist_eq_ALOS1_JI_Kanger_Jul20.tar  --eval-interval 1"
#python ${work_root}/pytorch-deeplab-xception/train.py ${work_root} ${work_root}/${para_file} ${work_root}/list/train_aug.txt --backbone drn  --lr 0.005 --workers 1 --epochs 30 --patience 4 --batch-size 8 --gpu-ids 0,1,2,3,4,5,6,7 --checkname drn_example.tar  --eval-interval 1
echo "python ${work_root}/pytorch-deeplab-xception/train.py ${work_root} ${work_root}/${para_file} ${work_root}/list/train_aug.txt --backbone mobilenet --lr 0.005 --workers 1 --epochs 60 --patience 5  --batch-size 32 --gpu-ids 0,1,2,3,4,5,6,7 --resume mobilenet_no_stretch_ALOS1_Mar23.tar --ft --checkname mobilenet_no_stretch_ALOS1_JI_Kanger_May27.tar  --eval-interval 1"

python ${work_root}/pytorch-deeplab-xception/train.py ${work_root} ${work_root}/${para_file} ${work_root}/list/train_aug.txt --backbone mobilenet --lr 0.005 --workers 1 --epochs 60 --patience 5  --batch-size 2 --gpu-ids 0,1,2,3,4,5,6,7 --checkname mobilenet_example.tar  --eval-interval 1
