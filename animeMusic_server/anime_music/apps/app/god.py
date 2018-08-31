# -*- coding:utf-8 -*-

import turbo.log
from bson import ObjectId

import json
import redis
import time
import os
import random
from models.anime_music import model
from helper.c_python import c_python as cp
import helper.image as image
import helper.tietuku as tietuku
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
    return 'http://anime-music.files.jijidown.com/%s_128.mp3?t=%s&sign=%s' % (id, timeout, m2.hexdigest().upper())


class MusicHeader(turbo.app.BaseHandler):
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
            f['atime'] = str(cp.unixtimeToDatetime(f['atime']))
            res.append(cp.formatWriteJson(f))

        self.write({
            'code': 0,
            'msg': 'ok',
            'count': count,
            'data': res,
        })


class AnimeSaveHeader(turbo.app.BaseHandler):
    def post(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)
        title = self.get_argument('title', '')
        desc = self.get_argument('desc', '')
        year = int(self.get_argument('year', 0))
        month = int(self.get_argument('month', 0))

        tb_anime.update({'_id': id}, {'$set': {
            'title': title,
            'desc': desc,
            'year': year,
            'month': month,
        }})
        self.write({'code': 0, 'msg': 'ok'})


class AnimeDelHeader(turbo.app.BaseHandler):
    def post(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)
        if tb_music.find({'anime_id': id}).count() > 0:
            self.write({'code': -1, 'msg': '数据库内还有音频数据，无法删除'})
            return
        tb_anime.remove({'_id': id})
        self.write({'code': 0, 'msg': 'ok'})


class AnimeUploadLogoHeader(turbo.app.BaseHandler):
    def post(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)

        if not os.path.exists('temp'):
            os.mkdir('temp')

        file_path = 'temp/%s' % self.request.files['file'][0]['filename']
        with open(file_path, 'wb') as f:
            f.write(self.request.files['file'][0]['body'])

        image.clipResizeImg(path=file_path, out_path=file_path, width=1220, height=604, quality=65)

        image_url = tietuku.uploadImgToTieTuKu(file_path)

        if image_url:
            tb_anime.update({'_id': id}, {'$set': {'logo': image_url}})
            self.write({'code': 0, 'msg': 'ok', 'src': image_url})
        else:
            self.write({'code': -1, 'msg': '上传失败'})


class AnimeUploadBgHeader(turbo.app.BaseHandler):
    def post(self, id):
        if not id or not ObjectId.is_valid(id):
            return
        id = ObjectId(id)

        if not os.path.exists('temp'):
            os.mkdir('temp')

        file_path = 'temp/%s' % self.request.files['file'][0]['filename']
        with open(file_path, 'wb') as f:
            f.write(self.request.files['file'][0]['body'])

        image.resizeImg(path=file_path, out_path=file_path, width=1920, quality=65)

        image_url = tietuku.uploadImgToTieTuKu(file_path)

        if image_url:
            tb_anime.update({'_id': id}, {'$set': {'bg': image_url}})
            self.write({'code': 0, 'msg': 'ok', 'src': image_url})
        else:
            self.write({'code': -1, 'msg': '上传失败'})


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
            res.append(cp.formatWriteJson(f))

        self.write({
            'code': 0,
            'msg': 'ok',
            'count': count,
            'data': res,
        })