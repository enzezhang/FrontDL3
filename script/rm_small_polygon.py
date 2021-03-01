import shapefile

import argparse

from shapely.geometry import Polygon
from shapely.geometry import shape

from pyproj import Proj
import numpy as np
import os

#############



#############

def shape_from_pyshp_to_shapely(pyshp_shape):
    """
     convert pyshp object to shapely object
    :param pyshp_shape: pyshp (shapefile) object
    :return: shapely object if successful, False otherwise
    """

    parts_index = pyshp_shape.parts
    if len(parts_index) < 2:
        # Create a polygon with no holes
        exterior = list(pyshp_shape.points)
    else:
        # find the largest polygon
        seperate_parts = []
        parts_index.append(len(pyshp_shape.points))
        for i in range(0, len(parts_index)-1):
            points = pyshp_shape.points[parts_index[i]:parts_index[i+1]]
            seperate_parts.append(list(points))



        length=len(seperate_parts)
        flag=0
        for i in range(length - 1):
            if len(seperate_parts[flag]) > len(seperate_parts[i + 1]):
                flag = flag
            else:
                flag = i + 1
        print ("the largest polygon has %d points" % len(seperate_parts[flag]))

        exterior = list(seperate_parts[flag])



    return exterior


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


def index_of_small_polygon(shape_data):
    length=len(shape_data)
    index=np.zeros([length,1])
    for i in range(length):
        polygon=shape_data[i]
        (lo, la) = extract_points(polygon.points)
        pa = Proj("+proj=stere +lat_0=90.0 +lat_ts=70 +lon_0=-45")
        x, y = pa(lo, la)
        cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
        b=shape(cop)
        area = shape(cop).area
        if area<100000:
            index[i]=1
    return index

parser = argparse.ArgumentParser()
parser.add_argument('--input_shape', type=str, help='absolute path of input shape')
parser.add_argument('--output_shape', type=str, help='absolute path of output shape')
args = parser.parse_args()





def main(input,output):
    input_shape=shapefile.Reader(input).shapes()
    length=len(input_shape)

    flag = 0
    for i in range(length-1):
        if len(input_shape[flag].points)>len(input_shape[i+1].points):
            flag=flag
        else:
            flag=i+1

    shapely=input_shape[flag]
    print(len(shapely.points))
    output_shapely=[shape_from_pyshp_to_shapely(shapely)]





    output_shape=shapefile.Writer(output)
    # output_shape.poly(output_shapely)
    output_shape.shapeType=input_shape[0].shapeType
    output_shape.poly(output_shapely)

    output_shape.field('name', 'C')

    output_shape.record('polygon')
    input_prj=os.path.splitext(input)[0] + ".prj"
    output_prj=os.path.splitext(output)[0] + ".prj"
    os.system('cp '+input_prj+' '+output_prj)






if (__name__ == '__main__'):

    main(args.input_shape,args.output_shape)

