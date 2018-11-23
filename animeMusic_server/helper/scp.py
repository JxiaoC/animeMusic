# -*- coding:utf-8 -*-

import paramiko, datetime
from .import realpath
from .import setting


def ssh_scp_put(local_file, name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(setting.SCP_IP, setting.SCP_PORT, setting.SCP_USER, setting.SCP_PASSWORD)
    a = ssh.exec_command('date')
    stdin, stdout, stderr = a
    print(stdout.read())
    sftp = ssh.open_sftp()
    sftp.put(local_file, setting.SCP_REMOTE_DIR + name)


if __name__ == '__main__':
    open('test.txt', 'wb').write(b'test')
    ssh_scp_put('test.txt', 'heihei.txt')