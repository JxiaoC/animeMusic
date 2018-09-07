# -*- coding:utf-8 -*-

import turbo.log
from .base import BaseHandler
from helper import app
logger = turbo.log.getLogger(__file__)


class MusicHeader(BaseHandler):
    def get(self, id=None):
        recommend = self.get_argument('recommend', '0')
        info = app.get_music_info(id, recommend)
        self.write({'code': 0, 'msg': 'ok', 'res': info})


class MusicListHeader(BaseHandler):
    def get(self):
        limit = int(self.get_argument('limit', 15))
        page = int(self.get_argument('limit', 1))
        info = app.get_music_list(limit, page)
        self.write({'code': 0, 'msg': 'ok', 'res': info})


class MusicSearchHeader(BaseHandler):
    def get(self):
        key = self.get_argument('key', '')
        limit = int(self.get_argument('limit', 15))
        page = int(self.get_argument('limit', 1))
        res = app.search_music(key, limit, page)
        self.write({'code': 0, 'msg': 'ok', 'res': res})


class AnimeSearchHeader(BaseHandler):
    def get(self):
        key = self.get_argument('key', '')
        limit = int(self.get_argument('limit', 15))
        page = int(self.get_argument('limit', 1))
        res = app.search_anime(key, limit, page)
        self.write({'code': 0, 'msg': 'ok', 'res': res})