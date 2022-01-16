# encoding: utf-8

from app.views.index_view import IndexHandler

# 配置路由
urls = [
    (r"/", IndexHandler),
]

