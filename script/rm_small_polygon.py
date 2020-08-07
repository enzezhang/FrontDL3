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
import parameters

#############
#when this code gose wrong, check the threshold.


#############

def shape_from_pyshp_to_shapely(pyshp_shape,threshold):
    """
     convert pyshp object to shapely object
    :param pyshp_shape: pyshp (shapefile) object
    :return: shapely object if successful, False otherwise
    """

    parts_index = pyshp_shape.parts
    if len(parts_index) < 2:
        # Create a polygon with no holes
        record = Polygon(pyshp_shape.points)
    else:
        # Create a polygon with one or several holes
        seperate_parts = []
        parts_index.append(len(pyshp_shape.points))
        for i in range(0, len(parts_index)-1):
            points = pyshp_shape.points[parts_index[i]:parts_index[i+1]]
            seperate_parts.append(points)

        # if list(parts_index)==[0,121,130,135,140]:
        #     debug = 1

        # assuming the first part is exterior
        # exterior = seperate_parts[0]  # assuming the first part is exterior
        # interiors = [seperate_parts[i] for i in range(1,len(seperate_parts))]
        # assuming the last part is exterior
        # exterior = seperate_parts[len(parts_index)-2]
        # interiors = [seperate_parts[i] for i in range(0,len(seperate_parts)-2)]

        all_polygons = []
        length=len(seperate_parts)
        flag=0
        for i in range(length - 1):
            if len(seperate_parts[flag]) > len(seperate_parts[i + 1]):
                flag = flag
            else:
                flag = i + 1
        threshold=len(seperate_parts[flag])-1
        while(len(seperate_parts)>0):
            print ("the first polygon has %d points" % len(seperate_parts[0]))
            #if shapefile.signed_area(seperate_parts[0]) < 0: # the area of  ring is clockwise, it's not a hole
            #if shapefile.signed_area(seperate_parts[0]) > 0:
            if len(seperate_parts[0]) > threshold:
                print ("the exterior polygon has %d points" %len(seperate_parts[0]))
                exterior = tuple(seperate_parts[0])
                seperate_parts.remove(seperate_parts[0])

                # find all the holes attach to the first exterior
                interiors = []
                holes_points = []
                for points in seperate_parts:
                    #if shapefile.signed_area(points) >= 0: # the value >= 0 means the ring is counter-clockwise,  then they form a hole
                    if len(points)<threshold:
                        interiors.append(tuple(points))
                        holes_points.append(points)
                # remove the parts which are holes
                for points in holes_points:
                    seperate_parts.remove(points)
                    # else:
                    #     break
                if len(interiors) < 1:
                    interiors = None
                else:
                    interiors = tuple(interiors)
                polygon = Polygon(shell=exterior,holes=interiors)
                all_polygons.append(polygon)
            else:
                seperate_parts.remove(seperate_parts[0])
        if len(all_polygons) > 1:
            record = MultiPolygon(polygons=all_polygons)
        else:
            record = all_polygons[0]
    shapelytogeojson = shapely.geometry.mapping
    geoj = shapelytogeojson(record)
    # create empty pyshp shape
    record = shapefile._Shape()
    record.points = geoj["coordinates"][0]
    record.shapeType=5
    record.parts = [0]
    # # plot shape for checking
    # from matplotlib import pyplot as plt
    # from descartes import PolygonPatch
    # from math import sqrt
    # # from shapely.geometry import Polygon, LinearRing
    # # from shapely.ops import cascaded_union
    # BLUE = '#6699cc'
    # GRAY = '#999999'
    #
    # # plot these two polygons separately
    # fig = plt.figure(1,  dpi=90) #figsize=SIZE,
    # ax = fig.add_subplot(111)
    # poly1patch = PolygonPatch(record, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
    # # poly2patch = PolygonPatch(polygon2, ec=BLUE, alpha=0.5, zorder=2)
    # ax.add_patch(poly1patch)
    # # ax.add_patch(poly2patch)
    # boundary = record.bounds
    # xrange = [boundary[0], boundary[2]]
    # yrange = [boundary[1], boundary[3]]
    # ax.set_xlim(*xrange)
    # # ax.set_xticks(range(*xrange) + [xrange[-1]])
    # ax.set_ylim(*yrange)
    # # ax.set_yticks(range(*yrange) + [yrange[-1]])
    # # ax.set_aspect(1)
    #
    # plt.show()



    return record


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
        # print(area)
    return index

parser = argparse.ArgumentParser()
parser.add_argument('--input_shape', type=str, help='absolute path of input shape')
parser.add_argument('--output_shape', type=str, help='absolute path of output shape')
parser.add_argument('--threshold',type=int,help='JI is 1000 Helheim is 500')
args = parser.parse_args()





def main(input,output,threshold):
    input_shape=shapefile.Editor(input)
    length=len(input_shape.shapes())
    # print(len(input_shape._shapes[0].points))
    flag = 0
    # for i in range(length-1):
    #     if len(input_shape._shapes[flag].points)>500:
    #         flag=flag+1
    #     else:
    #         input_shape.delete(flag)
    for i in range(length-1):
        if len(input_shape._shapes[flag].points)>len(input_shape._shapes[i+1].points):
            flag=flag
        else:
            flag=i+1
    shapely=input_shape.shapes()[flag]
    print(len(shapely.points))
    output_shapely=shape_from_pyshp_to_shapely(shapely,threshold)
    output_shape=shapefile.Writer()
    output_shape.shapeType=input_shape.shapeType

    output_shape.field('DN', fieldType="N", size="9")
    output_shape._shapes.append(output_shapely)
    rec=[1]
    output_shape.records.append(rec)
    input_prj=os.path.splitext(input)[0] + ".prj"
    output_prj=os.path.splitext(output)[0] + ".prj"
    os.system('cp '+input_prj+' '+output_prj)
    output_shape.save(output)






if (__name__ == '__main__'):

    main(args.input_shape,args.output_shape,args.threshold)

# sf=shapefile.Reader('/home/zez/test_deep_learning/u_net/post_process_test/20090917_out.shp')
#
# #b=shapefile.Reader('/home/zez/test_deep_learning/u_net/post_process_test/20090917_out_test.shp')
#
# shape_data=sf.shapes()
#
# index=index_of_small_polygon(shape_data)
# e = shapefile.Editor('/home/zez/test_deep_learning/u_net/post_process_test/20090917_out.shp')
# index2=np.where(index==1)[0]

# for temp in index2:
#     e.delete(0)
# #
# shape_data=e.shapes()
# polygon=shape_data[0]
#
# (lo, la) = extract_points(polygon.points)
# cop={"type": "Polygon", "coordinates": [zip(lo, la)]}
# b=shape(cop)
# c=b.buffer(0.0001)
#
# lo,la=c.exterior.coords.xy
#
# points=put_back_points(lo,la)
# thefile = open('test.txt', 'w')
# for item in points:
#     thefile.write("%6.3f %6.3f\n" % (item[0],item[1]))
# # #e.delete(0)
# test=[[[1,5],[5,5],[5,1],[3,3],[1,1]]]
# haha=[]
# haha.append(points)
# w = shapefile.Writer()
# w.poly(parts=haha)
#
#
#
# w.save('/home/zez/test_deep_learning/u_net/post_process_test/20090917_out_test')
#
# print('haha')
