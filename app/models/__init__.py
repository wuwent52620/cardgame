# encoding: utf-8
import json
import os
from datetime import datetime

from sqlalchemy.orm import class_mapper

from app.config import root_path

card_path = os.path.join(root_path, 'card')

version_file = os.path.join(card_path, f"card_version.json")

from app.libs.db_orm import ORM, Base
from sqlalchemy import Column, Integer, DateTime

orm = ORM()
engine = orm.get_engine()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column('create_time', DateTime(), default=datetime.now)
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


def init_data(session, name):
    file = os.path.join(card_path, f"{name}.json")
    with open(version_file, 'w+') as f1:
        c_version = json.load(f1)
        with open(file, 'r') as f2:
            data = json.load(f2)
            if data['version'] != c_version[name]:
                session.delete_all()
