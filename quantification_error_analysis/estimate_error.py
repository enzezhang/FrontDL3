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

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='absolute path of input shape')
parser.add_argument('--date', type=str, help='date of input shape')
parser.add_argument('--label', type=str, help='absolute path of input shape')
args = parser.parse_args()
def extract_points(points):

    length=len(points)
    lo=np.zeros([length,1])
    la=np.zeros([length,1])
    for i in range(length):
        point=points[i]
        lo[i], la[i]=point[0], point[1]
    return lo,la

def put_back_points(lo,la):
    length=len(lo)
    points=[]

    for i in range(length):
        point=(lo[i],la[i])
        points.append(point)
    return points


def area(shape_data,date):
    polygon = shape_data[0]
    (lo, la) = extract_points(polygon.points)

    pa = Proj("+proj=stere +lat_0=90.0 +lat_ts=70 +lon_0=-45")

    x, y = pa(lo, la)
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    b = shape(cop)
    c = b.buffer(-0.00000000001)
    if (c.area>b.area):
        area=c.area*2-b.area
    elif ((b.area-c.area)>100):
        area=c.area*2+b.area
    else:
	area=c.area
    # lo, la = c.envelope.exterior.coords.xy
    # point_test=np.array(c)
    # points = put_back_points(lo, la)
    # haha = []
    # haha.append(points)
    #w = shapefile.Writer()
    #w.poly(parts=haha)
    #
    # name=date+'_buffer_0.1_merge.shp'
    # driver = ogr.GetDriverByName('Esri Shapefile')
    # ds = driver.CreateDataSource(name)
    # layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    # # Add one attribute
    # layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    # defn = layer.GetLayerDefn()
    #
    # ## If there are multiple geometries, put the "for" loop here
    #
    # # Create a new feature (attribute and geometry)
    # feat = ogr.Feature(defn)
    # feat.SetField('id', 123)
    #
    # # Make a geometry, from Shapely object
    # geom = ogr.CreateGeometryFromWkb(c.wkb)
    # feat.SetGeometry(geom)
    #
    # layer.CreateFeature(feat)
    # feat = geom = None  # destroy these
    #
    # # Save and close everything
    # ds = layer = feat = geom = None
    return area


def cal_length(input):
    input_data = np.loadtxt(input)

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

def main(input,label,date):
    input_shape = shapefile.Editor(input)
    shape_data = input_shape.shapes()
    error_area=area(shape_data,date)

    dis=cal_length(label)

    result=error_area/dis
    print("%s %f %f %f " % (date,error_area,dis,result))
    #shape_buffer.save(output)
    #
    # a=[0,1,1,0]
    # b=[1,0,1,0]
    # cop = {"type": "Polygon", "coordinates": [zip(a, b)]}
    # test=shape(cop)
    # print('haha')




if (__name__ == '__main__'):

    main(args.input,args.label,args.date)
