# encoding: utf-8

from sqlalchemy import Column, String, Integer, Text, SmallInteger

from app.models import BaseModel, model_to_dict


class BasicCard(BaseModel):
    __tablename__ = 'BasicCard'
    name = Column('name', String(16), nullable=False)
    kind = Column('kind', String(16), unique=True, nullable=False)
    number = Column('number', SmallInteger(), nullable=False)
    func = Column('func', String(16), nullable=False)
    image = Column('image', String(32), nullable=False, default=3)
    info = Column('info', Text(length=256), nullable=False)
