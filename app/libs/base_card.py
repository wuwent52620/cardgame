import json
import os
import random
from importlib import import_module

from collections import deque

from tqdm import tqdm

import app
from app.config import kind_list, root_path
from app.views.base_view import BaseHandler

card_gen = {key: deque(range(1, 13)) for key in kind_list}

info_card = ['BasicCard']
base_attrs = {'name', 'kind', 'number', 'image', 'info'}


def __gen_id():
    i = 0
    while True:
        i += 1
        yield i


id_gen = __gen_id()


def gen_card(kind, num=None, **kwargs):
    kwargs.pop('number')

    def __gen_card(kind, num):
        for n in range(num):
            res = card_gen[kind].popleft()
            card_gen[kind].append(res)
            yield {'id': next(id_gen), 'kind': kind, 'number': res, **kwargs}

    return __gen_card(kind, num)


class Blood(object):
    def __set__(self, instance, value):
        if value < 0:
            setattr(instance, 'alive', False)
        setattr(instance, '_blood', value)

    def __get__(self, instance, owner):
        return getattr(instance, '_blood')


class CardMeta(type):  # todo all print must be replace by log
    def __new__(cls, clsname, clsbase, clsdict):
        file_path = os.path.join(root_path, 'card', f'{clsname.lower()}.json')
        if not clsname.lower().startswith('base'):
            with open(file_path, 'rb') as fl:
                base_info = json.load(fl)
                if clsname.lower().split('card')[0] in os.environ.get('card').split():
                    print(f'{clsname.lower()}版本有变， 即将更新数据库')
                    clsdict.update(reload=True)
                else:
                    print(f'{clsname.lower()}版本未变更')
                    clsdict.update(reload=False)

                clsdict.update(base_info=base_info)
        return super().__new__(cls, clsname, clsbase, clsdict)


class CardMixin(object):
    def __init__(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]

    def use(self, func, targets):
        """
        所有牌打出都是调用use方法
        :param func: 各自卡牌的发动自己技能的方法
        :param targets: 作用目标对象集
        :return: None
        """
        for target in targets:
            func = getattr(self, func)
            func(target)

    def __repr__(self):
        return f"{self.name}--{self.info}"


class RoleCard(CardMixin, metaclass=CardMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alive = True

    @classmethod
    def create(cls):
        cls.__slots__ = tuple(cls.base_info['cards'][0].keys())
        cards = deque()
        for single in cls.base_info['cards']:
            cards.append(cls(**single))
        random.shuffle(cards)
        return cards

    @classmethod
    def reload_card(cls):  # todo 交给杨希柳去写吧
        if cls.reload:
            pass


class BaseCard(CardMixin, BaseHandler, metaclass=CardMeta):
    _aclass = None

    @classmethod
    def create(cls):
        cls.__slots__ = tuple(cls.base_info['cards'][0].keys())
        cards = deque()
        for single in cls.base_info['cards']:
            cards.append(cls(**single))
        return cards

    @classmethod
    def reload_card(cls, session):
        reduce_attr = ['update_time', 'create_time']
        package = f"app.models.card"
        mod_name = f"{cls.__name__}"
        mod = import_module(package, mod_name)
        cls._aclass = getattr(mod, mod_name)
        new_base_info_cards = list()
        if cls.reload:
            cards = session.query(cls._aclass).filter(cls._aclass.id != 0)
            if cards:
                for card in cards:
                    session.delete(card)
            for card in cls.base_info['cards']:
                cards = list()
                for kind, number in tqdm(card['number'].items(), postfix={'version': ''}, desc=f'生成{cls.__name__}'):
                    card_info_gen = [card_info for card_info in gen_card(kind, number, **card)]
                    cards.extend([cls._aclass(**card_info) for card_info in card_info_gen])
                    session.add_all(cards)
                    new_base_info_cards.extend(card_info_gen)
        else:
            from app.models import model_to_dict
            cards = session.query(cls._aclass).all()
            data = [{k: v for k, v in model_to_dict(host).items() if k not in reduce_attr} for host in cards]
            new_base_info_cards.extend(data)


class BasicCard(BaseCard):
    pass


def init_cards(session):
    cls_list = BaseCard.__subclasses__()
    cards = deque()
    for cls in cls_list:
        cls.reload_card(session)
        cards += cls.create()
    random.shuffle(cards)
    return cards


if __name__ == '__main__':
    res = RoleCard.create()
    print(res)
