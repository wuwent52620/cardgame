# encoding: utf-8

from sqlalchemy import Column, String, Integer

from app.models import BaseModel, model_to_dict


class Host(BaseModel):
    __tablename__ = 'host'
    hostname = Column('hostname', String(64), unique=True, nullable=False)
    ip = Column('ip', String(15), nullable=False)
    port = Column('port', Integer, nullable=False)
