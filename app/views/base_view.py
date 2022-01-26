# encoding: utf-8
import json

import tornado.web
import tornado.websocket


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


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = dict()

    # 有新的连接时open()函数将会被调用,将客户端的连接统一放到self.clients
    def open(self, *args, **kwargs):
        self.id = self.get_argument("id")
        # self.stream.set_nodelay(True)
        self.clients[self.id] = {"id": self.id, "object": self}
        print(self.clients)
        print("建立连接...")

    # 客户收到消息将被调用
    def on_message(self, message):
        print("client %s received a message: %s" % (self.id, message))

    # 关闭连接时被调用
    def on_close(self):
        if self.id in self.clients:
            del self.clients[self.id]
        print("client %s is closed" % self.id)

    def check_origin(self, origin):
        return True
