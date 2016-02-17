# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django import forms

from formidable.forms.validations.interpreter import Interpreter


class TestForm(forms.Form):

    name = forms.CharField()


class TestInterpreter(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.form = TestForm(data={'name': 'Obiwan'})
        self.assertTrue(self.form.is_valid())
        self.cleaned_data = self.form.cleaned_data

    def test_bool(self):
        ast = {
            'node': 'boolean',
            'value': 'True',
        }
        self.assertTrue(Interpreter(self.cleaned_data)(ast))
        ast['value'] = 'false'
        self.assertFalse(Interpreter(self.cleaned_data)(ast))

    def test_int(self):
        ast = {
            'node': 'integer',
            'value': '21',
        }
        self.assertEquals(Interpreter(self.cleaned_data)(ast), 21)

    def test_string(self):
        ast = {
            'node': 'string',
            'value': 'Intërnasì©lÍzation',
        }
        interpreter = Interpreter(self.cleaned_data)
        self.assertEquals(interpreter(ast), 'Intërnasì©lÍzation')

    def test_access_field(self):
        ast = {
            'field_id': 'name',
            'node': 'field'
        }
        interpreter = Interpreter(self.cleaned_data)
        self.assertEquals(interpreter(ast), 'Obiwan')
