# encoding: utf-8

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """封装session操作
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.libs.base_card import init_cards
        init_cards(session=self.session)

    @property
    def session(self):
        return self.application.session
