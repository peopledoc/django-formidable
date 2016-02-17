# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django import forms

from formidable.forms.validations.interpreter import Interpreter


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
