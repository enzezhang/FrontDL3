import argparse
import os
import numpy as np
from tqdm import tqdm

from mypath import Path
#from dataloaders import make_data_loader
from modeling.sync_batchnorm.replicate import patch_replication_callback
from modeling.deeplab import *
from utils.loss import SegmentationLosses
from utils.calculate_weights import calculate_weigths_labels
from utils.lr_scheduler import LR_Scheduler
from utils.saver import Saver
from utils.summaries import TensorboardSummary
from utils.metrics import Evaluator
from pytorchtools import EarlyStopping
from torch.autograd import Variable

early_stopping = EarlyStopping(patience=5, verbose=True)
import sys
HOME = os.path.expanduser('~')
basicCodes_path = HOME + '/code'
sys.path.append(basicCodes_path)
from datasetRS_Mar15 import *
import parameters


parser = argparse.ArgumentParser()
parser.add_argument('dataroot', help='path to test dataset ')
parser.add_argument('para', help='path to the parameter file')
parser.add_argument('list', help='path to the list file')

parser.add_argument('--workers', type=int, help='number of data loading workers', default=1)
parser.add_argument('--batchSize', type=int, default=1, help='input batch size')

parser.add_argument('--cuda', action='store_true', help='enables cuda')

parser.add_argument('--useBN', action='store_true', help='enalbes batch normalization')


parser.add_argument('--backbone', type=str, default='resnet',
                        choices=['resnet', 'xception', 'drn', 'mobilenet'])
parser.add_argument('--out-stride', type=int, default=16,
                        help='network output stride (default: 8)')
parser.add_argument('--sync-bn', type=bool, default=None,
                        help='whether to use sync bn (default: auto)')
parser.add_argument('--freeze-bn', type=bool, default=False,
                        help='whether to freeze bn parameters (default: False)')
parser.add_argument('--resume', default='', type=str, metavar='PATH', help='path to latest checkpoint (default: none)')

args = parser.parse_args()
print(args)

parameters.set_saved_parafile_path(args.para)
patch_w = parameters.get_digit_parameters("", "inf_patch_width", None, 'int')
patch_h = parameters.get_digit_parameters("", "inf_patch_height", None, 'int')
overlay_x = parameters.get_digit_parameters("", "inf_pixel_overlay_x", None, 'int')
overlay_y = parameters.get_digit_parameters("", "inf_pixel_overlay_y", None, 'int')

crop_height=parameters.get_digit_parameters("","crop_height_test",None,'int')
crop_width=parameters.get_digit_parameters("","crop_width_test",None,'int')

dataset = RemoteSensingImg(args.dataroot, args.list, patch_w, patch_h, overlay_x,overlay_y, train=False)
train_loader = torch.utils.data.DataLoader(dataset, batch_size=args.batchSize,
                                           num_workers=args.workers, shuffle=False)


model = DeepLab(num_classes=1,
                        backbone=args.backbone,
                        output_stride=args.out_stride,
                        sync_bn=args.sync_bn,
                        freeze_bn=args.freeze_bn)
if args.cuda:
    model.cuda()

if args.resume:
    if os.path.isfile(args.resume):
        checkpoint = torch.load(args.resume)
        args.start_epoch = checkpoint['epoch']
        #if args.cuda:
            #model.module.load_state_dict(checkpoint['state_dict'])
        #else:
        model.load_state_dict(checkpoint['state_dict'])
        best_pred = checkpoint['best_pred']

        print("=> loaded checkpoint '{}' (epoch {}) with best mIoU {}"
              .format(args.resume, checkpoint['epoch'],best_pred))




    else:
        print("=> no checkpoint found at '{}'".format(args.resume))
        assert False
else:
    print("Please input the check point files")

model.eval()



def saveImg(img, patch_info, binary=True, fName=''):
    """
    show image from given numpy image
    """
    img = img[0, 0, :, :]

    if binary:
        img = img > 0.5

    # img = Image.fromarray(np.uint8(img*255), mode='L')
    img = (img * 255).astype(rasterio.uint8)
    org_img_path = patch_info[0][0]
    boundary = patch_info[1]
    boundary = [item[0].cpu().data.numpy() for item in boundary]
    xsize = boundary[2]
    ysize = boundary[3]
    x_off=boundary[0]
    y_off=boundary[1]
    window = ((boundary[1]*1.0, boundary[1]*1.0 + ysize), (boundary[0]*1.0, boundary[0]*1.0 + xsize))
    #window=windows.Window(boundary[0],boundary[1],boundary[2],boundary[3])
    if fName:
        # img.save('inf_result/'+fName+'.png')
        with rasterio.open(org_img_path) as org:
            profile = org.profile
            new_transform = org.window_transform(window)
        # calculate new transform and update profile (transform, width, height)

        profile.update(dtype=rasterio.uint8, count=1, transform=new_transform, width=xsize, height=ysize)
        # set the block size    , it should be a multiple of 16 (TileLength must be a multiple of 16)
        if profile.has_key('blockxsize') and profile['blockxsize'] > xsize :
            if xsize%16==0:
                profile.update(blockxsize=xsize)
            else:
                profile.update(blockxsize=16)  #  profile.update(blockxsize=16)
        if profile.has_key('blockysize') and profile['blockysize'] > ysize :
            if ysize%16==0:
                profile.update(blockysize=ysize)
            else:
                profile.update(blockysize=16) #  profile.update(blockxsize=16)

        #print(profile['blockxsize'],profile['blockysize'],'xsize:%d ysize:%d'%(xsize,ysize))

        with rasterio.open('test_output/' + fName + '.tif', "w", **profile) as dst:
            dst.write(img, 1)

    else:
        img.show()


patch_number = len(train_loader)

for i, (x,patch_info) in enumerate(train_loader):
    # print(img_name[0])
    org_img = patch_info[0][0]
    file_name = os.path.splitext(os.path.basename(org_img))[0] + '_' + str(i)
    #file_name = patch_info[0]
    print("inferece (%.1f%%,%d/%d): %s " % (float(i+1)*100/patch_number,(i+1),patch_number,file_name))

    # b_crop = False
    # x_shape = x.size()
    # if x_shape[2] < crop_height or x_shape[3] < crop_width:
    #     b_crop = True
    #     x_expand = torch.zeros(x_shape[0],x_shape[1],crop_height,crop_width)
    #     x_expand[:,:,:x_shape[2],:x_shape[3]] = x
    #     y_pred = model(Variable(x_expand.cuda()))
    # else:
        # get output
    y_pred = model(Variable(x.cuda()))
    saveImg(y_pred.cpu().data.numpy(), patch_info, binary=True, fName=file_name + '_pred')

    # if b_crop is True:
    #     x = x_expand[:,:,:x_shape[2],:x_shape[3]]
    #     y_pred = y_pred[:,:,:x_shape[2],:x_shape[3]]
