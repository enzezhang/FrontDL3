### Introduction

This is code for applyging deeplabv3+ to glacier front delineation. the code include pre-processing, network-training, and post-processing. The Deeplab3+ codes are based on https://github.com/jfzhang95/pytorch-deeplab-xception.

### Installation
  ```Shell
  git clone https://github.com/enzezhang/Front_DL3.git

  cd Front_DL3
  ```
### Install anaconda2 (not 3)

https://repo.anaconda.com/archive/

Choose Anaconda2-2019.10-Linux-x86_64.sh

```Shell
bash Anaconda2-2019.10-Linux-x86_64.sh
```
### install gdal_contrast_stretch 

gdal_contrast_stretch (for normalizing the histogram)
 https://github.com/gina-alaska/dans-gdal-scripts


### Install GDAL

```Shell
conda install gdal
```
There could be some library issues.
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

Also need to set the patch size and the data_path.

vi para.in

####root dir, contain input images, training files, and sub folders (for test)
working_root =~/Front_DL3 #(this is where you put Front_DL3 codes)
data_path=~/greenland #(this is the path of data files, it contains all the images of Greenland glaciers)
#### codes dir
codes_dir =~/Front_DL3/script #(for script folder within Front_DL3)

### Prepare CUDA

the CUDA version should be higher than 10.1.

###

### Download the network to ${User_dir}/Front_DL3/

https://www.dropbox.com/s/c6xmoi8exakk4gy/drn_Jan28_2021_single_0.01_aug_momentum_0.9_from_stretch_16_batch_size.tar?dl=0

Do not untar it.
###


### train the network.
  ```Shell
 
  bash preparing_traindata.sh
  ```
  This code will generate list/train_aug.txt that shows the training image and corresponding ground truth image (the file names of these two images are identical). 
``` Shell
  bash exe.sh
  ```
### inference the results
```Shell
  bash preparing_influence.sh ${User_dir}/Front_DL3/train

  bash exe_inference.sh ${User_dir}/Front_DL3/polygon/cut_polygon.gmt drn_Jan28_2021_single_0.01_aug_momentum_0.9_from_stretch_16_batch_size.tar
```
need to use the full path
