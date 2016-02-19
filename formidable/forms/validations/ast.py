# -*- coding: utf-8 -*-


class ASTNode(object):

    class Meta:
        node = None
        attributes = []

    def to_dict(self):
        res = {'node': self.Meta.node}
        for attr_name in self.Meta.attributes:
            try:
                meth_name = self.Meta.methods[attr_name]
            except (KeyError, AttributeError):
                attr = getattr(self, attr_name, None)
            else:
                attr = getattr(self, meth_name)()

            if attr:
                res[attr_name] = attr.to_dict() if hasattr(attr, 'to_dict') \
                        else attr
        return res


class IfNode(ASTNode):

    class Meta:
        node = 'if'
        attributes = ('condition', 'then', 'else')
        methods = {'else': 'get_else'}

    def __init__(self, condition, then, else_=None):
        self.condition = condition
        self.then = then
        self.else_ = else_

    def get_else(self):
        return self.else_


class FunctionNode(ASTNode):

    class Meta:
        node = 'function'
        attributes = ('function', 'params')
        methods = {'params': 'get_params'}

    def __init__(self, function, params):
        self.function = function
        self.params = params

    def get_params(self):
        return [elt.to_dict() for elt in self.params]


class IntegerNode(ASTNode):

    class Meta:
        node = 'integer'
        attributes = ('value',)

    def __init__(self, value):
        self.value = value


class BooleanNode(ASTNode):

    class Meta:
        node = 'boolean'
        attributes = ('value',)

    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):

    class Meta:
        node = 'string'
        attributes = ('value',)

    def __init__(self, value):
        self.value = value


class FieldNode(ASTNode):

    class Meta:
        node = 'field'
        attributes = ('field_id',)

    def __init__(self, field_id):
        self.field_id = field_id
