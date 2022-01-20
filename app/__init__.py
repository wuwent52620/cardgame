# encoding: utf-8
import os
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
