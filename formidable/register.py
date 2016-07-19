# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Register(dict):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def to_choices(self):
        return [(key, key) for key in self.keys()]


class FieldSerializerRegister(Register):
    lookup_field = 'type_id'


class ValidationSerializerRegister(Register):
    lookup_field = 'type'


def load_serializer(register):

    def _wrapper(klass):
        register[klass.type_id] = klass
        return klass

    return _wrapper
