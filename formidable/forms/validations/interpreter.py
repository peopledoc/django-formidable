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


class IfInterpreter(Interpreter):

    node = 'if'

    def __call__(self, ast):
        condition = self.route(ast['bool_expr'])
        if condition:
            return self.route(ast['then'])
        subast = ast.get('else')
        return self.route(subast) if subast else True


class OrBoolInterpreter(Interpreter):

    node = 'or_bool'

    def __call__(self, ast):
        params = [self.route(node) for node in ast['params']]
        return reduce(lambda x, y: x or y, params)


class AndBoolInterpreter(Interpreter):

    node = 'and_bool'

    def __call__(self, ast):
        for node in ast['params']:
            if not self.route(node):
                return False
        return True


class IdentityInterpreter(Interpreter):

    node = 'identity'

    def __call__(self, ast):
        res = self.route(ast['or_bool'])
        func_name = ast.get('identity')
        if func_name:
            func = func_register[func_name]()
            res = func(res)
        return res


class ComparisonInterpreter(Interpreter):

    node = 'comparison'

    def __call__(self, ast):
        function_name = ast['comparison']
        comparison = func_register[function_name]()
        args = [self.route(node) for node in ast['params']]
        # Parser garantuee the return is always Boolean
        return comparison(*args)


class FunctionInterpreter(Interpreter):

    node = 'function'

    def __call__(self, ast):
        function_name = ast['function']
        function = func_register[function_name]()
        args_list = [self.route(node) for node in ast['params']]
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
