# encoding: utf-8

from sqlalchemy import Column, String, Integer, Text

from app.models import BaseModel, model_to_dict


class Role(BaseModel):
    __tablename__ = 'role'
    name = Column('name', String(16), unique=True, nullable=False)
    info = Column('info', String(32), nullable=False)
    belong = Column('belong', String(16), nullable=False)
    blood = Column('blood', Integer(), nullable=False, default=3)
    skill = Column('skill', Text(length=256), nullable=False)
