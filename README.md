### Introduction

This is code for applyging deeplabv3+ to glacier front delineation. the code include pre-processing, network-training, and post-processing. The Deeplab3+ codes are based on https://github.com/jfzhang95/pytorch-deeplab-xception.

### Installation
  ```Shell
  git clone https://github.com/enzezhang/Front_DL3.git

  cd Front_DL3
  ```
### Install GDAL

```Shell
conda install gdal
```
### Install dependencies
  ```Shell
  pip install matplotlib pillow tensorboardX tqdm torch torchvision
  pip install Shapely pyshp pyproj rasterio
  ```
### Install GMT
```Shell
  sudo apt-get install gmt gmt-dcw gmt-gshhg
```
### Setting parameter

In the file para.ini, the user need to set working_root to ${User_dir}/Front_DL3, and code dir to ${User_dir}/Front_DL3/script.

Also need to set the patch size.

### Prepare CUDA

the CUDA version should be higher than 10.1.


###

### Run the code.
  ```Shell
  bash preparing_traindata.sh

  bash exe.sh

  bash preparing_influence.sh

  bash ./post-processing/exe_test_Helheim.sh
```
