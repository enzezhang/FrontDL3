import shapefile
from osgeo import ogr
import argparse
import shapely
from shapely.geometry import Polygon
from shapely.geometry import shape
from shapely.geometry import MultiPolygon
from pyproj import Proj
import numpy as np
import os
import datetime
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input gmt file')
parser.add_argument('--date', help="input date")
parser.add_argument('--reference',help="reference gmt file")
args = parser.parse_args()

def PolyArea(x,y):
    return -0.5*(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
def convert_time(date):
    date=str(date)
    year=int(date[0:4])
    month=int(date[4:6])
    day=int(date[6:8])
    d1 = datetime.datetime(year,month,day)
    d2=datetime.datetime(year,1,1)
    intervel=d1-d2
    out_date=year+(intervel.days)/365.25
    return out_date

def area(data):

    lo=data[:,0]
    la=data[:,1]

    pa = Proj("+proj=stere +lat_0=90.0 +lat_ts=70 +lon_0=-45")

    x, y = pa(lo, la)
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    b = shape(cop)
    return PolyArea(x,y)

def test():
    x1=np.array([0,1,1,0])
    y1=np.array([0,0,1,1])
    x2=np.array([0,0,1,1])
    y2=np.array([0,1,1,0])
    x3=np.array([0,1,0,1])
    y3=np.array([0,1,1,0])
    cop1={"type": "Polygon", "coordinates": [zip(x1, y1)]}
    cop2={"type": "Polygon", "coordinates": [zip(x2, y2)]}
    cop3 = {"type": "Polygon", "coordinates": [zip(x3, y3)]}
    b1=shape(cop1)
    b2=shape(cop2)
    b3=shape(cop3)
    print(b1.area,b2.area)
def ref_length(input_data):
    lo = input_data[:, 0]
    la = input_data[:, 1]
    pa = Proj("+proj=stere +lat_0=90.0 +lat_ts=70 +lon_0=-45")

    x, y = pa(lo, la)
    length = 0
    x_1 = x[0:len(x) - 1]
    x_2 = x[1:len(x)]
    y_1 = y[0:len(y) - 1]
    y_2 = y[1:len(y)]
    dis_array = ((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2) ** 0.5
    dis = np.sum(dis_array)
    return (dis)

if __name__=='__main__':
    input_data = np.loadtxt(args.input)
    ref_data=np.loadtxt(args.reference)
    area_data=area(input_data)
    reflength=ref_length(ref_data)
    date=convert_time(args.date)
    print("%f %f %f %s"%(area_data/1e7,area_data/reflength,date,args.date))
    #test()
