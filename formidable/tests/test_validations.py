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


class TestInterpreter(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.form = TestForm(data={'name': 'Obiwan'})
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
        self.assertEquals(self.interpreter(ast), 'Obiwan')

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
            'lhs': {
                'node': 'boolean',
                'value': 'True',
            },
            'rhs': {
                'node': 'boolean',
                'value': 'True'
            }
        }
        self.assertTrue(self.interpreter(ast))
        ast['lhs']['value'] = 'False'
        self.assertFalse(self.interpreter(ast))
