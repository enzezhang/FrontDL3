#!/usr/bin/env python
# Filename: geometryProcess.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 24 June, 2016
"""

import os,sys,tiepoints,re
import struct
import RSImageProcess

from RSImage import RSImageclass
import parameters
import basic,io_function

# from PIL import Image, ImageDraw
# import aggdraw,test_aggdraw

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

__author__ = 'huanglingcao'

def is_file_exist(file):
    if not os.path.isfile(file):
        basic.outputlogMessage('coregistration failed, can not find the file: ' + os.path.abspath(file))
        return False
    return True

def check_format(rsimage,syslog):
    result = rsimage.GetGetDriverLongName()
    if not result is False:
        if result.upper()!='GEOTIFF':
            syslog.outputlogMessage('Input format is not correct, GEOTIFF is the require')
            return False
        else:
            return True
    else:
        return False

def setorthoParameters(parafile,parameter, value):
    if not isinstance(value, str):
        value = str(value)
    inputfile = open(parafile, 'r')
    list_of_all_the_lines = inputfile.readlines( )
    for i in range(0,len(list_of_all_the_lines)):
        line = list_of_all_the_lines[i]
        if line[0:1] == '#' or len(line) < 2:
            continue
        lineStrs = line.split('=')
        lineStrs = lineStrs[0].strip()     #remove ' ' from left and right
        if lineStrs == parameter:
            # lineStrs[1] = value
            list_of_all_the_lines[i] = lineStrs + '= ' +value +'\n'
            break

    inputfile.close()
    #test
    # commands.getstatusoutput('cp '+ parafile + ' ' + parafile+'.bak')

    outputfile = open(parafile, 'w')
    for linestr in list_of_all_the_lines:
        outputfile.writelines(linestr)
    outputfile.close()

    return True

#setparameters for ortho
def setparameters(parafile_inp,parafile_ini,baseimage,warpimage,syslog):
    basefile = baseimage.imgpath
    warpfile = warpimage.imgpath
#set parafile_inp
#base image
    setorthoParameters(parafile_inp, 'BASE_LANDSAT', basefile)
    setorthoParameters(parafile_inp, 'UTM_ZONE', baseimage.GetUTMZone())
    setorthoParameters(parafile_inp, 'BASE_SATELLITE', baseimage.Getsatellite())
#warp Image
    Outbandname = warpfile.split('.')[0]+'_coreg'
    setorthoParameters(parafile_inp, 'WARP_SATELLITE', warpimage.Getsatellite())
    setorthoParameters(parafile_inp, 'WARP_ORIENTATION_ANGLE', 0)
    setorthoParameters(parafile_inp, 'WARP_NBANDS', 1)
    setorthoParameters(parafile_inp, 'WARP_LANDSAT_BAND', warpfile)
    setorthoParameters(parafile_inp, 'WARP_BASE_MATCH_BAND', warpfile)


    setorthoParameters(parafile_inp, 'OUT_PIXEL_SIZE', baseimage.GetXresolution())
    setorthoParameters(parafile_inp, 'RESAMPLE_METHOD', 'CC')
    setorthoParameters(parafile_inp, 'OUT_EXTENT', 'BASE')
    setorthoParameters(parafile_inp, 'OUT_LANDSAT_BAND', Outbandname)
    setorthoParameters(parafile_inp, 'OUT_BASE_MATCH_BAND', Outbandname)
    setorthoParameters(parafile_inp, 'OUT_BASE_POLY_ORDER', 1)
    setorthoParameters(parafile_inp, 'CP_PARAMETERS_FILE', parafile_ini)
#set parafile_ini
    setorthoParameters(parafile_ini, 'PRELIMINARY_REGISTRATION', 0)
    setorthoParameters(parafile_ini, 'COARSE_SCALE', 10)
    setorthoParameters(parafile_ini, 'COARSE_MAX_SHIFT', 150)
    setorthoParameters(parafile_ini, 'COARSE_CP_SEED_WIN', 5)

    setorthoParameters(parafile_ini, 'CHIP_SIZE', 11)
    setorthoParameters(parafile_ini, 'CP_SEED_WIN', 10)
    setorthoParameters(parafile_ini, 'MAX_SHIFT', 5)
    setorthoParameters(parafile_ini, 'MAX_NUM_HIGH_CORR', 3)
    setorthoParameters(parafile_ini, 'ACCEPTABLE_CORR', 0.8)
    setorthoParameters(parafile_ini, 'MIN_ACCEPTABLE_NCP', 8)
    setorthoParameters(parafile_ini, 'MAX_AVE_ERROR', 0.5)
    setorthoParameters(parafile_ini, 'MAX_NUM_ITER', 1)
    setorthoParameters(parafile_ini, 'MAX_ACCEPTABLE_RMSE', 0.75)

    syslog.outputlogMessage('Set inputing and matching parameters completed')

    return Outbandname


##coregistration by ortho
def coregistration(exefile,parafile_inp,parafile_ini,basefile, warpfile):
#check input
    if not is_file_exist(exefile):
        return False
    if (not is_file_exist(parafile_inp)) or (not is_file_exist(parafile_ini)):
        return False
    if (not is_file_exist(basefile)) or (not is_file_exist(warpfile)):
        return False

    baseimage = RSImageclass()
    warpimage = RSImageclass()
    if not baseimage.open(basefile):
        return False
    if not warpimage.open(warpfile):
        return False

    if not check_format(baseimage):
        return False
    if not check_format(warpimage):
        return False

    Outbandname = setparameters(parafile_inp,parafile_ini,baseimage,warpimage)

    CommandString = exefile + ' -r '+ parafile_inp
    basic.outputlogMessage(CommandString)
    (status, result) = commands.getstatusoutput(CommandString)
    basic.outputlogMessage(result)
    if not os.path.isfile(Outbandname):
        return False

#convert the result file to tif
    Outputtiff = Outbandname.split('.')[0]+'_tran.tif'
    CommandString = 'gdal_translate -of GTiff '+ Outbandname + ' '+Outputtiff
    basic.outputlogMessage(CommandString)
    (status, result) = commands.getstatusoutput(CommandString)
    basic.outputlogMessage(result)
    if not os.path.isfile(Outputtiff):
        return False

    return True


def test_ortho_coregistration():

    usrhome = os.path.expanduser('~')  #like /home/hlc, other people need to set this to '/home/hlc'

    # setorthoParameters('verification_example.inp','WARP_LANDSAT_BAND', 'test.tif')
    exefile = usrhome + '/bin/ortho'
    # coregistration(exefile,'landsatband8_band8_coreg.inp','landsatband8_band8_coreg.ini',\
    #                'LE70080112000083KIS00_B8_sub.TIF', 'LE70080112000115EDC00_B8_sub.TIF',syslog)

    coregistration(exefile,'band8_band8_coreg.inp','landsatband8_band8_coreg.ini',\
                   'LE70080112000083KIS00_B8_sub.TIF', 'LE70080112000115EDC00_B8_sub.TIF')

    return True

def setGCPsfromptsFile(imagefile,projection,GeoTransform, ptsfile):
    if not is_file_exist(imagefile):
        return False
    image = RSImageclass()
    if not image.open(imagefile):
        return False
    ngcpcount = image.ds.GetGCPCount()
    if ngcpcount > 0:
        basic.outputlogMessage('warning: The file already have GCP,GCP count is ' + str(ngcpcount))

    allgcps = []
    inputfile_object = open(ptsfile, 'r')
    all_points = inputfile_object.readlines( )
    for linestr in all_points:
        if linestr[0:1] == '#'  or linestr[0:1] == ';' or len(linestr) < 2:
            continue
        if len(allgcps) >= 10000:
            basic.outputlogMessage('warning: the count of gcps already greater than 10000, and ignore the others to make geotiff work correctly')
            continue
        tiepointXY = linestr.split()
        base_x = float(tiepointXY[0])
        base_y = float(tiepointXY[1])
        Xp = GeoTransform[0] +base_x*GeoTransform[1]+base_y*GeoTransform[2]
        Yp = GeoTransform[3] + base_x*GeoTransform[4] + base_y*GeoTransform[5]

        warp_x = float(tiepointXY[2])
        warp_y = float(tiepointXY[3])
        info =  'GCPbysiftgpu_%d' % len(allgcps)
        id = str(len(allgcps))
        gcp1 = gdal.GCP(Xp,Yp,0,warp_x,warp_y,info,id)
        allgcps.append(gcp1)
    inputfile_object.close()



    Outputtiff = imagefile.split('.')[0]+'_new.tif'
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE)  and metadata[gdal.DCAP_CREATE] == 'YES':
        basic.outputlogMessage( 'Driver %s supports Create() method.' % format)
    else:
        basic.outputlogMessage( 'Driver %s not supports Create() method.' % format)
        return False
    # if metadata.has_key(gdal.DCAP_CREATECOPY) and metadata[gdal.DCAP_CREATECOPY] == 'YES':
    #     syslog.outputlogMessage('Driver %s supports CreateCopy() method.' % format)

    # dst_ds = driver.CreateCopy(Outputtiff, dataset, 0)
    datatype = image.GetGDALDataType()
    dst_ds = driver.Create(Outputtiff, image.GetWidth(), image.GetHeight(), image.GetBandCount(),datatype)
    for bandindex in range(0,image.GetBandCount()):
        bandobject = image.Getband(bandindex+1)
        banddata = bandobject.ReadRaster(0,0,image.GetWidth(), image.GetHeight(),image.GetWidth(), image.GetHeight(),datatype)
        #byte
        # if banddata is 1:
        #     bandarray = struct.unpack('B'*image.GetWidth()*image.GetHeight(), banddata)
        dst_ds.GetRasterBand(bandindex+1).WriteRaster(0,0,image.GetWidth(), image.GetHeight(),banddata,image.GetWidth(), image.GetHeight(),datatype)

    dst_ds.SetGCPs(allgcps,projection)

    # if I have set the GCPs, should not do this again, or SetGCPs will be undo
    # dst_ds.SetGeoTransform(image.GetGeoTransform())
    # dst_ds.SetProjection(image.GetProjection())

    if not os.path.isfile(Outputtiff):
        basic.outputlogMessage('result file not exist, the operation of create set gcp failed')
        return False
    dst_ds = None
    image = None

    return Outputtiff

def output_tie_points_vector_on_base_image(drawed_image,tiepoint_rms_file,outputfile):
    if not os.path.isfile(drawed_image):
        basic.outputlogMessage('file not exist: '+os.path.abspath(drawed_image))
        return False
    if not os.path.isfile(tiepoint_rms_file):
        basic.outputlogMessage('file not exist: '+os.path.abspath(tiepoint_rms_file))
        return False

    #read points (x,y) and rms
    draw_scale = parameters.get_draw_tie_points_rms_vector_scale()
    if draw_scale is False:
        return False
    x0 = []
    y0 = []
    x1 = []
    y1 = []
    tiepoint_rms_file_object = open(tiepoint_rms_file,'r')
    lines_str = tiepoint_rms_file_object.readlines()
    if (len(lines_str)<5):
        basic.outputlogMessage('error, intput file contains lines less than 5')
        return False
    for i in range(4,len(lines_str)):
        digits = lines_str[i].split();
        tempx=0
        tempy=0
        dx =0
        dy =0
        try:
            tempx = float(digits[0])
            tempy = float(digits[1])
            dx = float(digits[6])*draw_scale #(float(digits[2]) - tempx )*draw_scale  #float(digits[6])*draw_scale
            dy = float(digits[7])*draw_scale #(float(digits[3]) - tempy)*draw_scale #float(digits[7])*draw_scale
        except ValueError:
            basic.outputlogMessage(str(ValueError))
        x0.append(tempx)
        y0.append(tempy)
        x1.append(tempx+dx)
        y1.append(tempy+dy)
    tiepoint_rms_file_object.close()

    drawed_image_gray = io_function.get_name_by_adding_tail(drawed_image,'gray')
    drawed_image_gray = RSImageProcess.convert_image_to_gray_auto(drawed_image_gray,drawed_image)
    im = Image.open(drawed_image_gray).convert('RGB')  #needing convert to RGB, or can not draw color line and text
    draw_content = aggdraw.Draw(im)
    # draw_content2 = ImageDraw.Draw(im)
    for k in range(0,len(x0)):
        test_aggdraw.line(draw_content,(x0[k], y0[k], x1[k], y1[k]),color='red',width=1,arrow='last',arrowshape=(4,5,3))

    #draw legend
    x0 = 100
    y0 = 100
    x1 = 0.5*draw_scale + x0
    y1 = y0
    test_aggdraw.line(draw_content,(x0, y0, x1, y1),color='red',width=1,arrow='last',arrowshape=(8,10,3))
    test_aggdraw.draw_text(draw_content,(100,80),'0.5 pixel')
    # draw_content2.text((3000,90),'1000 m/year')
    # draw_content2.flush()
    # del draw_content2

    draw_content.flush()
    im.save(outputfile)


    return True

#coregistration
def coregistration_siftGPU(basefile, warpfile,bkeepmidfile,xml_obj):
    tiepointfile = '0_1_after.pts'
    if os.path.isfile(tiepointfile):
        basic.outputlogMessage('warning:tie points already exist in dir, skip get_tie_points_by_ZY3ImageMatch')
    else:
        tiepointfile = tiepoints.get_tie_points_by_ZY3ImageMatch(basefile,warpfile,bkeepmidfile)

    if tiepointfile is False:
        basic.outputlogMessage('Get tie points by ZY3ImageMatch failed')
        return False

    xml_obj.add_coregistration_info('tie_points_file', tiepointfile)
    #draw tie points rms vector on base image
    result_rms_files = '0_1_fs.txt'
    tiepoint_vector_ = 'tiepoints_vector.png'
    output_tie_points_vector_on_base_image(basefile,result_rms_files,tiepoint_vector_)
    xml_obj.add_coregistration_info('tie_points_drawed_image', os.path.abspath(tiepoint_vector_))

    #check the tie points
    try:
        rms_files_obj = open(result_rms_files,'r')
        rms_lines = rms_files_obj.readlines()
        if len(rms_lines)<2:
            basic.outputlogMessage("%s do not contain tie points information"%os.path.abspath(result_rms_files))
            return False
        required_point_count = parameters.get_required_minimum_tiepoint_number()
        acceptable_rms = parameters.get_acceptable_maximum_RMS()
        xml_obj.add_coregistration_info('required_tie_point_count', str(required_point_count))
        xml_obj.add_coregistration_info('acceptable_rms', str(acceptable_rms))
        try:
            digit_str = re.findall('\d+',rms_lines[0])
            tiepoints_count = int(digit_str[0])
            xml_obj.add_coregistration_info('tie_points_count', str(tiepoints_count))
            if tiepoints_count < required_point_count:
                basic.outputlogMessage("ERROR: tiepoints count(%d) is less than required one(%d)"%(tiepoints_count,required_point_count))
                return False
            digit_str = re.findall('\d+\.?\d*',rms_lines[1])
            totalrms_value = float(digit_str[2])
            xml_obj.add_coregistration_info('total_rms_value', str(totalrms_value))
            if totalrms_value > acceptable_rms:
                basic.outputlogMessage("ERROR:Total RMS(%f) exceeds the acceptable one(%f)"%(totalrms_value,acceptable_rms))
                return False
        except ValueError:
            return basic.outputlogMessage(str(ValueError))
            return False
        rms_files_obj.close()
    except IOError:
        syslog.outputlogMessage(str(IOError))
        return False


    baseimg = RSImageclass()
    if not baseimg.open(basefile):
        return False
    proj = baseimg.GetProjection()
    geotransform = baseimg.GetGeoTransform()
    xres = baseimg.GetXresolution()
    yres = baseimg.GetYresolution()

    try:
        Outputtiff = setGCPsfromptsFile(warpfile,proj,geotransform,tiepointfile)
    except RuntimeError as e:
        basic.outputlogMessage('setGCPsfromptsFile failed: ')
        basic.outputlogMessage(str(e))
        return False
    if Outputtiff is False:
        return False
    else:
        basic.outputlogMessage('setGCPsfromptsFile completed, Out file: '+Outputtiff)

    # if not bkeepmidfile:
    #     os.remove(warpfile)

    xml_obj.add_coregistration_info('setted_gcps_file', Outputtiff )

    #warp image
    warpresultfile = Outputtiff.split('.')[0]+'_warp.tif'
    #-order 1  -tps
    #-tr xres yres: set output file resolution (in target georeferenced units)
    # set resolution as the same as base image is important
    order_number = parameters.get_gdalwarp_polynomial_order()
    xml_obj.add_coregistration_info('warp_polynomial_order_number', str(order_number))
    if order_number is False:
        return False
    CommandString = 'gdalwarp '+' -order ' + str(order_number) +' -r bilinear -tr '+str(xres)+' ' +str(yres) + ' '+ Outputtiff + ' '+warpresultfile
    basic.outputlogMessage(CommandString)
    (status, result) = commands.getstatusoutput(CommandString)
    basic.outputlogMessage(result)
    if not os.path.isfile(warpresultfile):
        return False

    if not bkeepmidfile:
        os.remove(Outputtiff)

    return warpresultfile

def test_gdalwarp():
    filedir = '/Users/huanglingcao/Data/landsat_offset_test/coregistration_test/L7_B8_test_2/'
    os.chdir(filedir)
    file1 = 'LE70080111999288EDC00_B8.TIF'
    file2 = 'LE70080112000083KIS00_B8.TIF'

    warpresultfile = coregistration_siftGPU(file1,file2,True)
    if warpresultfile is False:
        return False


    return True

if __name__=='__main__':
    # test_ortho_coregistration()
    # test_gdalwarp(syslog)
    length = len(sys.argv)
    if length == 3 :
        basefile = sys.argv[1]
        warpfile = sys.argv[2]
    else:
        print (' Input error, Try to do like this:')
        print ('geometryProcess.py basefile warpfile ')
        sys.exit(1)

    bkeepmidfile = True
    parameters.set_saved_parafile_path('para.ini')

    coregistration_siftGPU(basefile, warpfile,bkeepmidfile)
