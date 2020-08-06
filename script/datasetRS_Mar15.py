import torch.utils.data as data
import torch
import random
from scipy.ndimage import imread
import os
import os.path
import glob

import numpy as np

HOME = os.path.expanduser('~')
import sys

basicCodes_path = HOME + '/code'
#sys.path.insert(0, basicCodes_path)
from basic_src.RSImage import RSImageclass
import basic_src.basic as  basic
import split_image



class patchclass(object):
    """
    store the information of each patch (a small subset of the remote sensing images)
    """
    def __init__(self,org_img,boundary):
        self.org_img = org_img  # the original remote sensing images of this patch
        self.boundary=boundary      # the boundary of patch (xoff,yoff ,xsize, ysize) in pixel coordinate
    def boundary(self):
        return self.boundary

import rasterio
def read_patch(patch_obj,crop_height,crop_width):
    """
    Read all the pixel of the patch
    :param patch_obj: the instance of patchclass 
    :return: The array of pixel value
    """
    # window structure; expecting ((row_start, row_stop), (col_start, col_stop))
    boundary = patch_obj.boundary #(xoff,yoff ,xsize, ysize)
    window = ((boundary[1],boundary[1]+boundary[3])  ,  (boundary[0],boundary[0]+boundary[2]))
    #print(window)
    with rasterio.open(patch_obj.org_img) as img_obj:
        # read the all bands
        indexes = img_obj.indexes
        data = img_obj.read(indexes,window=window)
        if boundary[3]< crop_height or boundary[2] < crop_width:
            data_expend=np.zeros([data.shape[0],crop_height,crop_width])

            data_expend[:,:boundary[3],:boundary[2]]=data
            return data_expend
        else:
        # replace the nodata as zeros (means background)
            if img_obj.profile.has_key('nodata'):
                nodata = img_obj.profile['nodata']
                data[np.where(data==nodata)] = 0

            return data
def read_patch2(patch_obj):
    """
    Read all the pixel of the patch
    :param patch_obj: the instance of patchclass 
    :return: The array of pixel value
    """
    # window structure; expecting ((row_start, row_stop), (col_start, col_stop))
    boundary = patch_obj.boundary #(xoff,yoff ,xsize, ysize)
    window = ((boundary[1],boundary[1]+boundary[3])  ,  (boundary[0],boundary[0]+boundary[2]))
    #print(window)
    with rasterio.open(patch_obj.org_img) as img_obj:
        # read the all bands
        indexes = img_obj.indexes
        data = img_obj.read(indexes,window=window)

        # replace the nodata as zeros (means background)
        if img_obj.profile.has_key('nodata'):
            nodata = img_obj.profile['nodata']
            data[np.where(data==nodata)] = 0

        return data

def check_input_image_and_label(image_path, label_path):
    """
    check the input image and label, they should have same width, height, and projection 
    :param image_path: the path of image
    :param label_path: the path of label
    :return: (width, height) of image if successful, Otherwise (None, None).
    """

    img_obj = RSImageclass()
    if img_obj.open(image_path) is False:
        assert False
    label_obj = RSImageclass()
    if label_obj.open(label_path) is False:
        assert False
    # check width and height
    width = img_obj.GetWidth()
    height = img_obj.GetHeight()
    if width != label_obj.GetWidth() or height != label_obj.GetHeight():
        basic.outputlogMessage("Error, not the same width and height of image (%s) and label (%s)"%(image_path,label_path))
        assert False

    # check resolution
    a=img_obj.GetXresolution()#test
    b=label_obj.GetXresolution()
    c=img_obj.GetYresolution()
    d=label_obj.GetYresolution()
    if img_obj.GetXresolution() != label_obj.GetXresolution() or img_obj.GetYresolution() != label_obj.GetYresolution():
        basic.outputlogMessage(
            "warning, not the same resolution of image (%s) and label (%s)" % (image_path, label_path))
        #assert False

    # check projection
    if img_obj.GetProjection() != label_obj.GetProjection():
        basic.outputlogMessage(
            "warning, not the same projection of image (%s) and label (%s)" % (image_path, label_path))
    #     assert False

    return (width, height)


def make_dataset(root,list_txt,patch_w,patch_h,adj_overlay_x,adj_overlay_y,train=True):
    """
    get the patches information of the remote sensing images. 
    :param root: data root
    :param list_txt: a list file contain images (one row contain one train image and one label 
    image with space in the center if the input is for training; one row contain one image if it is for inference)
    :param patch_w: the width of the expected patch
    :param patch_h: the height of the expected patch
    :param adj_overlay: the extended distance (in pixel) to adjacent patch, make each patch has overlay with adjacent patch
    :param train:  indicate training or inference
    :return: dataset (list)
    """
    dataset = []

    crop_height=patch_h+2*adj_overlay_y
    crop_width=patch_w+2*adj_overlay_x
    if os.path.isfile(list_txt) is False:
        basic.outputlogMessage("error, file %s not exist"%list_txt)
        assert False

    with open(list_txt) as file_obj:
        files_list = file_obj.readlines()
    if len(files_list) < 1:
        basic.outputlogMessage("error, no file name in the %s" % list_txt)
        assert False

    if train:
        abandon_number = 0
        count_for_pure_image = 0
        for line in files_list:
            names_list = line.split()
            if len(names_list) < 1: # empty line
                continue
            image_name = names_list[0]
            label_name = names_list[1].strip()

            # img_path = os.path.join(root,image_name)
            # label_path = os.path.join(root,label_name)

            img_path=image_name
            label_path=label_name
            #
            (width,height) = check_input_image_and_label(img_path,label_path)

            # split the image and label
            patch_boundary = split_image.sliding_window(width, height, patch_w, patch_h, adj_overlay_x,adj_overlay_y)

            for patch in patch_boundary:
               # remove the patch small than model input size
               #  if patch[2] < crop_width or patch[3] < crop_height:# xSize < 480 or ySize < 480
               #
               #    # print ('not in edge mode')
               #      continue
                img_patch = patchclass(img_path,patch)
                label_patch = patchclass(label_path,patch)
                gt_test = read_patch2(label_patch)
                max=np.amax(gt_test)
                min=np.amin(gt_test)

                if max==min:
                    count_for_pure_image = count_for_pure_image+1
                    #print ("this is %d image"%min)
                    a=random.randint(0,1)
                    if a == 1:
                        dataset.append([img_patch, label_patch])
                    else:
                        abandon_number=abandon_number+1
                        continue
                else:
                    dataset.append([img_patch, label_patch])
        print("%d images are abandoned"%abandon_number)
        print("%d images are 1 or 0 images"%count_for_pure_image)

    else:
        for line in files_list:
                names_list = line.split()
                image_name = names_list[0].strip()

                img_path = image_name
                #
                img_obj = RSImageclass()
                if img_obj.open(img_path) is False:
                    assert False
                width = img_obj.GetWidth()
                height = img_obj.GetHeight()

                # split the image and label
                patch_boundary = split_image.sliding_window(width, height, patch_w, patch_h, adj_overlay_x,
                                                            adj_overlay_y)

                for patch in patch_boundary:
                    # need to handle the patch with smaller size
                    # if patch[2] < crop_width or patch[3] < crop_height:   # xSize < 480 or ySize < 480
                    #     continue
                    img_patch = patchclass(img_path, patch)

                    dataset.append(img_patch)

    return dataset


def getImg_count(dir):
    files = glob.glob(os.path.join(dir, '*.tif'))
    return len(files)


class RemoteSensingImg(data.Dataset):
    """
    Read dataset of kaggle ultrasound nerve segmentation dataset
    https://www.kaggle.com/c/ultrasound-nerve-segmentation
    """

    def __init__(self, root,list_txt,patch_w,patch_h,adj_overlay_x,adj_overlay_y,transform=None, train=True):
        self.train = train
        self.root = root
        # we cropped the image(the size of each patch, can be divided by 16 )
        self.nRow = patch_h+2*adj_overlay_y
        self.nCol =patch_w+2*adj_overlay_x

        self.patches = make_dataset(root, list_txt,patch_w,patch_h,adj_overlay_x,adj_overlay_y,train)

    def __getitem__(self, idx):
        if self.train:
            img_patch, gt_patch = self.patches[idx]
           # print(idx)

            img = read_patch(img_patch,self.nRow,self.nCol)
            # img.resize(self.nRow,self.nCol)
            img = img[:,0:self.nRow, 0:self.nCol]
            img = np.atleast_3d(img).astype(np.float32)
            if (img.max() - img.min()) < 0.01:
                pass
            else:
                img = (img - img.min()) / (img.max() - img.min())
            img = torch.from_numpy(img).float()

            gt = read_patch(gt_patch,self.nRow,self.nCol)
            gt=gt[:,0:self.nRow, 0:self.nCol]
            gt = np.atleast_3d(gt)
            # gt = gt / 255.0   # we don't need to scale
            gt = torch.from_numpy(gt).float()

            return img, gt
        else:
            img_patch = self.patches[idx]
            patch_info = [img_patch.org_img, img_patch.boundary]
            # img_name_noext = os.path.splitext(os.path.basename(img_patch.org_img))[0]+'_'+str(idx)
            img = read_patch2(img_patch)
            # img.resize(self.nRow,self.nCol)
            img = img[:, 0:self.nRow, 0:self.nCol]
            img = np.atleast_3d(img).astype(np.float32)
            if (img.max() - img.min()) < 0.01:
                pass
            else:
                img = (img - img.min()) / (img.max() - img.min())
            img = torch.from_numpy(img).float()
            return img, patch_info

    def __len__(self):
        count = len(self.patches)
        print("Image count is %d" % count)
        return count
        # if self.train:
        #     # train image count
        #     label_dir = os.path.join(self.root, 'split_labels')
        #     count = getImg_count(label_dir)
        #     print("Image count for training is %d" % count)
        #     return count
        #     # return 5635
        #     # test image count
        # else:
        #     label_dir = os.path.join(self.root, 'inf_split_images')
        #     count = getImg_count(label_dir)
        #     print("Image count for inference is %d" % count)
        #     return count
        #     # return 5508   # test image count


