# -*- coding: utf-8 -*-
from six import with_metaclass

from formidable.utils import singleton


class FunctionRegister(dict, singleton):
    pass


class FunctionMetaClass(type):

    def __new__(mcls, name, base, attrs):
        klass = super(FunctionMetaClass, mcls).__new__(mcls, name, base, attrs)
        if hasattr(klass, 'Meta'):
            register = FunctionRegister.get_instance()
            register[klass.Meta.name] = klass
        return klass


class Function(with_metaclass(FunctionMetaClass)):
    pass


class IsEmpty(Function):

    class Meta:
        name = 'is_empty'

    def __call__(self, value):
        return value in [None, '', 0, False]
