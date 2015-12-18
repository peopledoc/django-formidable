# -*- coding: utf-8 -*-


class SerializerRegister(dict):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def to_choices(self):
        return [(key, key) for key in self.keys()]


def load_serializer(klass):
    SerializerRegister.get_instance()[klass.type_id] = klass
    return klass
