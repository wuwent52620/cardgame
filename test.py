from datetime import datetime
import re
import pickle
from queue import Queue


class A(type):
    def __new__(cls, *args, **kwargs):
        print(args, kwargs, '----')
        return super().__new__(cls, *args, **kwargs)


class B(metaclass=A):
    __slots__ = ['c']
    _ad = 'ad'

    @classmethod
    def q(cls):
        return 'q'

    def f(self):
        return 1

    def y(self):
        return 2

    def __init__(self, *args):
        self.c = 'e'


q = Queue(10)
for i in range(12):
    q.put('abcd')

print(q)