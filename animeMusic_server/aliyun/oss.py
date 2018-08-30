import oss2
from .import setting

ossauth = oss2.Auth(setting.OSSKEY, setting.OSSVALUE)
ossendpoint = 'http://oss-cn-hangzhou-internal.aliyuncs.com'
ossbucket = oss2.Bucket(ossauth, ossendpoint, setting.OSSNAME)


def uploadFile(key, path):
    try:
        if not ossbucket.object_exists(key):
            ossbucket.put_object_from_file(key, path)
        return True
    except:
        return False


if __name__ == '__main__':
    uploadFile('test.html', '/home/xiaoc/index.html')
    pass