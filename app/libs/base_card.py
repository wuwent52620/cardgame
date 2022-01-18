import json
import os
from collections import deque

from app.config import kind_list, root_path

card_gen = {key: deque(range(1, 13)) for key in kind_list}

info_card = ['BasicCard']
base_attrs = {'name', 'kind', 'number', 'image', 'info'}


def gen_card(kind, num=None):
    _num = num

    def __gen_card(kind, num=100):
        if _num:
            num = _num
        for n in range(num):
            res = card_gen[kind].popleft()
            card_gen[kind].append(res)
            yield kind, res

    return __gen_card(kind, num)


class Blood(object):
    def __set__(self, instance, value):
        print(instance, value)
        if value < 0:
            setattr(instance, 'alive', False)
        setattr(instance, '_blood', value)

    def __get__(self, instance, owner):
        return getattr(instance, '_blood')


class CardMixin(object):
    def use(self, func, targets):
        for target in targets:
            func = getattr(self, func)
            func(target)


class RoleCard(CardMixin):
    __slots__ = []
    blood = Blood()

    def __init__(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]
        self.alive = True


class CardMeta(type):
    def __new__(cls, clsname, clsbase, clsdict):
        file_path = os.path.join(root_path, 'card', f'{clsname.lower()}.json')
        with open(file_path, 'rb') as fl:
            base_info = json.load(fl)
            clsdict.update(_base_info=base_info)
        return super().__new__(cls, clsname, clsbase, clsdict)


class BaseCard(metaclass=CardMeta):
    __slots__ = ['name', 'kind', 'number', 'image', 'info']


print(BaseCard.__subclasses__())
