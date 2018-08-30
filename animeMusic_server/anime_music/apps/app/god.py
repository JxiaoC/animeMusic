# -*- coding:utf-8 -*-
# pip install xpinyin

import turbo.log
from bson import ObjectId

import json
import redis
import time
import random
from models.anime_music import model
from lib.c_python import c_python as cp
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
            res.append(cp.formatWriteJson(f))

        self.write({
            'code': 0,
            'msg': 'ok',
            'count': count,
            'data': res,
        })


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