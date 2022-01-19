import json
import os
import random

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
        if value < 0:
            setattr(instance, 'alive', False)
        setattr(instance, '_blood', value)

    def __get__(self, instance, owner):
        return getattr(instance, '_blood')


class CardMeta(type):
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

                clsdict.update(base_info=base_info)
        return super().__new__(cls, clsname, clsbase, clsdict)


class CardMixin(object):
    def use(self, func, targets):
        for target in targets:
            func = getattr(self, func)
            func(target)


class RoleCard(CardMixin, metaclass=CardMeta):

    def __init__(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]
        self.alive = True

    @classmethod
    def create(cls):
        cls.__slots__ = tuple(cls.base_info['cards'][0].keys())
        cards = deque()
        for single in cls.base_info['cards']:
            cards.append(cls(**single))
        random.shuffle(cards)
        return cards

    def __repr__(self):
        return f"{self.name}--{self.info}"


class BaseCard(CardMixin, metaclass=CardMeta):
    pass


if __name__ == '__main__':
    res = RoleCard.create()
    print(res)
