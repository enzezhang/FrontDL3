#!/usr/bin/env python
# Filename: io_function.py
"""
introduction: support I/O operation for normal files

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 04 May, 2016
"""

import os,shutil
import basic_src.basic as basic

def mkdir(path):
    """
    create a folder
    Args:
        path: the folder name

    Returns:True if successful, False otherwise.
    Notes:  if IOError occurs, it will exit the program
    """
    path = path.strip()
    path = path.rstrip("\\")
    isexists = os.path.exists(path)
    if not isexists:
        try:
            os.makedirs(path)
            basic.outputlogMessage(path + ' Create Success')
            return True
        except IOError:
            basic.outputlogMessage('creating %s failed'%path)
            assert False
    else:
        print(path + '  already exist')
        return False


def delete_file_or_dir(path):
    """
    remove a file or folder
    Args:
        path: the name of file or folder

    Returns: True if successful, False otherwise
    Notes: if IOError occurs or path not exist, it will exit the program
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            basic.outputlogMessage('%s not exist'%path)
            assert False
    except IOError:
        basic.outputlogMessage('remove file or dir failed : ' + str(IOError))
        assert False

    return True

def is_file_exist(file_path):
    """
    determine whether the file_path is a exist file
    Args:
        file_path: the file path

    Returns:True if file exist, False otherwise

    """
    if os.path.isfile(file_path):
        return True
    else:
        basic.outputlogMessage("File : %s not exist"%os.path.abspath(file_path))
        return False

def is_folder_exist(folder_path):
    """
    determine whether the folder_path is a exist folder
    :param folder_path: folder path
    :return:True if folder exist, False otherwise
    """
    if len(folder_path) < 1:
        basic.outputlogMessage('error: The input folder path is empty')
        return False
    if os.path.isdir(folder_path):
        return True
    else:
        basic.outputlogMessage("Folder : %s not exist"%os.path.abspath(folder_path))
        return False


def os_list_folder_dir(top_dir):
    if not os.path.isdir(top_dir):
        basic.outputlogMessage('the input string is not a dir, input string: %s'%top_dir)
        return False

    sub_folders = []
    for file in sorted(os.listdir(top_dir)):
        file_path = os.path.abspath(os.path.join(top_dir, file))
        if os.path.isfile(file_path):
            continue
        elif os.path.isdir(file_path):
            sub_folders.append(file_path)
    if len(sub_folders) < 1:
        basic.outputlogMessage('There is no sub folder in %s'%top_dir)
        return False
    return sub_folders

def os_list_folder_files(top_dir):
    if not os.path.isdir(top_dir):
        basic.outputlogMessage('the input string is not a dir, input string: %s'%top_dir)
        return False

    list_files = []
    for file in sorted(os.listdir(top_dir)):
        file_path = os.path.abspath(os.path.join(top_dir, file))
        if os.path.isfile(file_path):
            list_files.append(file_path)


    if len(list_files) < 1:
        basic.outputlogMessage('There is no file in %s',top_dir)
        return False
    return list_files

def get_file_list_by_ext(ext,folder,bsub_folder):
    """

    Args:
        ext: extension name of files want to find, can be string for a single extension or list for multi extension
        eg. '.tif'  or ['.tif','.TIF']
        folder:  This is the directory, which needs to be explored.
        bsub_folder: True for searching sub folder, False for searching current folder only

    Returns: a list with the files abspath ,eg. ['/user/data/1.tif','/user/data/2.tif']
    Notes: if input error, it will exit the program
    """

    extension = []
    if isinstance(ext, str):
        extension.append(ext)
    elif isinstance(ext, list):
        extension = ext
    else:
        basic.outputlogMessage('input extension type is not correct')
        assert False
    if os.path.isdir(folder) is False:
        basic.outputlogMessage('input error, %s is not a directory'%folder)
        assert False
    if isinstance(bsub_folder,bool) is False:
        basic.outputlogMessage('input error, bsub_folder must be a bool value')
        assert False
        # sys.exit(1)

    files = []
    sub_folders = []
    sub_folders.append(folder)

    while len(sub_folders) > 0:
        current_sear_dir = sub_folders[0]
        file_names = os.listdir(current_sear_dir)
        for str_file in file_names:
            if os.path.isdir(str_file):
                sub_folders.append(os.path.join(current_sear_dir,str_file))
                continue
            ext_name = os.path.splitext(str_file)[1]
            for temp in extension:
                if ext_name == temp:
                    files.append(os.path.abspath(os.path.join(current_sear_dir,str_file)))
                    break
        if bsub_folder is False:
            break
        sub_folders.pop(0)

    return files

def get_absolute_path(path):
    return os.path.abspath(path)

def get_name_by_adding_tail(basename,tail):
    """
    create a new file name by add a tail to a exist file name
    Args:
        basename: exist file name
        tail: the tail name

    Returns: a new name if successfull
    Notes: if input error, it will exit program

    """
    text = os.path.splitext(basename)
    if len(text)<2:
        basic.outputlogMessage('ERROR: incorrect input file name: %s'%basename)
        assert False
    return text[0]+'_'+tail+text[1]


def copy_file_to_dst(file_path, dst_name, overwrite=False):
    """
    copy file to a destination file
    Args:
        file_path: the copied file
        dst_name: destination file name

    Returns: True if successful or already exist, False otherwise.
    Notes:  if IOError occurs, it will exit the program
    """
    if os.path.isfile(dst_name) and overwrite is False:
        basic.outputlogMessage("%s already exist, skip copy file"%dst_name)
        return True

    if file_path==dst_name:
        basic.outputlogMessage('warning: shutil.SameFileError')
        return True

    try:
        shutil.copy(file_path,dst_name)
    # except shutil.SameFileError:
    #     basic.outputlogMessage('warning: shutil.SameFileError')
    #     pass
    except IOError:
        basic.outputlogMessage(str(IOError))
        basic.outputlogMessage('copy file failed: '+ file_path)
        assert False



    if not os.path.isfile(dst_name):
        basic.outputlogMessage('copy file failed')
        return False
    else:
        basic.outputlogMessage('copy file success: '+ file_path)
        return True


def move_file_to_dst(file_path, dst_name):
    """
    move file to a destination file
    Args:
        file_path: the moved file
        dst_name: destination file name

    Returns: True if successful or already exist, False otherwise.
    Notes:  if IOError occurs, it will exit the program

    """
    if os.path.isfile(dst_name):
        basic.outputlogMessage("%s already exist, skip move file"%dst_name)
        return True
    try:
        shutil.move(file_path,dst_name)
    except IOError:
        basic.outputlogMessage(str(IOError))
        basic.outputlogMessage('move file failed: '+ file_path)
        assert False

    if not os.path.isfile(dst_name):
        basic.outputlogMessage('move file failed')
        return False
    else:
        basic.outputlogMessage('move file success: '+ file_path)
        return True

def movefiletodir(file_path, dir_name):
    """
    move file to a destination folder
    Args:
        file_path: the moved file
        dir_name: destination folder name

    Returns: True if successful or already exist, False otherwise.
    Notes:  if IOError occurs, it will exit the program

    """
    dst_name =  os.path.join(dir_name,os.path.split(file_path)[1])
    if os.path.isfile(dst_name):
        basic.outputlogMessage("%s already exist, skip"%dst_name)
        return True
    try:
        shutil.move(file_path,dst_name)
    except IOError:
        basic.outputlogMessage(str(IOError))
        basic.outputlogMessage('move file failed: '+ file_path)
        assert False

    if not os.path.isfile(dst_name):
        basic.outputlogMessage('move file failed')
        return False
    else:
        basic.outputlogMessage('move file success: '+ file_path)
        return True

def copyfiletodir(file_path, dir_name):
    """
    copy file to a destination folder
    Args:
        file_path: the copied file
        dir_name: destination folder name

    Returns: True if successful or already exist, False otherwise.
    Notes:  if IOError occurs, it will exit the program

    """
    dst_name =  os.path.join(dir_name,os.path.split(file_path)[1])
    if os.path.isfile(dst_name):
        basic.outputlogMessage("%s already exist, skip"%dst_name)
        return True
    try:
        shutil.copyfile(file_path,dst_name)
    except IOError:
        basic.outputlogMessage(str(IOError))
        basic.outputlogMessage('copy file failed: '+ file_path)
        assert False

    if not os.path.isfile(dst_name):
        basic.outputlogMessage('copy file failed')
        return False
    else:
        basic.outputlogMessage('copy file success: '+ file_path)
        return True

def decompress_gz_file(file_path,work_dir,bkeepmidfile):
    """
    decompress a compressed file with gz extension
    Args:
        file_path:the path of gz file
        bkeepmidfile: indicate whether keep the middle file(eg *.tar file)

    Returns:the absolute path of a folder which contains the decompressed files

    """
    if os.path.isdir(work_dir) is False:
        basic.outputlogMessage('dir %s not exist'%os.path.abspath(work_dir))
        return False
    file_basename = os.path.basename(file_path).split('.')[0]
    # file_tar = os.path.join(os.path.abspath(work_dir), file_basename + ".tar")
    file_tar = os.path.join(os.path.dirname(file_path), file_basename + ".tar")


    # decompression file and keep it
    # CommandString = 'gzip -dk ' + landsatfile
    # change commond line like below, bucause gzip version on cry01 do not have the -k option  by hlc 2015.12.26
    # CommandString = 'gzip -dc ' + file_path + ' > ' + file_tar
    args_list = ['gzip','-dk',file_path]
    # (status, result) = basic.exec_command_string(CommandString)
    # if status != 0:
    #     basic.outputlogMessage(result)
    #     return False
    if os.path.isfile(file_tar):
        basic.outputlogMessage('%s already exist')
    else:
        basic.exec_command_args_list(args_list)

    # decompression file and remove it
    dst_folder = os.path.join(os.path.abspath(work_dir),file_basename)
    mkdir(dst_folder)
    # CommandString = 'tar -xvf  ' + file_tar + ' -C ' + dst_folder
    args_list = ['tar', '-xvf', file_tar,'-C',dst_folder]
    # (status, result) = basic.exec_command_string(CommandString)
    basic.exec_command_args_list(args_list)
    # if status != 0:
    #     basic.outputlogMessage(result)
    #     return False
    if bkeepmidfile is False:
        os.remove(file_tar)
    return dst_folder


def keep_only_used_files_in_list(output_list_file,old_image_list_txt,used_images_txt,syslog):
    if is_file_exist(old_image_list_txt) is False:
        return False
    if is_file_exist(used_images_txt) is False:
        return False

    output_list_obj = open(output_list_file,"w")

    image_list_txt_obj = open(old_image_list_txt,'r')
    image_list = image_list_txt_obj.readlines()
    if len(image_list)< 1:
        syslog.outputlogMessage('%s open failed or do not contains file paths'%os.path.abspath(old_image_list_txt))
        return False
    used_images_txt_obj = open(used_images_txt,'r')
    used_images = used_images_txt_obj.readlines()
    if len(used_images)<1:
        syslog.outputlogMessage('%s open failed or do not contains file paths'%os.path.abspath(used_images_txt))
        return False

    for image_file in image_list:
        file_id = os.path.basename(image_file).split('.')[0]
        for used_file in used_images:
            used_file = os.path.splitext(os.path.basename(used_file))[0]
            used_file = used_file.split('_')[0]
            if file_id == used_file:
                output_list_obj.writelines(image_file)
                break

    image_list_txt_obj.close()
    used_images_txt_obj.close()
    output_list_obj.close()


if __name__=='__main__':
    pass