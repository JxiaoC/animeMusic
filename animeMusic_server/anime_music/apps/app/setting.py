#-*- coding:utf-8 -*-

# sub app setting
# try not to include function or class 

import os
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = 'app/'

CachePath = '/data/image/'

QiNiuUrl = 'http://cdn.video.dandanjiang.tv/'

if os.path.exists(os.path.join(SERVER_DIR, '__test__')):
    Debug = True
else:
    Debug = False