# -*- coding:utf-8 -*-
import sys
import urllib.request

import datetime
import requests
import re
import time
import types
import http.client
from pyquery import PyQuery as pq  # sudo pip install PyQuery


class c_python:
    # 截取字符串
    @staticmethod
    def getString(data, startStr, endStr, contain=False):
        try:
            startIndex = 0 if startStr == '' else data.find(startStr)
            if data[startIndex:].find(endStr) == -1:
                return ''
            endIndex = len(data) if endStr == '' else data[startIndex:].find(endStr) + startIndex + endStr.__len__()
            if not contain:
                startIndex += startStr.__len__()
                endIndex -= endStr.__len__()
            return data[startIndex:endIndex]
        except:
            return ''

    # 删除字典中指定的key
    @staticmethod
    def removeDicKey(dic, keyList=[]):
        try:
            for k in keyList:
                if k == '': continue;
                if k in dic.keys():
                    dic.pop(k)
            return dic
        except:
            return dic

    # 将Str转换为datetime格式
    @staticmethod
    def strToTime(str, format='auto'):
        try:
            str_bak = str
            str = str.replace('年', '-').replace('月', '-').replace('日', '').replace('时', ':').replace('分', ':').replace(
                '秒', '')
            if str.endswith(':'):
                str = str[0:''.__len__() - 1]
            if re.match('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', str):
                format = '%Y-%m-%d %H:%M:%S'
            elif re.match('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', str):
                format = '%Y-%m-%d %H:%M'
            elif re.match('\d{4}-\d{1,2}-\d{1,2}', str):
                format = '%Y-%m-%d'
            else:
                str = str_bak
                num = re.findall('^\d*', str)[0]
                if num != '':
                    num = int(num)
                    time = datetime.datetime.now()
                    str = str.replace('前', '').replace('分钟', '分').replace('小时', '时')
                    if str.rfind('秒') > -1:
                        return time + datetime.timedelta(seconds=-num)
                    if str.rfind('分') > -1:
                        return time + datetime.timedelta(minutes=-num)
                    if str.rfind('时') > -1:
                        return time + datetime.timedelta(hours=-num)
                    if str.rfind('天') > -1:
                        return time + datetime.timedelta(days=-num)
                    if str.rfind('周') > -1:
                        return time + datetime.timedelta(weeks=-num)
                    if str.rfind('月') > -1:
                        return time + datetime.timedelta(days=-(num*30))

            date_time = datetime.datetime.strptime(str, format)
            return date_time
        except:
            return None

    # 将datetime转换为指定格式的字符串
    @staticmethod
    def getStrTime(time=datetime.datetime.now(), format='%Y-%m-%d'):
        try:
            return time.__format__(format)
        except:
            return None

    # 将时间戳转换为datetime
    @staticmethod
    def unixtimeToDatetime(timestamp):
        time_local = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    # 将datetime转换为时间戳
    @staticmethod
    def datetimeToUnixtime(_datetime):
        return time.mktime(_datetime.timetuple())

    # 格式化输出的JSON数据
    @staticmethod
    def formatWriteJson(data):
        for key in data.keys():
            if type(data[key]) not in (
                    int, str, bool, float, bytes,type(None)):
                data[key] = str(data[key])
        return data


class c_spider:
    defaultHeaders = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
        'Accept': '*/*',
        'cache-control': "no-cache"
    }

    # 获取网页源代码
    @staticmethod
    def getHtml(url, headers=None, encode=None, maxError=3, timeout=10):
        error = 0
        while error < maxError:
            try:
                if not headers:
                    headers = c_spider.defaultHeaders
                    headers.__setitem__('Referer', url)

                request = urllib.request.Request(url)
                for key in headers:
                    request.add_header(key, headers[key])

                response = urllib.request.urlopen(request, timeout=timeout)
                html = response.read()
                if encode:
                    return html.decode(encode)
                else:
                    return html
            except:
                error += 1

    # 获取网页源代码
    @staticmethod
    def getHtmlForRequests(url, maxError=5, timeout=10, headers=None, encode=None):
        error = 0
        while error <= maxError:
            if not headers:
                headers = c_spider.defaultHeaders
                headers.__setitem__('Referer', url)

            response = requests.request("GET", url, headers=headers, timeout=timeout)
            html = response.text
            if not html.strip():
                time.sleep(1)
                error += 1
                continue
            if encode:
                return html.decode(encode)
            else:
                return html

    @staticmethod
    def postForRequest(url='', params='', _data='', headers=None, encode=None, timeout=10):
        if not headers:
            headers = c_spider.defaultHeaders
            headers.__setitem__('Referer', url)

        response = requests.request('POST', url, data=_data, headers=headers, params=params, timeout=timeout)
        html = response.text
        if encode:
            return html.decode(encode)
        else:
            return html

    @staticmethod
    def postForRequestReturnHtmlAndCookie(url='', params='', _data='', headers=None, encode=None, timeout=10):
        if not headers:
            headers = c_spider.defaultHeaders
            headers.__setitem__('Referer', url)

        response = requests.request('POST', url, data=_data, headers=headers, params=params, timeout=timeout)
        html = response.text
        if encode:
            return html.decode(encode), ';'.join([(f[0] + '=' + f[1]) for f in response.cookies.items()])
        else:
            return html, ';'.join([(f[0] + '=' + f[1]) for f in response.cookies.items()])

    @staticmethod
    def post(url, _data, headers=None, ):
        if not headers:
            headers = c_spider.defaultHeaders
            headers.__setitem__('Referer', url)
        conn = http.client.HTTPConnection('www.51mokao.com');
        conn.request(method="POST", url='/testpractice?id=11757', body=_data, headers=headers);
        # 返回处理后的数据
        response = conn.getresponse()
        return response.msg

    # 清理A标签
    @staticmethod
    def clearA(data):
        jq = pq(data)
        for f in jq('a'):
            f = pq(f)
            f.attr('href', None)
        return jq.outer_html()

    # 清理指定标签 clearLabel('<html>...</html>', ['a', 'img'])
    @staticmethod
    def clearLabel(data, name):
        for n in name:
            jq = pq(data)(n)
            for f in jq:
                f = pq(f)
                if data.find(f.outer_html()) > -1:
                    data = data.replace(f.outer_html(), '')
                else:
                    data = data.replace(f.html(), '')
        return data

    # 清除掉所有html标签
    @staticmethod
    def clearAllHtmlLabel(data):
        result, number = re.subn("<[\s\S]+?>", '', data)
        return result

    @staticmethod
    def clearLabelForContains(data, label, str):
        temp = pq(data)('%s:contains("%s")' % (label, str)).html()

        if temp and data.find(temp) > -1:
            data = data.replace(temp, '')
        return data

    # 删除掉多余的attr
    # selectStr: 即为选择器的表达式，JQ中$(".abc")，.abc则为表达式
    @staticmethod
    def removeAttr(data, selectStr, attrList=[]):
        jq = pq(data)
        for f in jq(selectStr):
            f = pq(f)
            for attr in attrList:
                f.remove_attr(attr)
        return jq.outer_html()

    # 补全URL（有些img之内的标签，其中src是相对路径，采集过后会导致图片无法显示，所以需要补全成绝对路径）
    @staticmethod
    def completionSrc(data, selectStr, host, attr='src'):
        jq = pq(data)
        for f in jq(selectStr):
            f = pq(f)
            if f.attr(attr).find('http') != 0:
                f.attr(attr, ('%s%s%s' % (host, ('' if f.attr(attr).find('/') == 0 else '/'), f.attr(attr))))
        return jq.outer_html()


if __name__ == '__main__':
    # html = c_python.getHtml('http://www.baidu.com')
    # print c_python.getString('asdasd132aabbccddee233dasdasd3adasd4', '132', '233de',True)
    pass
