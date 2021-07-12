#!/usr/bin/env bash

python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/image_augment.py list/augment_figure_Apr17.txt -o ./new_prepared/figure
#python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/image_augment.py ./list/20131023_label.txt -o ./train/label_figure
python /home/zez/test_deep_learning/u_net/Unet_pytorch-master_Dec5/image_augment.py list/augment_label_Apr17.txt -o ./new_prepared/label_figure
