#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import socket
import json
import base64
import time


def CheckData(data, url):
    try:
        dic = json.loads(data)
        if dic['status'] != 'completehelp' or dic['url'] != url:
            return ''
        data = dic['data']
        data = base64.b64decode(data)
        return data
    except:
        return ''


class socketClient:

    SocketServerAddress = None
    SocketServerPort = 0
    sock = None

    def getHtml(self, url, cookie, needprovince, header, encode, timeout, maxms, minnum):
        try:
            errorNum = 0
            retNum = 0
            self.Connet()
            self.sock.settimeout(timeout)
            self.sock.connect((self.SocketServerAddress, self.SocketServerPort))
            sendDic = {
                'status': 'needhelp',
                'needprovince': needprovince,
                'url': url,
                'cookie': cookie,
                'encode': encode,
                'maxms': maxms,
                'minnum': minnum,
            }

            self.sock.send(json.dumps(sendDic))
            retData = ''
            while True:
                try:
                    # print 'begin to rec'
                    buf = self.sock.recv(4096)

                    retNum += 1
                    if retNum >= 100:
                        self.Close()
                        return '[proxyError]error ret'

                    retData += buf
                    if str(buf).endswith('}'):
                        retData = CheckData(retData, url)
                        if not retData:
                            continue
                        break
                except Exception as e:
                    time.sleep(1)
                    errorNum += 1
                    if errorNum >= 5:
                        self.Close()
                        return '[proxyError]timed out'
                    if e.message == 'timed out':
                        self.sock.send(json.dumps(sendDic))
                        retData = ''
                    pass
            pass
        except Exception as e:
            print e
            self.Close()
            return '[proxyError]socket Error'
        self.Close()
        return retData

    def Connet(self):
        try:
            self.sock.send('t')
        except:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Close(self):
        try:
            self.sock.close()
        except:
            pass