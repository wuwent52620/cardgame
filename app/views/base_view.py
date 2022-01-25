# encoding: utf-8
import json

import tornado.web


class BaseResponse(object):
    def __init__(self):
        self.__res_data = {"message": '', "state_code": 0, "data": {}}

    def update(self, **kwargs):
        self.__res_data.update(**kwargs)

    def update_data(self, **kwargs):
        self.__res_data['data'].update(**kwargs)

    @property
    def data(self):
        return json.dumps(self.__res_data, ensure_ascii=False)


class BaseHandler(tornado.web.RequestHandler):
    """封装session操作
    """
    __has_reload = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.libs.base_card import init_cards
        if not BaseHandler.__has_reload:
            init_cards(session=self.session)
            BaseHandler.__has_reload = True
        self.response = BaseResponse()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    @property
    def session(self):
        return self.application.session
