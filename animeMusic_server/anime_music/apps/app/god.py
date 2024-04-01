# -*- coding:utf-8 -*-

import turbo.log
from bson import ObjectId

import tornado
import redis
import time
import threading
import os
from models.anime_music import model
from helper.c_python import c_python as cp
from helper import image
from helper import tietuku
from helper import file_server
from helper import ftp
from lib import bangumi
from aliyun import oss
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import hashlib

logger = turbo.log.getLogger(__file__)

tb_anime = model.AnimeList()
tb_music = model.MusicList()

r = redis.Redis(host='127.0.0.1', port=6379,db=0)


def Sign(self):
    m2 = hashlib.md5()
    m2.update('%s%s{AnimeToken}' % (self.av, self.url))
    sign = m2.hexdigest().upper()
    return True if sign == self.sign else False


def GetSignUrl(id):
    timeout = int(time.time() + 3600)
    m2 = hashlib.md5()
    m2.update(('%s%s{AnimeToken}' % (id, timeout)).encode('utf-8'))
    return 'http://anime-music-files.jijidown.com/%s_128.mp3?t=%s&sign=%s' % (id, timeout, m2.hexdigest().upper())


class GodHeader(turbo.app.BaseHandler):
    def get(self):
        self.render('app/god/index.html')


class AnimeListHeader(turbo.app.BaseHandler):
    def get(self):
        search_value = self.get_argument('search_value', '')
        search_type = self.get_argument('search_type', '')
        page = int(self.get_argument('page', 1))
        if page <= 0: page = 1

        limit = int(self.get_argument('limit', 10))
        if limit <=0 or limit >= 100: limit = 10

        Q = {}
        if search_value and search_type in ['title', '_id']:
            if search_type == '_id':
                Q[search_type] = ObjectId(search_value)
            else:
                Q[search_type] = {'$regex': search_value}

        _list = tb_anime.find(Q).sort('atime', -1).limit(limit).skip((page - 1) * limit)
        count = tb_anime.find(Q).count()

        res = []
        for f in _list:
            f['atime'] = str(cp.unixtimeToDatetime(f.get('atime', 0)))
            res.append(cp.formatWriteJson(f))

        self.write({
            'code': 0,
            'msg': 'ok',
            'count': count,
            'data': res,
        })


class AnimeAddHeader(turbo.app.BaseHandler):
    def post(self):
        title = self.get_argument('title', '')
        if tb_anime.find_one({'title': title}):
            self.write({'code': -1, 'msg': '已经存在相同的名称了'})
            return
        tb_anime.insert({
            'title': title,
            'atime': int(time.time()),
            'desc': '',
            'bg': '',
            'logo': '',
            'year': 0,
            'month': 0,
        })
        self.write({'code': 0, 'msg': 'ok'})


class AnimeSearchBangumiHeader(turbo.app.BaseHandler):
    def post(self):
        title = self.get_argument('title', '')
        res = bangumi.search(title)
        self.write({'code': 0, 'msg': 'ok', 'res': res})


class AnimeHeader(turbo.app.BaseHandler):
    def post(self, type, id):
        if not id or not ObjectId.is_valid(id):
            return
        self.id = ObjectId(id)
        self.route(type)

    def do_save(self):
        title = self.get_argument('title', '')
        desc = self.get_argument('desc', '')
        year = int(self.get_argument('year', 0))
        month = int(self.get_argument('month', 0))

        tb_anime.update({'_id': self.id}, {'$set': {
            'title': title,
            'desc': desc,
            'year': year,
            'month': month,
        }})
        self.write({'code': 0, 'msg': 'ok'})

    def do_del(self):
        if tb_music.find({'anime_id': self.id}).count() > 0:
            self.write({'code': -1, 'msg': '数据库内还有音频数据，无法删除'})
            return
        tb_anime.remove({'_id': self.id})
        self.write({'code': 0, 'msg': 'ok'})


class AnimeUploadHeader(turbo.app.BaseHandler):
    def post(self, type, id):
        try:
            if not id or not ObjectId.is_valid(id):
                return
            id = ObjectId(id)

            if not os.path.exists('temp'):
                os.mkdir('temp')

            file_path = 'temp/%s' % self.request.files['file'][0]['filename']
            out_file_path = file_path.replace('png', 'jpg')
            with open(file_path, 'wb') as f:
                f.write(self.request.files['file'][0]['body'])

            if type == 'logo':
                image.clipResizeImg(path=file_path, out_path=out_file_path, width=1220, height=604, quality=85)
            else:
                image.resizeImg(path=file_path, out_path=out_file_path, width=1920, quality=85)

            image_url = tietuku.uploadImgToTieTuKu(out_file_path)

            if os.path.exists(file_path):
                os.remove(file_path)

            if os.path.exists(out_file_path):
                os.remove(out_file_path)

            if image_url:
                tb_anime.update({'_id': id}, {'$set': {type: image_url}})
                self.write({'code': 0, 'msg': 'ok', 'src': image_url})
            else:
                self.write({'code': -1, 'msg': '上传失败'})
        except Exception as e:
                self.write({'code': -1, 'msg': e})


class MusicListHeader(turbo.app.BaseHandler):
    def get(self):
        search_value = self.get_argument('search_value', '')
        search_type = self.get_argument('search_type', '')
        page = int(self.get_argument('page', 1))
        if page <= 0: page = 1

        limit = int(self.get_argument('limit', 10))
        if limit <=0 or limit >= 100: limit = 10

        Q = {}
        if search_value and search_type in ['title', '_id', 'anime_id']:
            if search_type in ['_id', 'anime_id']:
                Q[search_type] = ObjectId(search_value)
            else:
                Q[search_type] = {'$regex': search_value}

        _list = tb_music.find(Q).sort('atime', -1).limit(limit).skip((page - 1) * limit)
        count = tb_music.find(Q).count()

        res = []
        for f in _list:
            f['play_url'] = GetSignUrl(str(f['_id']))
            anime_info = tb_anime.find_one({'_id': f.get('anime_id', None)})
            if anime_info:
                f['anime_name'] = anime_info.get('title')
            else:
                f['anime_name'] = '未知'
            f['atime'] = str(cp.unixtimeToDatetime(f['atime']))
            res.append(cp.formatWriteJson(f))

        self.write({
            'code': 0,
            'msg': 'ok',
            'count': count,
            'data': res,
        })


class MusicAddHeader(turbo.app.BaseHandler):
    def post(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)

        title = self.get_argument('title', '')
        if tb_music.find_one({'title': title}):
            self.write({'code': -1, 'msg': '已经存在相同的名称了'})
            return
        tb_music.insert({
            'title': title,
            'atime': int(time.time()),
            'anime_id': id,
            'author': '',
            'recommend': False,
        })
        self.write({'code': 0, 'msg': 'ok'})


class MusicHeader(turbo.app.BaseHandler):
    @gen.coroutine
    def post(self, type, id):
        if not id or not ObjectId.is_valid(id):
            return
        self.id = ObjectId(id)
        self.route(type)

    def do_save(self):
        title = self.get_argument('title', '')
        author = self.get_argument('author', '')
        type = self.get_argument('type', '')
        recommend = True if self.get_argument('recommend', 'true') == 'true' else False

        tb_music.update({'_id': self.id}, {'$set': {
            'title': title,
            'type': type,
            'author': author,
            'recommend': recommend,
        }})
        self.write({'code': 0, 'msg': 'ok'})
        self.finish()

    def do_del(self):
        tb_music.remove({'_id': self.id})
        _thread = threading.Thread(target=self.thread_del)
        _thread.start()
        self.write({'code': 0, 'msg': 'ok'})
        self.finish()

    def thread_del(self):
        name = '%s.mp3' % self.id
        oss.del_file(name)
        ftp.del_file(name.replace('.mp3', '_128.mp3'))


class MusicUploadHeader(turbo.app.BaseHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def post(self, id):
        image_url, error_data = yield self.upload(id)
        if image_url:
            self.write({'code': 0, 'msg': 'ok', 'src': GetSignUrl(str(id))})
        else:
            self.write({'code': -1, 'msg': '上传失败:' + error_data})

    @run_on_executor
    def upload(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)

        if not os.path.exists('temp'):
            os.mkdir('temp')

        file_path = 'temp/%s' % self.request.files['file'][0]['filename']
        with open(file_path, 'wb') as f:
            f.write(self.request.files['file'][0]['body'])

        return file_server.upload_file_to_oss_and_scp(file_path, '%s.mp3' % id)