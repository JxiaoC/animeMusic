# -*- coding:utf-8 -*-

import turbo

class BaseHandler(turbo.app.BaseHandler):
    def initialize(self):
        super(BaseHandler,self).initialize()

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
