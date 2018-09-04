# -*- coding:utf-8 -*-

import turbo.log
from helper import app
logger = turbo.log.getLogger(__file__)


class MusicHeader(turbo.app.BaseHandler):
    def get(self, id=None):
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        recommend = self.get_argument('recommend', '0')
        info = app.get_music_info(id, recommend)
        self.write(info)
