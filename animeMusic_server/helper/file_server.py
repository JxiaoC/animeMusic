# -*- coding:utf-8 -*-
import os
import urllib
import time
import traceback
from .import realpath
from .import setting
from .import ftp
from .import scp
import aliyun.oss as oss
from ffmpy import FFmpeg


def upload_file_to_oss_and_ftp(file_path, name):
    print('uploadImgToOSSAndFtp, ', name)
    try:
        print('uploading to oss...')
        oss.upload_file(name, file_path)

        print('format mp3 file...')
        file_path_128 = file_path.replace('.mp3', '_128.mp3')
        get_mp3file(file_path, file_path_128)

        _128_name = name.replace('.mp3', '_128.mp3')

        print('uploading to ftp...')
        ftp.upload_file(file_path_128, _128_name)

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(file_path_128):
            os.remove(file_path_128)
        return '%s%s/%s' % (setting.FILESERVERHOST, setting.FTPDIR, _128_name), ''

    except:
        if os.path.exists(file_path):
            os.remove(file_path)
        return False, traceback.format_exc()


def upload_file_to_oss_and_scp(file_path, name):
    print('uploadImgToOSSAndscp, ', name)
    try:
        print('uploading to oss...')
        oss.upload_file(name, file_path)

        print('format mp3 file...')
        file_path_128 = file_path.replace('.mp3', '_128.mp3')
        get_mp3file(file_path, file_path_128)

        _128_name = name.replace('.mp3', '_128.mp3')

        print('uploading to scp...')
        scp.ssh_scp_put(file_path_128, _128_name)

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(file_path_128):
            os.remove(file_path_128)
        return '%s%s/%s' % (setting.FILESERVERHOST, setting.FTPDIR, _128_name), ''

    except:
        if os.path.exists(file_path):
            os.remove(file_path)
        return False, traceback.format_exc()


def get_mp3file(out_file_path, out_file_path_mp3):
    try:
        ff = FFmpeg(inputs={out_file_path: '-loglevel quiet'}, outputs={out_file_path_mp3: '-y'})
        print(ff.cmd)
        ff.run()
    except:
        print(traceback.format_exc())