# -*- coding: utf-8 -*-

from six import with_metaclass


class Routeur(dict):

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def add(self, klass):
        self[klass.node] = klass

    def route(self, ast):
        return self[ast['node']]


class InterpreterMetaClass(type):

    def __new__(cls, name, bases, attrs):

        klass = super(InterpreterMetaClass, cls).__new__(
                cls, name, bases, attrs
                )
        mapper = Routeur.get_instance()
        if klass.node:
            mapper[klass.node] = klass
        return klass


class Interpreter(with_metaclass(InterpreterMetaClass)):

    node = None

    def __init__(self, cleaned_data):
        self.form_data = cleaned_data
        self.routeur = Routeur.get_instance()

    def __call__(self, ast):
        return self.route(ast)

    def route(self, ast):
        subinterpreter_klass = self.routeur.route(ast)
        subinterpreter = subinterpreter_klass(self.form_data)
        return subinterpreter(ast)


class BooleanIntepreter(Interpreter):

    node = 'boolean'

    def __call__(self, ast):
        return ast['value'].lower() == 'true'


class IntegerInterpreter(Interpreter):

    node = 'integer'

    def __call__(self, ast):
        return int(ast['value'])


class StringInterpreter(Interpreter):

    node = 'string'

    def __call__(self, ast):
        return ast['value']


class FieldInterpreter(Interpreter):

    node = 'field'

    def __call__(self, ast):
        slug = ast['field_id']
        return self.form_data[slug]
