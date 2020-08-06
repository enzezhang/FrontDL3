#import requests
#import cStringIO
import numpy as np
#from PIL import Image
#from timer import Timer
import argparse
import cv2
import rasterio
import numpy as np
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser()


parser.add_argument('--input', help='input image')
parser.add_argument('--output',help='output image')
args = parser.parse_args()
print(args)


name=args.input
name_out=args.output
img = cv2.imread(name,cv2.IMREAD_UNCHANGED)

#img = cv2.imread(name)
#with rasterio.open(name) as img:

height=img.shape[0]
length=img.shape[1]
#profile=img.profile
x_looking=5
y_looking=5
y_size=int(height)/y_looking
x_size=int(length)/x_looking


# im = Image.open(name)
for i in range(3):
    out_image = cv2.medianBlur(img,5)
    print i
    img=out_image






# hight=im.size[0]
# length=im.size[1]
# hight_new=np.rint(hight/4)
# length_new=np.rint(length/4)
#imarray = np.array(im)
# img=im.thumbnail((hight_new,length_new),Image.ANTIALIAS)
# plt.figure()
# plt.subplot(1,2,1),plt.imshow(img,'gray')
# plt.subplot(1,2,2),plt.imshow(out_image,'gray')
# plt.show()
cv2.imwrite(name_out,out_image)



#
# new_im = Image.fromarray(new_image_array)
# new_im.save('/home/zez/JI/TSX/Harvard-CS205-Parallel-Programming-Final-master/20110216_stretch_comprassed_anisodiff.tif')

#new_image = anisodiff_vec(imarray, 2)


