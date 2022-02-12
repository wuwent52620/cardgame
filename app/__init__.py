# encoding: utf-8
import os
import random
from collections import deque, Iterable
from contextlib import contextmanager

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options
from tornado.web import Application as tornadoApp
from app.config import config
from app.urls import urls
from app.libs.db_orm import ORM
from utils.decorator import singleton

orm = ORM()

# 定义服务的监听端口，主机IP
define("host", default="0.0.0.0", type=str, help="监听主机")
define("port", default=8000, type=int, help="监听端口")
define("db", default=None, type=str, help="数据库初使化或迁移")
define("card", default='', type=str, help="需要重新reload的卡牌类型, 可以是多个(空格隔开)")
define("version", default='', type=str, help="所用卡牌的版本号(此功能后续再说，先支持着)")


# 使用上下文管理器封装session的建立和关闭，这样就不用手动关闭session
@contextmanager
def session_maker(session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# 1.自定义app
class Application(tornadoApp):
    # 重写__init__构造方法
    def __init__(self):
        # 指定路由规则
        handlers = urls
        # 指定配置信息
        settings = config
        super(Application, self).__init__(handlers=handlers, **settings)

        from app import models
        orm.create_all()

        # 初使化session，方便在调用(self.session.query())
        self.session = orm.create_session()


class CardDeque(deque):
    __give_way = {'head': 'popleft', 'foot': 'pop'}
    __get_way = {'head': 'extendleft', 'foot': 'extend'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.name = kwargs.get('name')

    def give(self, num=1, way='head', define=None):
        try:
            if define and isinstance(define, int):
                return self[define]
            func = getattr(self, self.__give_way.get(way))
            cards = [func() for _ in range(num)]
            return cards
        except IndexError as e:
            return None

    def get(self, cards, way='head'):
        if not isinstance(cards, Iterable):
            cards = [cards]
        func = getattr(self, self.__get_way.get(way))
        func(cards)

    def shuffle(self):
        random.shuffle(self)


@singleton
class Game(object):
    __users = []
    __cards = {}

    def __init__(self):
        self.users = self.__users
        self.cards = self.__cards

    @classmethod
    def add_users(cls, args):
        cls.__users.append(args)

    @classmethod
    def add_cards(cls, **kwargs):
        cls.__cards.update(**kwargs)

    @classmethod
    def create(cls):
        if len(cls.__users) == 4:
            return cls()


# 2. 自定义服务
def create_server():
    # 允许在命令行启动
    tornado.options.parse_command_line()
    os.environ.update(card=options.card, version=options.version)
    # 创建http服务
    http_server = tornado.httpserver.HTTPServer(Application())
    # 绑定监听端口
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
