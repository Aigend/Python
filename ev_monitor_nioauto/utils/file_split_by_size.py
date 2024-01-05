# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : file_split_by_size.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/7 2:27 下午
# @Description :

import sys, os
from config.settings import BASE_DIR


def split(file_path, to_dir, file_size=10, file_name='new_data', suffix=".mp4"):
    """
    1M = 1024 Kb = 1024*1024 bate
    """
    chunk_size = file_size * 1024 * 1024
    if not os.path.exists(to_dir):  # check whether todir exists or not
        os.mkdir(to_dir)
    else:
        for file in os.listdir(to_dir):
            os.remove(os.path.join(to_dir, file))
    part_number = 0
    input_file = open(file_path, 'rb')  # open the fromfile
    split_files = {}
    while True:
        chunk = input_file.read(chunk_size)
        if not chunk:  # check the chunk is empty
            break
        part_number += 1
        new_file_path = os.path.join(to_dir, ('%s_%04d%s' % (file_name, part_number, suffix)))
        file_obj = open(new_file_path, 'wb')  # make partfile
        file_obj.write(chunk)  # write data into partfile
        file_obj.close()
        split_files["%04d" % part_number] = new_file_path
    return split_files


if __name__ == '__main__':
    # fromfile = input('File to be split?')
    # todir = input('Directory to store part files?')
    # chunksize = int(input('Chunksize to be split?'))
    # fromfile = "../data/file_upload_data/test_upload.mp4"
    # from_file = "/Users/qiangwei.zhang/workspace/ev_monitor_nioauto/data/file_upload_data/28Mvedio_file.mp4"
    from_file = "/tests/app_message_portal/file_upload/img/ET7_25M.jpg"
    to_dir = "../tests/app_message_portal/data"
    chunk_size = 9
    absfrom, absto = map(os.path.abspath, [from_file, to_dir])
    print('Splitting', absfrom, 'to', absto, 'by', chunk_size)
    try:
        split_files = split(from_file, to_dir, chunk_size, file_name="new_split_file", suffix=".jpg")

    except:
        print('Error during split:')
        print(sys.exc_info()[0], sys.exc_info()[1])
    else:
        print('split finished:', split_files, 'parts are in', absto)
