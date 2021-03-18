#!/usr/bin/env python
# Filename: tiepoints.py
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 24 June, 2016
"""

import os,time,random,shutil,parameters,ntpath,basic,subprocess
# from basic import LogMessage
import basic,io_function

def reduce_tie_points_by_range(inputfile, outputfile,maxXrange,maxYrange,syslog):
    inputfile_object = open(inputfile, 'r')
    all_points = inputfile_object.readlines( )

    save_lines = []

    for linestr in all_points:
        if linestr[0:1] == '#'  or linestr[0:1] == ';' or len(linestr) < 2:
            save_lines.append(linestr)
            continue
        tiepointXY = linestr.split()
        base_x = float(tiepointXY[0])
        base_y = float(tiepointXY[1])
        warp_x = float(tiepointXY[2])
        warp_y = float(tiepointXY[3])

        if abs(base_x-warp_x)<maxXrange and abs(base_y-warp_y)<maxYrange:
            save_lines.append(linestr)
    inputfile_object.close()


    outputfile_object = open(outputfile, 'w')
    for linestr in save_lines:
        outputfile_object.writelines(linestr)
    outputfile_object.close()

    return True



def get_tie_points_by_ZY3ImageMatch(basefile,warpfile,bkeepmidfile):
    workdir = os.getcwd()
    if not os.path.isfile(basefile):
        basic.outputlogMessage('not exist,file path: %s'%basefile)
        return False
    if not os.path.isfile(warpfile):
        basic.outputlogMessage('not exist ,file path: %s'%warpfile)
        return False

    taskID = time.strftime('%Y%m%d_%H%M%S', time.localtime())+'_' + str(int(random.uniform(100,999)))
    taskfile = taskID+'+filelist.txt'
    file_object = open(taskfile,'w')
    file_object.writelines(str(2)+'\n')

    tempstr = os.path.abspath(basefile) + '\n'
    file_object.writelines(tempstr)
    tempstr = os.path.abspath(warpfile) +'\n'
    file_object.writelines(tempstr)
    file_object.close()

    io_function.mkdir(taskID)
    try:
        shutil.move(taskfile,taskID+'/.')
    except:
        basic.outputlogMessage("mv taskfile failed" )
        basic.outputlogMessage('taskfile: '+ taskfile)
        basic.outputlogMessage('taskid: ' + taskID)
        return False

    taskfile = os.path.join(workdir,taskID,taskfile)
    resultdir = os.path.join(workdir,taskID)
    resultpath = os.path.join(resultdir,'results.txt')

    exe_dir = parameters.get_exec_dir()
    if exe_dir is False:
        return False
    exepath = os.path.join(exe_dir,'ImageMatchsiftGPU')
    CommandString = exepath + ' ' + taskfile + ' ' + resultpath + ' '+ str(2)
    basic.outputlogMessage(CommandString)

    (status, result) = commands.getstatusoutput(CommandString)
    #syslog.outputlogMessage(result)

    if os.path.isfile('system.log'):
        io_function.copyfiletodir('system.log',taskID)
        shutil.move('system.log','matchbysiftgpu_systemlog.txt')

    #waiting and trying to get the tie points files
    result_tiepointfile = os.path.join(workdir,taskID,'0_1_after.pts')
    result_rms_files = os.path.join(workdir,taskID,'0_1_fs.txt')

    if os.path.isfile(result_tiepointfile):
        io_function.copyfiletodir(result_tiepointfile,'.')
        io_function.copyfiletodir(result_rms_files,'.')

    if bkeepmidfile is False:
        io_function.delete_file_or_dir(resultdir)

    tiepointfile = '0_1_after.pts'
    if os.path.isfile(tiepointfile):
        return os.path.abspath(tiepointfile)
    else:
        return False


def get_tie_points_by_ZY3ImageMatch_win(basefile,warpfile,syslog):
    #workdir(need to confirm this dir is exist first)
    workdir = parameters.get_share_floder(syslog) # '/Volumes/Dtemp/'
    workdir_win = parameters.get_window_work_dir(syslog) #'D:\\Dtemp\\'
     #copy files to my window's pc
    if not io_function.copyfiletodir(basefile,workdir):
        return False
    if not io_function.copyfiletodir(warpfile,workdir):
        return False

    taskID = time.strftime('%Y%m%d_%H%M%S', time.localtime())+'_' + str(int(random.uniform(100,999)))
    taskfile = taskID+'+filelist.txt'
    file_object = open(taskfile,'w')
    file_object.writelines(str(2)+'\n')

    # file path for window
    tempstr = ntpath.join(workdir_win,os.path.split(basefile)[1]) +'\n'
    file_object.writelines(tempstr)
    tempstr = ntpath.join(workdir_win,os.path.split(warpfile)[1]) +'\n'
    file_object.writelines(tempstr)
    file_object.close()

    if not io_function.copyfiletodir(taskfile,workdir):
        return False

    #waiting and trying to get the tie points files
    result_tiepointfile = os.path.join(workdir,taskID,'0_1_after.pts')
    result_logfile = os.path.join(workdir,taskID,'system.log')
    timeout = parameters.get_tie_points_time_out(syslog)
    addtime = 0
    while True:
        if os.path.isfile(result_tiepointfile) and os.path.isfile(result_logfile):
            io_function.copyfiletodir(result_tiepointfile,'.')
            time.sleep(5)
            io_function.copyfiletodir(result_logfile,'.') # this file always exist, but it failed copy, dont know why
            if os.path.isfile('system.log'):
                shutil.move('system.log','matchbysiftgpu_systemlog.txt')
            break
        else:
            if addtime > timeout:
                syslog.outputlogMessage('get %s and %s time out',result_tiepointfile,result_logfile)
                break
            syslog.outputlogMessage('wait time %d'%addtime)
            addtime += 5
            time.sleep(5)

    tiepointfile = '0_1_after.pts'
    if os.path.isfile(tiepointfile):
        return os.path.abspath(tiepointfile)
    else:
        return False


def test_reduce_tie_points(syslog):

    # inputfile = '/Users/huanglingcao/Data/landsat_offset_test/coregistration_test/L7_B8_test_2/test1/0_1_after.pts'
    inputfile = '/Users/huanglingcao/Data/landsat_offset_test/coregistration_test/L7_B8_test_2/test1/0_1_before.pts'
    outputfile = os.path.splitext(inputfile)[0] + '_p'+os.path.splitext(inputfile)[1]
    reduce_tie_points_by_range(inputfile,outputfile,10,10,syslog)
    return True

def test_get_tie_points_by_ZY3ImageMatch_win(syslog):
    filedir = '/Users/huanglingcao/Data/landsat_offset_test/coregistration_test/L7_B8_test_2/'
    os.chdir(filedir)
    file1 = 'LE70080111999288EDC00_B8.TIF'
    file2 = 'LE70080112000083KIS00_B8.TIF'
    get_tie_points_by_ZY3ImageMatch_win(filedir+file1,filedir+file2,syslog)

    return True

def test_get_tie_points_by_ZY3ImageMatch():
    filedir = '/home/hlc/Data/landsat_offset_test/coregistration_test/L7_B8_test_2'
    os.chdir(filedir)
    exe_dir = parameters.get_exec_dir('para.ini')

    file1 = os.path.join(filedir,'LE70080111999288EDC00_B8.TIF')
    file2 = os.path.join(filedir,'LE70080112000083KIS00_B8.TIF')
    result = get_tie_points_by_ZY3ImageMatch(file1,file2)
    if not result is False:
        basic.outputlogMessage('get_tie_points_by_ZY3ImageMatch success,result path is:'+result)
    else:
        basic.outputlogMessage('get_tie_points_by_ZY3ImageMatch failed')


    return True


if __name__=='__main__':

    # test_reduce_tie_points(syslog)
    # test_get_tie_points_by_ZY3ImageMatch(syslog)
    test_get_tie_points_by_ZY3ImageMatch()