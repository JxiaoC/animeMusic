# -*- coding:utf-8 -*-

import turbo.log
from .base import BaseHandler
from helper import app
logger = turbo.log.getLogger(__file__)


class MusicHeader(BaseHandler):
    def get(self, id=None):
        recommend = self.get_argument('recommend', '0')
        info = app.get_music_info(id, recommend)
        self.write(info)