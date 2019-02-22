# -*- coding:utf-8 -*-
from .import setting
import time
import json
import os
import requests
from turbo.core.exceptions import ResponseMsg


def uploadImgToTieTuKu(file_path):
    exception = None
    Num = 0
    while Num < 3:
        try:
            Num += 1

            # 贴图库的token在http://www.tietuku.com/manager/createtoken可以获取到, 上传方式选择本地上传;
            # aid在http://www.tietuku.com/manager/album可以获取到, 就是相册的ID

            token, aid = setting.TieTuKuTOKEN, setting.TieTuKuAID

            data = {
                'deadline': int(time.time()) + 60,
                'from': 'file',
                'aid': aid,
                'Token': token
            }

            files = {'file': open(file_path, "rb")}

            reponse = requests.post('http://up.imgapi.com/', data=data, files=files)
            json_data = json.loads(reponse.text)
            if json_data.__len__() > 5:
                os.remove(file_path)
                return json_data['linkurl']
            else:
                exception = json_data
        except:
            pass
    raise ResponseMsg(-1, exception)

if __name__ == '__main__':
    print (uploadImgToTieTuKu('/home/xiaoc/1.jpg'))