# -*- coding: utf-8 -*-

from six import with_metaclass

from formidable.utils import singleton
from formidable.forms.validations.functions import FunctionRegister


func_register = FunctionRegister.get_instance()


class Routeur(dict, singleton):

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
            mapper.add(klass)
        return klass


class Interpreter(with_metaclass(InterpreterMetaClass)):
    """
    """

    node = None

    def __init__(self, cleaned_data):
        self.form_data = cleaned_data
        self.routeur = Routeur.get_instance()

    def __call__(self, ast):
        return self.route(ast)

    def route(self, ast):
        """
        Look at the substree ``ast`` and interpret it with the rigth
        node visitor.
        """
        subinterpreter_klass = self.routeur.route(ast)
        subinterpreter = subinterpreter_klass(self.form_data)
        return subinterpreter(ast)


class AndBoolInterpreter(Interpreter):

    node = 'and_bool'

    def __call__(self, ast):
        lhs = self.route(ast['lhs'])
        rhs = self.route(ast['rhs'])

        return lhs and rhs


class ComparisonInterpreter(Interpreter):

    node = 'comparison'

    def __call__(self, ast):
        function_list = [self.route(node) for node in ast['params']]
        function_name = ast['comparison']
        comparison = func_register[function_name]()
        return comparison(*function_list)


class FunctionInterpreter(Interpreter):

    node = 'function'

    def __call__(self, ast):
        args_list = [self.route(node) for node in ast['params']]
        function_name = ast['function']
        function = func_register[function_name]()
        return function(*args_list)


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
