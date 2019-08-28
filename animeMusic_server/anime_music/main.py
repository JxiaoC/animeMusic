#-*- coding:utf-8 -*-

from tornado.options import define, options
import tornado.options

import setting
import turbo.register
import turbo.app

turbo.register.register_app(setting.SERVER_NAME, setting.TURBO_APP_SETTING, setting.WEB_APPLICATION_SETTING, __file__, globals())

define("port", default=8885, type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    turbo.app.start(options.port)