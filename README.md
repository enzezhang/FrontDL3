This is code for applyging deeplabv3+ to glacier front delineation. the code include pre-processing, network-training, and post-processing. The Deeplab3+ codes are based on https://github.com/jfzhang95/pytorch-deeplab-xception.

1 Install

git clone https://github.com/enzezhang/Front_DL3.git

cd Front_DL3

2 Install dependencies

pip install matplotlib pillow tensorboardX tqdm

3 Setting parameter

In the file para.ini, the user need to set working_root, ${User_dir}/Front_DL3, and code dir, ${User_dir}/Front_DL3/script.

Also need to set the patch size.

3 Change dir

In some script, the direction should be changed.

(1) In pytorch-deeplab-xception/train.py and pytorch-deeplab-xception/inference.py, basicCodes_path need to be set.

4 Run the code.

(1) bash preparing_traindata.sh

(2) bash exe.sh

(3) bash preparing_influence.sh

(4) bash ./post-processing/exe_test_Helheim.sh
