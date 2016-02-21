# -*- coding: utf-8 -*-

from formidable.forms.validations.functions import Eq, Gt, IsEmpty
from formidable.forms.validations.ast import FieldNode as Field, StringNode
from formidable.forms.validations.ast import IfNode
from formadible.forms.validations import ast


class PreceptTemplate(object):

    def __init__(self, ast_template):
        self.ast_template = ast_template


class Template(object):

    def __init__(self, klass, slug):
        self.slug = slug
        self.klass = klass

    def to_dict(self, **kwargs):
        args = kwargs[self.slug]
        return self.klass(args).to_dict()


class Confirmation(PreceptTemplate):

    source = Eq(
        Template(Field, slug='tutu'), Template(StringNode, slug='toto')
    )

    def to_dict(self, tutu, toto):
        return self.source.to_dict(tutu=tutu, toto=toto)


class If(PreceptTemplate):
    source = IfNode(
        # Condition, If the field is checked
        Eq(ast.BooleanNode("True"), Template(Field, slug='conditional')),
        # Then, the "to_check" is not empty and the value is greater than 0
        ast.AndNode(
            Eq(
                IsEmpty(Template(Field, slug='to_check')),
                ast.BooleanNode("False")
            ),
            Gt(Template(Field, slug='to_check'), ast.IntegerNode("0"))
        )
    )
