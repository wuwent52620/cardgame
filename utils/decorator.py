from functools import wraps


def singleton(cls):
    cls.__instance = None

    @wraps(cls)
    def inner(*args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    return inner


def keywords(keys=list()):
    def outer(cls):
        cls.__obj_dict = {}

        @wraps(cls)
        def inner(*args, **kwargs):
            obj_name = ''.join(str(kwargs.get(key)) for key in keys)
            if not cls.__obj_dict.get(obj_name):
                cls.__obj_dict[obj_name] = cls(*args, **kwargs)
            return cls.__obj_dict[obj_name]

        return inner

    return outer
