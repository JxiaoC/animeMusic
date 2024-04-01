#-*- coding:utf-8 -*-

from .base import *
from bson import ObjectId


class AnimeList(Model):
    name = 'anime_list'

    """
    id: 此字段只是为了方便之前的数据转移，现在没用了
    title: 标题
    desc: 描述
    bg: 背景图URL
    logo: 封面图URL
    atime: 添加时间，时间戳格式
    year: anime发行年份
    month: anime发行月份
    bangumi_id: 对应bangumi番剧id
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
        'bangumi_id':   (int,                   0),
        'tietukuname':  (str,                  ''),
    }


class MusicList(Model):
    name = 'music_list'

    """
    anime_id: 所属animeid
    title: 标题
    author: 作者
    atime: 添加时间，时间戳格式
    recommend: 是否为推荐, 1=true, 0=false
    type: 所属类型, op, ed, bgm, 角色歌, 其他
    """
    field = {
        'anime_id':      (ObjectId,           None),
        'title':         (str,                  ''),
        'author':        (str,                  ''),
        'atime':         (int,                None),
        'recommend':     (int,                   0),
        'type':          (str,                  ''),
    }