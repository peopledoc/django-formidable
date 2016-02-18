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


class Add(Function):

    class Meta:
        name = 'add'

    def __call__(self, x, y):
        return x + y


class Sub(Function):

    class Meta:
        name = 'sub'

    def __call__(self, x, y):
        return x - y


class Mult(Function):

    class Meta:
        name = 'mult'

    def __call__(self, x, y):
        return x * y


class Div(Function):

    class Meta:
        name = 'div'

    def __call__(self, x, y):
        if y == 0:
            raise ZeroDivisionError()
        return x / y


class Not(Function):

    class Meta:
        name = 'not'

    def __call__(self, x):
        return not(x)


class Eq(Function):

    class Meta:
        name = 'eq'

    def __call__(self, *args):
        return reduce(lambda x, y: x and y, args)


class Gt(Function):

    class Meta:
        name = 'gt'

    def __call__(self, x, y):
        return x > y


class Gte(Function):

    class Meta:
        name = 'gte'

    def __call__(self, x, y):
        return x >= y


class Lt(Function):

    class Meta:
        name = 'lt'

    def __call__(self, x, y):
        return x < y


class Lte(Function):

    class Meta:
        name = 'lte'

    def __call__(self, x, y):

        return x <= y
