#-*- coding:utf-8 -*-

from .base import *
from bson import ObjectId


class AnimeList(Model):
    name = 'anime_list'

    """
    id: 此字段只是为了方便之前的数据转移，现在没用了
    """
    field = {
        'title':        (str,                  ''),
        'desc':         (str,                  ''),
        'bg':           (str,                  ''),
        'atime':        (int,                   0),
        'id':           (str,                  ''),
        'logo':         (str,                  ''),
        'year':         (int,                   0),
        'month':        (int,                   0),
    }


class MusicList(Model):
    name = 'music_list'

    """
    """
    field = {
        'anime_id':      (ObjectId,           None),
        'title':         (str,                  ''),
        'author':        (str,                  ''),
        'atime':         (int,                None),
        'recommend':     (int,                   0),
    }