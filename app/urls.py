# encoding: utf-8

from app.views.index_view import IndexHandler

# 配置路由
from app.views.user_view import UserHandler

urls = [
    (r"/index", IndexHandler),
    (r"/user", UserHandler),
]

