
import sys
import numpy as np
from shapely.geometry import shape
from pyproj import Proj
from scipy.spatial import ConvexHull
import argparse
def tri_order(x,y):
    if ((x[1]-x[0])*(y[2]-y[1])-(x[2]-x[1])*(y[1]-y[0])>0):
        # print('clock wise')
        return True
    elif ((x[1]-x[0])*(y[2]-y[1])-(x[2]-x[1])*(y[1]-y[0])<0):
        # print("conter clock wise")
        return False
    else:
        #print("the triangle is not in the correct format")
	pass
def extract_points(points):

    length=len(points)
    lo=np.zeros([length,1])
    la=np.zeros([length,1])
    for i in range(length):
        point=points[i]
        lo[i], la[i]=point[0], point[1]
    return lo,la



def vibration_freq(x,y):
    clock=0
    conter_clock=0
    for i in range(len(x)-2):
        if tri_order(x[i:i+3],y[i:i+3]):
            clock+=1
        else:
            conter_clock+=1
    notch_norm=(float(clock)/(len(x)-3))
    freq=16*np.power((notch_norm-0.5),4)-8*np.power((notch_norm-0.5),2)+1
    # print("clock points are %d, conter clock points are %d"%(clock,conter_clock))
    # print("notch norm is %f"%(notch_norm))
    # print("frequency of vibration is %f"%(freq))
    return notch_norm



def cal_area(x,y):
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    b = shape(cop)
    c = b.buffer(-0.00000000001)
    if (c.area > b.area):
        area = c.area * 2 - b.area
    elif ((b.area - c.area) > 100):
        area = c.area * 2 + b.area
    else:
        area = c.area
    return area

def cal_length(x,y):
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    b = shape(cop)
    return b.length


def vibration_amp_conv(x,y):
    points = np.vstack((x, y)).T
    points2 = np.random.rand(30, 2)
    length_ori=cal_length(x,y)
    area_ori=cal_area(x,y)
    hull=ConvexHull(points)
    hull_points=points[hull.vertices]
    length_hull=cal_length(hull_points[:,0],hull_points[:,1])
    area_hull=cal_area(hull_points[:,0],hull_points[:,1])
    amp=(length_ori-length_hull)/length_ori
    conv=(area_hull-area_ori)/area_hull
    return amp,conv









def main(input,date):
    data=np.loadtxt(input)
    lo=data[:,0]
    la=data[:,1]
    pa = Proj("+proj=stere +lat_0=90.0 +lat_ts=70 +lon_0=-45")
    x, y = pa(lo, la)
    freq=vibration_freq(x,y)
    amp,conv=vibration_amp_conv(x,y)
    compl=0.8*amp*freq+0.2*conv
    print("%s %f"%(date,compl))


parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='absolute path of input shape')
parser.add_argument('--date', type=str, help='date of input shape')
args = parser.parse_args()




if (__name__ == '__main__'):
    main(args.input, args.date)
