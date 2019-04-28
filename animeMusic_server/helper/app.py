# -*- coding:utf-8 -*-
from .import realpath
from .import setting
import random
from bson import ObjectId
import redis
import time
import hashlib
import json

from models.anime_music import model

tb_anime = model.AnimeList()
tb_music = model.MusicList()

r = redis.Redis(host='127.0.0.1', port=6379, db=0)


def GetSignUrl(id):
    timeout = int(time.time() + 3600)
    m2 = hashlib.md5()
    m2.update(('%s%s{AnimeToken}' % (id, timeout)).encode('utf-8'))
    return '%s/%s_128.mp3?t=%s&sign=%s' % (setting.FILESERVERHOST, id, timeout, m2.hexdigest().upper())


def get_music_info(id, recommend):
    if not id or not ObjectId.is_valid(id):
        id = ObjectId(get_random_id(recommend))
    else:
        id = ObjectId(id)
    info = tb_music.find_one({'_id': id})
    return format_music_info(info)


def format_music_info(info):
    info['anime_info'] = get_anime_info(info.get('anime_id', None))
    info['id'] = str(info.pop('_id'))
    info.pop('anime_id')
    info['play_url'] = GetSignUrl(info['id'])
    info['type'] = info.get('type', '其他')
    info['author'] = info.get('author', '未知')
    info['recommend'] = True if info.get('recommend', False) else False
    return info


def get_anime_info(animeid):
    if not animeid:
        return {}
    info = tb_anime.find_one({'_id': animeid})
    info['id'] = str(info.pop('_id'))
    if 'tietukuname' in info.keys(): info.pop('tietukuname')
    return info


def get_random_id(recommend):
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


def get_music_list(limit, page):
    _list = tb_music.find().sort('atime', -1).limit(limit).skip((page - 1) * limit)
    res = []
    for f in _list:
        f = format_music_info(f)
        f.pop('play_url')
        res.append(f)
    return res


def search_music(key, limit, page):
    limit, page = int(limit), int(page)
    _list = tb_music.find({'title': {'$regex': key}}).sort('atime', -1).limit(limit).skip((page - 1) * limit)
    res = []
    for f in _list:
        f = format_music_info(f)
        f.pop('play_url')  # 因为play_url有时效性, 可能在使用的时候就已经失效了, 所以这里过滤掉.
        res.append(f)
    return res


def search_anime(key, limit, page):
    anime_list = tb_anime.find({'title': {'$regex': key}}).sort('atime', -1)
    anime_ids = []
    for f in anime_list:
        anime_ids.append(f['_id'])
    res = []

    _list = tb_music.find({'anime_id': {'$in': anime_ids}}).sort('atime', -1).limit(limit).skip((page - 1) * limit)
    for f in _list:
        f = format_music_info(f)
        f.pop('play_url')  # 因为play_url有时效性, 可能在使用的时候就已经失效了, 所以这里过滤掉.
        res.append(f)
    return res
