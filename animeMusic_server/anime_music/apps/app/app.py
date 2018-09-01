# -*- coding:utf-8 -*-
# pip install xpinyin

import turbo.log
from bson import ObjectId
import tornado

import json
import redis
import time
import random
from models.anime_music import model
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
    @tornado.web.asynchronous
    def get(self, id=None):
        if not id or not ObjectId.is_valid(id):
            recommend = self.get_argument('recommend', '0')
            id = ObjectId(self.get_random_id(recommend))
        info = tb_music.find_one({'_id': ObjectId(id)})
        info['anime_info'] = self.get_anime_info(info.get('anime_id', None))
        info['id'] = str(info.pop('_id'))
        info.pop('anime_id')
        info['play_url'] = GetSignUrl(info['id'])
        self.set_header("Access-Conitrol-Allow-Origin", "*")
        self.write(info)
        self.finish()

    def get_anime_info(self, animeid):
        if not animeid:
            return {}
        info = tb_anime.find_one({'_id': animeid})
        info['id'] = str(info.pop('_id'))
        return info

    def get_random_id(self, recommend):
        key = 'recommend_keys' if recommend == 'true' else 'keys'
        keys = r.get(key)
        if keys:
            keys = json.loads(keys.decode())
        else:
            keys = []
            Q = {}
            if recommend == 'true':
                Q = {'recommend': 1}
            list = tb_music.find(Q, {'_id': 1})
            for f in list:
                keys.append(str(f['_id']))
            r.set(key, json.dumps(keys))
            r.expire(key, 600)

        return keys[random.randint(0, len(keys) - 1)]
