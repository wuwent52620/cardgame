from queue import Queue
base_queue = Queue(12)
info_card = ['BasicCard']
base_attrs = {'name', 'kind', 'number', 'image', 'info'}


class _BaseDecor(object):
    __instance = None
    __full_size = 0
    __size = -1

    def __new__(cls, *args, **kwargs):
        if cls.__size < cls.__full_size:
            cls.__instance = super().__new__(cls)
            cls.__size += 1
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self, size):
        _BaseDecor.__full_size += size

    def __set__(self, instance, value):
        if instance(value, dict) and set(value.keys()) == base_attrs:
            if value['number'] >= 12:
                value['number'] = 12
            if value['number'] <= 1:
                value['number'] = 1
            for k, v in value.items():
                setattr(instance, k, v)
        else:
            raise AttributeError('Cards json file is error')


class Number(object):

    def __set__(self, instance, value):
        if value < 1:
            setattr(instance, 'number', 1)



def create_info_queue():
    for i in range(1, 13):
        pass


class CardMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        if clsname not in info_card:
            return super().__new__(cls, clsname, bases, clsdict)


class BaseCard(metaclass=CardMeta):
    __slots__ = ['name', 'kind', 'number', 'image', 'info']
    __red_tao = red_tao()
    __mei_hua = mei_hua()
    __fang = fang_()
    __black_tao = black_tao()

    def __init__(self, kind, number):
