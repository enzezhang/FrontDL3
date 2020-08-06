#!/usr/bin/env python
# Filename: DemConvert.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 25 June, 2016
"""


import sys,basic,urllib,urllib2,httplib,RSImageProcess,RSImage,parameters
# from basic import LogMessage
from RSImage import RSImageclass
from RSImageProcess import RSImgProclass
import numpy,commands
from numpy import *
from optparse import OptionParser
import io_function
import map_projection

from HTMLParser import HTMLParser

def degree_to_dms(dd_s):
    degrees = int(dd_s)
    temp = 60 * (dd_s - degrees)
    minutes = int(temp)
    seconds = 60 * (temp - minutes)
    # print degrees, minutes, seconds
    return (degrees, minutes, seconds)


def get_geoid_height(LatitudeDeg,LatitudeMin,LatitudeSec,LongitudeDeg,LongitudeMin,LongitudeSec,nodata):
    # nodata = -9999
    geoid_height = nodata

    # Origin= "http://earth-info.nga.mil"
    # # POST = '/nga-bin/gandg-bin/intpt.ci'
    # # POST = '/GandG/wgs84/gravitymod/egm96/intpt.html'
    # url = Origin #+ POST
    # data = [('LatitudeDeg',str(LatitudeDeg)),('LongitudeDeg',str(LongitudeDeg)),('LatitudeMin',str(LatitudeMin)),\
    #         ('LongitudeMin',str(LongitudeMin)),('LatitudeSec',str(LatitudeSec)),('LongitudeSec',str(LongitudeSec)),\
    #         ('Units',str(Units))]
    # getString = url + "?" + urllib.urlencode(data)
    # syslog.outputlogMessage(getString)
    #
    # req = urllib2.Request(getString)
    # fd = urllib2.urlopen(req)
    # while 1:
    #     data = fd.read(1024)
    #     if not len(data):
    #         break
    #     sys.stdout.write(data)

    #https://www.unavco.org/software/geodetic-utilities/geoid-height-calculator/geoid-height-calculator.html
    params = urllib.urlencode({'lat':str(LatitudeDeg),'lat_m':str(LatitudeMin),'lat_s':str(LatitudeSec),\
                'lon':str(LongitudeDeg),'lon_m':str(LongitudeMin),'lon_s':str(LongitudeSec),\
                 'gpsheight':str(0),'submit':'submit'})

    # syslog.outputlogMessage(str(params))

    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection("jules.unavco.org")
    conn.request(method="POST",url="/Geoid/Geoid",body=params,headers=headers)
    response = conn.getresponse()
    status = response.status
    text_got = response.read()
    conn.close()
    if status != 200:
        basic.outputlogMessage(text_got)
        return False
    # parser = HTMLParser()
    # print text_got
    # try:
    #     parser.feed(text_got)
    #     geoidheight_str = parser.handle_data('body')
    # except :
    #     syslog.outputlogMessage('parser error')
    #     syslog.outputlogMessage(text_got)
    #     return False

    loc = text_got.find('Geoid')
    if loc< 0:
        return False
    sub_str = text_got[loc:loc+40]
    sub_str = sub_str[sub_str.find('=')+1:sub_str.find('\n')]

    try:
        geoid_height = float(sub_str)
    except ValueError:
        basic.outputlogMessage(str(ValueError))
        return False

    # parser.close()
    return geoid_height

def get_range_geoid_height(outputfile,up,down,left,right):
    nodata = -999999
    delt_x = 3.0/60
    delt_y = 3.0/60

    width = int((right - left)/delt_x+0.5)
    height = int((up-down)/delt_y + 0.5)

    geoid_height = numpy.zeros((height,width),numpy.float)
    for i in range(0,height):
        for j in range(0,width):
            Longitude = left + delt_x*j
            Latitude = down + delt_y*i
            (LongitudeDeg,LongitudeMin,LongitudeSec) = degree_to_dms(Longitude)
            (LatitudeDeg,LatitudeMin,LatitudeSec) = degree_to_dms(Latitude)
            value = get_geoid_height(LatitudeDeg,LatitudeMin,LatitudeSec,LongitudeDeg,LongitudeMin,LongitudeSec,nodata)
            if value is False:
                return False
            basic.outputlogMessage('Longitude=%f, Latitude=%f, geoid = %f'%(Longitude,Latitude,value))
            geoid_height[i,j] = value

    srs_longlat_wkt = "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.01745329251994328]]"
    # proj4 = '\'+proj=longlat +datum=WGS84 +no_defs\''
    # adfGeoTransform[0] /* top left x */
    # adfGeoTransform[1] /* w-e pixel resolution */
    # adfGeoTransform[2] /* 0 */
    # adfGeoTransform[3] /* top left y */
    # adfGeoTransform[4] /* 0 */
    # adfGeoTransform[5] /* n-s pixel resolution (negative value) */

    trans = [left,delt_x,0,up,0,delt_y*(-1)]
    RSImageProcess.save_numpy_2d_array_to_image_tif(outputfile,geoid_height,\
        6,tuple(trans),srs_longlat_wkt,nodata)

    return True

def get_geoimage_range_geoid_height(outputfile,ref_image):
    #convert srs
    ref_img_obj = RSImageclass()
    if not ref_img_obj.open(ref_image):
        return False
    # x_res = ref_img_obj.GetXresolution()
    # y_res = ref_img_obj.GetYresolution()
    width = ref_img_obj.GetWidth()
    height = ref_img_obj.GetHeight()

    img_pro = RSImgProclass()
    ref_image_data = img_pro.Read_Image_band_data_to_numpy_array_all_pixel(1,ref_image)
    if ref_image_data is False:
        return False

    nodata = parameters.get_nodata_value()
    Image_array = ref_image_data.reshape(height,width)
    start_x = ref_img_obj.GetStartX()
    start_y = ref_img_obj.GetStartY()
    resolution_x = ref_img_obj.GetXresolution()
    resolution_y = ref_img_obj.GetYresolution()
    ref_img_WKT = ref_img_obj.GetProjection()
    # ref_img_WKT = RSImageProcess.get_raster_or_vector_srs_info_wkt(ref_image,syslog)

    (i,j)= numpy.where(Image_array != nodata)
    input_x = start_x + j*resolution_x
    input_y = start_y + i*resolution_y

    # srs_longlat_prj4 = '\'+proj=longlat +datum=WGS84 +no_defs\''
    # intput_proj4 = RSImage.wkt_to_proj4(ref_img_WKT,syslog)
    # intput_proj4 = RSImageProcess.get_raster_or_vector_srs_info_proj4(ref_image,syslog)
    # map_projection.convert_points_coordinate_proj4(input_x,input_y,intput_proj4,srs_longlat_prj4,syslog)

    srs_longlat_wkt = "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.01745329251994328]]"
    map_projection.convert_points_coordinate(input_x,input_y,ref_img_WKT,srs_longlat_wkt)

    tempsave_str = []
    save_point_txt_file = 'TXTgeoid_'+os.path.splitext(os.path.basename(ref_image))[0]+'.txt'
    if os.path.isfile(save_point_txt_file):
        file_object = open(save_point_txt_file,'r')
        savepoints = file_object.readlines()
        for point in savepoints:
            tempsave_str.append(point)
        file_object.close()
        io_function.delete_file_or_dir(save_point_txt_file)
    file_object = open(save_point_txt_file,'a')

    nsize = Image_array.size
    Image_array = Image_array.astype(numpy.float32)
    for index in range(0,nsize):
        lon_deg = input_x[index]
        lat_deg = input_y[index]
        if index< len(tempsave_str):
            temp_point = tempsave_str[index].split()
            value = float(temp_point[2])
        else:
            (LongitudeDeg,LongitudeMin,LongitudeSec) = degree_to_dms(lon_deg)
            (LatitudeDeg,LatitudeMin,LatitudeSec) = degree_to_dms(lat_deg)
            value = get_geoid_height(LatitudeDeg,LatitudeMin,LatitudeSec,LongitudeDeg,LongitudeMin,LongitudeSec,nodata)
            if value is False:
                break
        saved_point = ('%f  %f  %f'%(lon_deg,lat_deg,value))
        print saved_point
        # tempsave_str.append(saved_point)
        file_object.writelines(saved_point+'\n')
        file_object.flush()
        basic.outputlogMessage('Longitude=%f, Latitude=%f, geoid = %f'%(lon_deg,lat_deg,value))
        # Image_array[index] = value
        Image_array[i[index],j[index]] = value
        print (i[index],j[index],Image_array[i[index],j[index]])


    file_object.close()
    if index != (nsize-1):
        return False
    #save geoid height
    RSImageProcess.save_numpy_2d_array_to_image_tif(outputfile,Image_array,\
        6,ref_img_obj.GetGeoTransform(),ref_img_WKT,nodata)

    return True

def convert_orthometricH_to_elliopsoidalH(output,orthometricH_file,geoidHfile):
    if io_function.is_file_exist(orthometricH_file) is False or io_function.is_file_exist(geoidHfile) is False:
        return False

    orthom_obj = RSImageclass()
    if orthom_obj.open(orthometricH_file) is False:
        return False
    geoidH_obj = RSImageclass()
    if geoidH_obj.open(geoidHfile) is False:
        return False

    Nodata = parameters.get_nodata_value()

    x_res = orthom_obj.GetXresolution()
    y_res = orthom_obj.GetYresolution()
    x_res_geoid = geoidH_obj.GetXresolution()
    y_res_geoid = geoidH_obj.GetYresolution()

    orthom_prj = orthom_obj.GetProjection()
    geoid_prj = geoidH_obj.GetProjection()

    #check projection and resolution, and convert it if need
    #use orthometricH_file as base image
    if x_res != x_res_geoid or y_res != y_res_geoid or orthom_prj!=geoid_prj:
        geoid_convertfile = io_function.get_name_by_adding_tail(geoidHfile,'tran')
        if os.path.isfile(geoid_convertfile) is False:
            if RSImageProcess.transforms_raster_srs(geoidHfile,orthom_prj,geoid_convertfile,abs(x_res),abs(y_res)) is False:
                return False
        else:
            basic.outputlogMessage(geoid_convertfile +' already exist')

    #sub geoidHfile base on the small one
    (ulx,uly,lrx,lry) = RSImageProcess.get_image_proj_extent(orthometricH_file)
    if ulx is False:
        return False
    geoid_convertfile_sub = io_function.get_name_by_adding_tail(geoid_convertfile,'sub')
    if os.path.isfile(geoid_convertfile_sub) is False:
        result = RSImageProcess.subset_image_projwin(geoid_convertfile_sub,geoid_convertfile,ulx,uly,lrx,lry)
        if result is False:
            return False
    else:
        basic.outputlogMessage(geoid_convertfile_sub +' already exist')

    ##caculate elliopsoidal height
    # orthometricH_data = img_pro.Read_Image_band_data_to_numpy_array_all_pixel(1,orthometricH_file)
    # img_pro = None
    # img_pro = RSImgProclass(syslog)
    # geoidH_data = img_pro.Read_Image_band_data_to_numpy_array_all_pixel(1,geoid_convertfile_sub)
    # img_pro = None
    # if orthometricH_data.shape != geoidH_data.shape:
    #     syslog.outputlogMessage("the shape of orthometricH_data and geoidH_data is different")
    #     return False
    #
    # nodata = parameters.get_nodata_value(syslog)
    # width  = orthom_obj.GetWidth()
    # height = orthom_obj.GetHeight()
    # orthometricH_data = orthometricH_data.astype(numpy.float32)
    # geoidH_data = geoidH_data.astype(numpy.float32)
    # elliopsoidalH = orthometricH_data + geoidH_data
    # elliopsoidalH = elliopsoidalH.reshape(height,width)
    #
    # RSImageProcess.save_numpy_2d_array_to_image_tif(output,elliopsoidalH,6,\
    #             orthom_obj.GetGeoTransform(),orthom_obj.GetProjection(),nodata,syslog)
    #
    # orthom_obj = None
    # geoidH_obj = None

    CommandString = 'gdal_calc.py  -A '+orthometricH_file + ' -B ' + geoid_convertfile_sub +\
      ' --NoDataValue='+str(Nodata)  +' --outfile='+output +  ' --calc="A+B"'
    if RSImageProcess.exec_commond_string_one_file(CommandString,output) is False:
        return False
    else:
        basic.outputlogMessage("converting orthometric Height to elliopsoidal Height is completed")

    return True

def prepare_GTOPO30_for_Jakobshavn(workdir):
    #subset dem file
    GTOPO30_dem = "gt30w060n90.tif"
    ulx = -56  #degree
    uly = 72
    lrx =-42
    lry = 67
    GTOPO30_sub = io_function.get_name_by_adding_tail(GTOPO30_dem,'jako')
    RSImageProcess.subset_image_projwin(GTOPO30_sub,GTOPO30_dem,ulx,uly,lrx,lry)

    #transform projection
    x_res = 30
    y_res = 30
    srs_UTM_prj4 = '\'+proj=utm +zone=22 +datum=WGS84 +units=m +no_defs\' '
    GTOPO30_utm = io_function.get_name_by_adding_tail(GTOPO30_sub,'utm22')
    if os.path.isfile(GTOPO30_utm) is False:
        if RSImageProcess.transforms_raster_srs(GTOPO30_sub,srs_UTM_prj4,GTOPO30_utm,x_res,y_res) is False:
            return False

    return True

def prepare_gimpdem_for_Jakobshavn(workdir):
    nodata = parameters.get_nodata_value()
    #mosaics gimdem files
    os.chdir(workdir)
    gimpdem_file = ['gimpdem1_2.tif','gimpdem2_2.tif']
    gimpdem_output = 'dem_gimp_jako.tif'
    if os.path.isfile(gimpdem_output) is False:
        if RSImageProcess.mosaics_images(gimpdem_file,gimpdem_output) is False:
            return False

    geoid_file = 'geoid_hegith_jako.tif'

    #convert srs
    img_temp = RSImageclass()
    if not img_temp.open(gimpdem_output):
        return False
    x_res = img_temp.GetXresolution()
    y_res = img_temp.GetYresolution()
    srs_UTM_prj4 = '\'+proj=utm +zone=22 +datum=WGS84 +units=m +no_defs\' '
    gimpdem_utm = io_function.get_name_by_adding_tail(gimpdem_output,'utm22')
    if os.path.isfile(gimpdem_utm) is False:
        if RSImageProcess.transforms_raster_srs(gimpdem_output,srs_UTM_prj4,gimpdem_utm,abs(x_res),abs(y_res)) is False:
            return False

    # print img_temp.GetGDALDataType(),type(img_temp.GetGDALDataType())
    # print img_temp.GetProjection(),type(img_temp.GetProjection())
    # print img_temp.GetGeoTransform(),type(img_temp.GetGeoTransform())

    #get geoid_height
    # srs_longlat_wkt = "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.01745329251994328]]"
    # srs_longlat_prj4 = '\'+proj=longlat +datum=WGS84 +no_defs\' '
    # image = RSImageclass(syslog)
    # if not image.open(gimpdem_utm):
    #     return False
    #
    # img_pro = RSImgProclass(syslog)
    # dem_data = img_pro.Read_Image_band_data_to_numpy_array_all_pixel(1,gimpdem_utm)
    # if dem_data is False:
    #     return False
    #
    # # geoid_height = geoid_height + -9999
    # geoid_utm_file = basic.get_name_by_adding_tail(geoid_file,'tran',syslog)
    # if RSImageProcess.transforms_raster_srs_to_base_image(geoid_file,gimpdem_utm,geoid_utm_file,\
    #                                                       x_res,y_res,syslog) is False:
    #     return False
    # geoid_height = img_pro.Read_Image_band_data_to_numpy_array_all_pixel(1,geoid_utm_file)
    # if geoid_height is False:
    #     return False
    #
    # #get ellipsoidal height
    # Image_array = dem_data + geoid_height
    # gimpdem_utm_elli = basic.get_name_by_adding_tail(gimpdem_utm,'elli',syslog)
    # RSImageProcess.save_numpy_2d_array_to_image_tif(gimpdem_utm_elli,Image_array,\
    #     image.GetGDALDataType(),image.GetGeoTransform(),image.GetProjection(),nodata)

    # image = None
    # img_pro = None
    return True

def calculate_terrain_offset(output,dem_file,image_file,exec_dir,bkeepmidfile):
    if io_function.is_file_exist(image_file) is False or io_function.is_file_exist(dem_file,) is False:
        return False
    exefile = os.path.join(exec_dir,'geometry_pro')
    nodata = parameters.get_nodata_value()

    (centre_lat, centre_lon) = RSImage.get_image_latlon_centre(image_file)
    if centre_lat is False or centre_lon is False:
        return False

    image_obj = RSImageclass()
    if image_obj.open(image_file) is False:
        return False
    dem_obj = RSImageclass()
    if dem_obj.open(dem_file) is False:
        return False

    x_res = image_obj.GetXresolution()
    y_res = image_obj.GetYresolution()
    x_res_dem = dem_obj.GetXresolution()
    y_res_dem = dem_obj.GetYresolution()

    image_prj = image_obj.GetProjection()
    dem_prj = dem_obj.GetProjection()

    #check projection and resolution, and convert it if need
    #use orthometricH_file as base image
    dem_convertedfile = io_function.get_name_by_adding_tail(dem_file,'tran')
    if x_res != x_res_dem or y_res != y_res_dem or image_prj!=dem_prj:
        if os.path.isfile(dem_convertedfile) is False:
            if map_projection.transforms_raster_srs(dem_file,image_prj,dem_convertedfile,abs(x_res),abs(y_res)) is False:
                return False
    if os.path.isfile(dem_convertedfile):
        dem_file = dem_convertedfile

    #sub  dem file
    (ulx,uly,lrx,lry) = RSImage.get_image_proj_extent(image_file)
    if ulx is False:
        return False
    tail = os.path.splitext(os.path.basename(image_file))[0]
    dem_file_sub = io_function.get_name_by_adding_tail(dem_file,tail)
    if os.path.isfile(dem_file_sub) is False:
        if RSImageProcess.subset_image_projwin(dem_file_sub,dem_file,ulx,uly,lrx,lry) is False:
            return False

    #calculateing terrain contains a lot of I/O operations, the parallel computing will slow down it
    nblockwidth = 8000
    nblcckheight = 8000
    njobs = 1

    logfile = 'cal_terrain_offset_log.txt'

    CommandString = exefile \
                    + ' -i ' + image_file + ' -d ' + dem_file_sub \
                    + ' -o '  + output  + ' -n ' + str(nodata)\
                    + ' -w ' + str(nblockwidth) + ' -h ' + str(nblcckheight) + ' -j ' +str(njobs) \
                    + ' --centre_lat=' + str(centre_lat)  \
                    + ' --logfile=' + logfile

    basic.outputlogMessage(CommandString)
    (status, result) = commands.getstatusoutput(CommandString)
    basic.outputlogMessage(result)

    if bkeepmidfile is False:
        # if os.path.isfile(dem_convertedfile):
        #     io_function.delete_file_or_dir(dem_convertedfile)
        if os.path.isfile(dem_file_sub):
            io_function.delete_file_or_dir(dem_file_sub)

    if os.path.isfile(output):
        if os.path.getsize(output) > 0:
            return output
        else:
            basic.outputlogMessage('error: the size of file %s is 0'%os.path.basename(output))
            return False
    else:
        return False

def test_get_geoid_height():
    LatitudeDeg = 72
    LatitudeMin = 0
    LatitudeSec = 0
    LongitudeDeg = -57
    LongitudeMin = 0
    LongitudeSec = 0
    nodata = 0

    value = get_geoid_height(LatitudeDeg,LatitudeMin,LatitudeSec,LongitudeDeg,LongitudeMin,LongitudeSec,nodata)
    if value is False:
        return False
    basic.outputlogMessage(str(value))
    return True

def help():
    print "what_to_do: 1 is prepare_gimpdem_for_Jakobshavn"
    print "what_to_do: 2 is get_range_geoid_height"
    print "what_to_do: 3 is get_geoimage_range_geoid_height"
    print "what_to_do: 4 is convert_orthometricH_to_elliopsoidalH"
    print "what_to_do: 5 is calculate_terrain_offset"
    print "what_to_do: 6 is prepare_GTOPO30_for_Jakobshavn"

def main(options, args):
    # syslog = LogMessage()
    # length = len(sys.argv)

    # test_get_geoid_height(syslog)
    # sys.exit(1)
    #
    # if length >=3 :
    #     work_dir = sys.argv[1]
    #     what_to_do = sys.argv[2]
    # else:
    #     print 'Input error, Try to do like this:'
    #     print 'DemConvert.py work_dir what_to_do'
    #     help()
    #     sys.exit(1)

    length = len(args)
    want_to_do = options.what_to_do# (what_to_do)#options.what_to_do
    work_dir = args[0]
    basic.setlogfile('dem_prepare_log.txt')
    parameters.set_saved_parafile_path(options.para_file)
    if want_to_do==1:
        if prepare_gimpdem_for_Jakobshavn(work_dir):
            basic.outputlogMessage('process sucess')
        else:
            basic.outputlogMessage('process failed')
    elif want_to_do==2:
        outputfile = options.output
        up = 72
        down = 69
        left = -57
        right = -40
        get_range_geoid_height(outputfile,up,down,left,right)
    elif want_to_do==3:
        if length == 2 :
            outputfile = options.output
            ref_image = args[1]
            if get_geoimage_range_geoid_height(outputfile,ref_image) != False:
                return True
        print 'Input error, Try to do like this: '
        print 'DemConvert.py  -a 3 -o outputfile work_dir ref_image'
        sys.exit(1)

    elif want_to_do == 4:
        if length ==3 :
            orthometric_demfile = args[1]
            geoid_demfile = args[2]
            outputfile = io_function.get_name_by_adding_tail(orthometric_demfile,"ellip")
            if convert_orthometricH_to_elliopsoidalH(outputfile,orthometric_demfile,geoid_demfile) != False:
                return True
        print 'Input error, Try to do like this: '
        print 'DemConvert.py -a 4  work_dir  orthometric_demfile geoid_demfile'
        sys.exit(1)

    elif want_to_do == 5:
        if length ==3 :
            outputfile = options.output
            dem_file = args[1]
            image_file = args[2]
            exec_dir = os.path.expanduser('~') +'/bin/'
            if calculate_terrain_offset(outputfile,dem_file,image_file,exec_dir) != False:
                return True
        print 'Input error, Try to do like this: '
        print 'DemConvert.py  -a 5 -o output work_dir dem_file image_file'
        sys.exit(1)

    elif want_to_do == 6:
        if length !=3 :
            print 'Input error, Try to do like this: '
            print 'DemConvert.py work_dir what_to_do'
            sys.exit(1)
        print prepare_GTOPO30_for_Jakobshavn(work_dir)

    else:
        basic.outputlogMessage('nothing to do')

    #test
    # print get_geoid_height(22,31,32,114,15,16,-999999,syslog)

    return True

if __name__=='__main__':

    usage = "usage: %prog [options] work_dir and other input"
    parser = OptionParser(usage=usage,version="1.0 2016-4-26")
    parser.add_option("-a", "--action",type="int",
                      action="store", dest="what_to_do",
                      help="the flag stands for what to do:"
                      "1 is prepare_gimpdem_for_Jakobshavn;"
                      "2 is get_range_geoid_height; "
                      "3 is get_geoimage_range_geoid_height; "
                      "4 is convert_orthometricH_to_elliopsoidalH; "
                      "5 is calculate_terrain_offset; "
                      "6 is prepare_GTOPO30_for_Jakobshavn; ")

    parser.add_option("-p", "--para",
                      action="store", dest="para_file",
                      help="the parameters file")

    parser.add_option('-o',"--output",action='store',dest="output",
                      help="the output file name, need when you set action = 2,3,5")
    # parser.

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2 or len(args)<1 or options.what_to_do==None or options.para_file==None:
        parser.print_help()
        sys.exit(2)


    main(options, args)

    # main()


