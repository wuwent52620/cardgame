# encoding: utf-8

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """封装session操作
    """

    @property
    def session(self):
        return self.application.session
