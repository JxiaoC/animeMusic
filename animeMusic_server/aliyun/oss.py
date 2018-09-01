import oss2
from .import setting

ossauth = oss2.Auth(setting.OSSKEY, setting.OSSVALUE)
if setting.Debug:
    ossendpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
else:
    ossendpoint = 'http://oss-cn-hangzhou-internal.aliyuncs.com'
ossbucket = oss2.Bucket(ossauth, ossendpoint, setting.OSSNAME)


def upload_file(key, path):
    try:
        if not ossbucket.object_exists(key):
            ossbucket.put_object_from_file(key, path)
        return True
    except:
        return False


def del_file(key):
    try:
        if ossbucket.object_exists(key):
            ossbucket.delete_object(key)
        return True
    except:
        return False


if __name__ == '__main__':
    upload_file('test.html', '/home/xiaoc/index.html')
    pass