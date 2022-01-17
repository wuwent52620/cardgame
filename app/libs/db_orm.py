# encoding: utf-8

import pymysql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from app.config import config

Base = declarative_base()  # 调用
metadata = Base.metadata  # 创建元类


class ORM:
    def __init__(self):
        self.mysql_config = dict(
            db_host=config['db_host'],
            db_user=config['db_user'],
            db_pwd=config['db_pwd'],
            db_port=config['db_port'],
            db_name=config['db_name']
        )

    def get_engine(self):
        # 创建连接引擎，encoding定义编码，echo是(True)否(False)输出日志
        engine = create_engine(
            'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8'.format(**self.mysql_config),
            echo=False)
        return engine

    def create_all(self):
        metadata.create_all(self.get_engine())

    def create_session(self):
        session = sessionmaker(
            bind=self.get_engine(),
            autocommit=True,
            autoflush=True,
            expire_on_commit=False
        )
        return session()
