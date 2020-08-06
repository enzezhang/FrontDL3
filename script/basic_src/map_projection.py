#!/usr/bin/env python
# Filename: map_projection.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 05 May, 2016
"""
import sys,basic

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

import io_function

def wkt_to_proj4(wkt):
    srs = osr.SpatialReference()
    srs.importFromWkt(wkt)
    proj4 = srs.ExportToProj4()
    if proj4 is False:
        basic.outputlogMessage('convert wkt to proj4 failed')
        return False
    return proj4

def proj4_to_wkt(proj4):
    srs = osr.SpatialReference()
    srs.ImportFromProj4(proj4)
    wkt = srs.ExportToWkt()
    if wkt is False:
        basic.outputlogMessage('convert wkt to proj4 failed')
        return False
    return wkt

def convert_points_SpatialRef(input_x,input_y,inSpatialRef,outSpatialRef):
    """
    convert points coordinate from old SRS to new SRS
    Args:
        input_x:input points x, list type
        input_y:input points y, list type
        inSpatialRef: object of old SpatialReference
        outSpatialRef:object of new SpatialReference

    Returns:True is successful, False Otherwise

    """
    if len(input_x) != len(input_y):
        basic.outputlogMessage('the count of input x or y is different')
        return False
    ncount = len(input_x)
    if ncount<1:
        basic.outputlogMessage('the count of input x less than 1')
        return False

    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    # print coordTransform
    # start = time.time()
    for i in range(0,ncount):
        # pointX = input_x[i]
        # pointY = input_y[i]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(input_x[i], input_y[i])
        # transform point
        point.Transform(coordTransform)
        input_x[i] = point.GetX()
        input_y[i] = point.GetY()
    # end = time.time()
    # cost = end - start #time in second
    # print cost

    return True

def convert_points_coordinate_proj4(input_x,input_y,in_proj4, out_proj4):
    inSpatialRef = osr.SpatialReference()
    # inSpatialRef.ImportFromEPSG(inputEPSG)
    inSpatialRef.ImportFromProj4(in_proj4)
    outSpatialRef = osr.SpatialReference()
    # outSpatialRef.ImportFromEPSG(outputEPSG)
    outSpatialRef.ImportFromProj4(out_proj4)
    return convert_points_SpatialRef(input_x,input_y,inSpatialRef,outSpatialRef)

def  convert_points_coordinate(input_x,input_y,inwkt, outwkt ):
    """
    convert points coordinate from old SRS(wkt format) to new SRS(wkt format)
    Args:
        input_x:points x, list type
        input_y:input points y, list type
        inwkt: complete wkt of old SRS
        outwkt: complete wkt of old SRS

    Returns: True is successful, False Otherwise

    """
    # if (isinstance(input_x,list) is False) or (isinstance(input_y,list) is False):
    #     syslog.outputlogMessage('input x or y type error')
    #     return False
    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    # inSpatialRef.ImportFromEPSG(inputEPSG)
    inSpatialRef.ImportFromWkt(inwkt)
    outSpatialRef = osr.SpatialReference()
    # outSpatialRef.ImportFromEPSG(outputEPSG)
    outSpatialRef.ImportFromWkt(outwkt)
    return convert_points_SpatialRef(input_x,input_y,inSpatialRef,outSpatialRef)

def get_raster_or_vector_srs_info(spatial_data,format):
    """
    get SRS(Spatial Reference System) information from raster or vector data
    Args:
        spatial_data: the path of raster or vector data
        format: Any of the usual GDAL/OGR forms(complete WKT, PROJ.4, EPSG:n or a file containing the SRS)

    Returns:the string of srs info in special format, False otherwise

    """
    if io_function.is_file_exist(spatial_data) is False:
        return False
    CommandString = 'gdalsrsinfo -o  '+ format +' '+  spatial_data
    result = basic.exec_command_string_output_string(CommandString)
    if result.find('ERROR') >=0:
        return False
    return result

def get_raster_or_vector_srs_info_wkt(spatial_data):
    """
    get SRS(Spatial Reference System) information from raster or vector data
    Args:
        spatial_data: the path of raster or vector data

    Returns:the string of srs info in WKT format, False otherwise

    """
    return get_raster_or_vector_srs_info(spatial_data,'wkt')

def get_raster_or_vector_srs_info_proj4(spatial_data):
    """
    get SRS(Spatial Reference System) information from raster or vector data
    Args:
        spatial_data: the path of raster or vector data

    Returns:the string of srs info in proj4 format, False otherwise

    """
    return get_raster_or_vector_srs_info(spatial_data, 'proj4')


def transforms_vector_srs(shapefile,t_srs,t_file):
    """
    convert vector file to target SRS(Spatial Reference System)
    Args:
        shapefile:input vector file
        t_srs:target SRS(Spatial Reference System)
        t_file:the output target file

    Returns:the output file path is successful, False Otherwise

    """
    if io_function.is_file_exist(shapefile) is False:
        return False;
    CommandString = 'ogr2ogr  -t_srs  ' +  t_srs + ' '+ t_file + ' '+ shapefile
    # if result.find('ERROR') >=0 or result.find('FAILURE'):
    #     return False
    return basic.exec_command_string_one_file(CommandString,t_file)

def transforms_raster_srs(rasterfile,t_srs,t_file,x_res,y_res):
    """
    convert raster file to target SRS(Spatial Reference System)
    Args:
        rasterfile:input raster file
        t_srs: target SRS(Spatial Reference System)
        t_file:the output target file
        x_res:set output file x-resolution (in target georeferenced units),assigning this value to make sure the resolution would not change in target file
        y_res:set output file y-resolution (in target georeferenced units),assigning this value to make sure the resolution would not change in target file

    Returns:the output file path is successful, False Otherwise

    """
    if io_function.is_file_exist(rasterfile) is False:
        return False
    x_res  = abs(x_res)
    y_res = abs(y_res)
    CommandString = 'gdalwarp  -r bilinear  -t_srs ' + t_srs  +' -tr ' +str(x_res)+ ' ' + str(y_res) \
                    +' '+ rasterfile +' '+ t_file
    return basic.exec_command_string_one_file(CommandString,t_file)

def transforms_raster_srs_to_base_image(rasterfile,baseimage,target_file,x_res,y_res):
    """
    convert raster file to target SRS(Spatial Reference System) of base image
    Args:
        rasterfile:input raster file
        baseimage:a image contains target srs info
        target_file:the output target file
        x_res:set output file x-resolution (in target georeferenced units)
        y_res:set output file y-resolution (in target georeferenced units)

    Returns:the output file path is successful, False Otherwise

    """
    if io_function.is_file_exist(baseimage) is False:
        return False
    target_srs = get_raster_or_vector_srs_info_proj4(baseimage)
    if target_srs is False:
        return False
    return transforms_raster_srs(rasterfile,target_srs,target_file,x_res,y_res)

if __name__=='__main__':
    length = len(sys.argv)
    if length == 6:
        rasterfile = sys.argv[1]
        baseimage = sys.argv[2]
        target_file = sys.argv[3]
        x_res = int(sys.argv[4])
        y_res = int(sys.argv[5])
        transforms_raster_srs_to_base_image(rasterfile, baseimage, target_file, x_res, y_res)
    else:
        print ('no Input error, Try to do like this:')
        print ('RSImageProcess.py  ....')
        sys.exit(1)

    pass