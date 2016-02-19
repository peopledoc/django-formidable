# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django import forms

from formidable.forms.validations import functions
from formidable.forms.validations.interpreter import Interpreter


class ValidationFunctionTest(TestCase):

    def test_is_empty(self):
        func = functions.IsEmpty()
        self.assertTrue(func(None))
        self.assertTrue(func(''))
        self.assertTrue(func(False))
        self.assertTrue(func(0))
        self.assertTrue(func(""))
        self.assertFalse(func("tutu"))
        self.assertFalse(func(True))
        self.assertFalse(func(1))

    def test_add(self):
        func = functions.Add()
        self.assertEquals(func(21, 21), 42)
        self.assertEquals(func(10, 11), 21)

    def test_sub(self):
        func = functions.Sub()
        self.assertEquals(func(21, 11), 10)
        self.assertEquals(func(11, 21), -10)
        self.assertEquals(func(0, 0), 0)

    def test_mult(self):
        func = functions.Mult()
        self.assertEquals(func(6, 7), 42)
        self.assertEquals(func(0, 0), 0)

    def test_div(self):
        func = functions.Div()
        self.assertEquals(func(42, 7), 6)
        self.assertRaises(ZeroDivisionError, func, 42, 0)

    def test_eq(self):
        func = functions.Eq()
        self.assertTrue(func(12, 12))
        self.assertFalse(func(12, 10))

    def test_not(self):
        func = functions.Not()
        self.assertTrue(func(False))
        self.assertFalse(func(True))

    def test_gt(self):
        func = functions.Gt()
        self.assertTrue(func(7, 5))
        self.assertFalse(func(5, 7))
        self.assertFalse(func(5, 5))

    def test_gte(self):
        func = functions.Gte()
        self.assertTrue(func(7, 5))
        self.assertFalse(func(5, 7))
        self.assertTrue(func(5, 5))

    def test_lt(self):
        func = functions.Lt()
        self.assertFalse(func(7, 5))
        self.assertTrue(func(5, 7))
        self.assertFalse(func(5, 5))

    def test_lte(self):
        func = functions.Lte()
        self.assertFalse(func(7, 5))
        self.assertTrue(func(5, 7))
        self.assertTrue(func(5, 5))


class TestForm(forms.Form):

    name = forms.CharField(required=False)
    has_children = forms.BooleanField(required=False)
    number_children = forms.IntegerField(required=False)


class TestInterpreter(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.form = TestForm(data={
            'name': 'Anakin', 'has_children': True, 'number_children': 2
        })
        self.assertTrue(self.form.is_valid())
        self.interpreter = Interpreter(self.form.cleaned_data)

    def test_bool(self):
        ast = {
            'node': 'boolean',
            'value': 'True',
        }
        self.assertTrue(self.interpreter(ast))
        ast['value'] = 'false'
        self.assertFalse(self.interpreter(ast))

    def test_int(self):
        ast = {
            'node': 'integer',
            'value': '21',
        }
        self.assertEquals(self.interpreter(ast), 21)

    def test_string(self):
        ast = {
            'node': 'string',
            'value': 'Intërnasì©lÍzation',
        }
        self.assertEquals(self.interpreter(ast), 'Intërnasì©lÍzation')

    def test_access_field(self):
        ast = {
            'field_id': 'name',
            'node': 'field'
        }
        self.assertEquals(self.interpreter(ast), 'Anakin')

    def test_simple_function(self):
        ast = {
            'node': 'function',
            'function': 'is_empty',
            'params': [{
                'node': 'string',
                'value': ''
            }]
        }
        self.assertTrue(self.interpreter(ast))
        ast = {
            'node': 'function',
            'function': 'is_empty',
            'params': [{
                'node': 'string',
                'value': 'Tutu'
            }]
        }
        self.assertFalse(self.interpreter(ast))

    def test_function_with_field(self):
        ast = {
            'node': 'function',
            'function': 'is_empty',
            'params': [{
                'node': 'field',
                'field_id': 'name'
            }]
        }
        self.assertFalse(self.interpreter(ast))
        form = TestForm(data={'name': ''})
        self.assertTrue(form.is_valid())
        interpreter = Interpreter(form.cleaned_data)
        self.assertTrue(interpreter(ast))

    def test_comparison(self):
        ast = {
            'node': 'comparison',
            'comparison': 'eq',
            'params': [{
                'node': 'boolean',
                'value': 'False'
            }, {
                'node': 'function',
                'function': 'is_empty',
                'params': [{
                    'node': 'field',
                    'field_id': 'name'
                }]
            }]
        }

        self.assertTrue(self.interpreter(ast))

    def test_and_bool(self):
        ast = {
            'node': 'and_bool',
            'params': [{
                'node': 'boolean',
                'value': 'True',
            }, {
                'node': 'boolean',
                'value': 'True'
            }]
        }
        self.assertTrue(self.interpreter(ast))
        ast['params'][0]['value'] = 'False'
        self.assertFalse(self.interpreter(ast))

    def test_or_bool(self):
        ast = {
            'node': 'or_bool',
            'params': [{
                'node': 'boolean',
                'value': 'True'
            }, {
                'node': 'boolean',
                'value': 'True'
            }]
        }
        self.assertTrue(self.interpreter(ast))
        ast['params'][0]['value'] = 'False'
        self.assertTrue(self.interpreter(ast))
        ast['params'][1]['value'] = 'False'
        self.assertFalse(self.interpreter(ast))

    def test_if_then_else(self):
        # if the value of the field "has_children" is True,
        # Check the value of "number_children" exists and > 0
        # Else, the value of "number_children" does not Exist or equals to 0
        ast = {
            'node': 'if',
            'condition': {
                'node': 'comparison',
                'comparison': 'eq',
                'params': [{
                    'node': 'field',
                    'field_id': 'has_children'
                }, {
                    'node': 'boolean',
                    'value': 'True'
                }],
            },
            'then': {
                'node': 'and_bool',
                'params': [{
                    'node': 'comparison',
                    'comparison': 'eq',
                    'params': [{
                        'node': 'function',
                        'function': 'is_empty',
                        'params': [{
                            'node': 'field',
                            'field_id': 'number_children',
                        }]
                    }, {
                        'node': 'boolean',
                        'value': 'False',
                    }]
                }, {
                    'node': 'comparison',
                    'comparison': 'gt',
                    'params': [{
                        'node': 'field',
                        'field_id': 'number_children'
                    }, {
                        'node': 'integer',
                        'value': '0'
                    }]
                }]
            },
        }

        self.assertTrue(self.interpreter(ast))
        # check "has_children" but do not fill "number_children"
        form = TestForm(data={
            'name': 'Anakin', 'has_children': True,
        })
        self.assertTrue(form.is_valid())
        interpreter = Interpreter(form.cleaned_data)
        self.assertFalse(interpreter(ast))
        # check "has_children" but fill children_number with 0
        form = TestForm(data={
            'name': 'Anakin', 'has_children': True, 'number_children': 0
        })
        self.assertTrue(form.is_valid())
        interpreter = Interpreter(form.cleaned_data)
        self.assertFalse(interpreter(ast))
        # Do not check children_number
        form = TestForm(data={
            'name': 'Anakin', 'has_children': False,
        })
        self.assertTrue(form.is_valid())
        interpreter = Interpreter(form.cleaned_data)
        self.assertTrue(interpreter(ast))
