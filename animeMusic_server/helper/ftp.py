# -*- coding:utf-8 -*-
import ftplib
import traceback
from .import setting

# setting参数说明
# FTPDIR: FTP上传文件目录, 使用/开头
# FTPADDRESS: FTP地址, 推荐使用IP
# FTPUSER: FTP登录账号
# FTPASSWD: FTP登录密码
def upload_file(file_path, name, to_dir=setting.FTPDIR):
    f = ftplib.FTP(setting.FTPADDRESS)
    f.login(setting.FTPUSER, setting.FTPASSWD)
    f.cwd(to_dir)
    bufsize = 1024
    fp = open(file_path, 'rb')
    f.storbinary('STOR ' + name, fp, bufsize)
    fp.close()


def del_file(name, dir=setting.FTPDIR):
    f = ftplib.FTP(setting.FTPADDRESS)
    f.login(setting.FTPUSER, setting.FTPASSWD)
    f.cwd(dir)
    [(_name == name and f.delete(name)) for _name in f.nlst()]


# 没有找到在FTP直接判定文件是否存在的方法, 无脑循环在文件较多时效率会极低, 也可以直接使用下面这种try ex的方式直接容错处理
# def del_file(name, dir=setting.FTPDIR):
#     try:
#         f = ftplib.FTP(setting.FTPADDRESS)
#         f.login(setting.FTPUSER, setting.FTPASSWD)
#         f.cwd(dir)
#         f.delete(name)
#     except:
#         pass

if __name__ == '__main__':
    # upload_file('/home/xiaoc/1.jpg', 'test.jpg', setting.FTPDIR)
    del_file('test.jpg')