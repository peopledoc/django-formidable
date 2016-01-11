# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase

from formidable.models import Formidable


class TestDynamicForm(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(label=u'test',
                                              description=u'desc')
        self.text_field = self.form.fields.create(
            slug=u'text-input', type_id=u'text', label=u'mytext'
        )

    def test_text_input(self):
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('text-input', form.fields)
        text = form.fields['text-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.TextInput)

    def test_paragraph_input(self):
        self.form.fields.create(
            slug=u'area-input', type_id=u'paragraph', label=u'type a msg'
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('area-input', form.fields)
        text = form.fields['area-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.Textarea)

    def test_dropdown_input(self):
        drop = self.form.fields.create(
            slug=u'weapons', type_id=u'dropdown', label=u'chose you weapon'
        )
        for key in ['sword', 'gun']:
            drop.items.create(key=key, value=key)

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('weapons', form.fields)
        dropdown = form.fields['weapons']
        self.assertEquals(type(dropdown), forms.ChoiceField)
        self.assertEquals(type(dropdown.widget), forms.Select)
        self.assertTrue(dropdown.choices)
        self.assertEquals(len(dropdown.choices), 2)

    def test_radio_input(self):
        field = self.form.fields.create(
            slug=u'input-radio', type_id=u'checkbox',
            label=u'chose you weapon'
        )
        for key in ['sword', 'gun']:
            field.items.create(key=key, value=key)

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-radio', form.fields)
        checkbox = form.fields['input-radio']
        self.assertEquals(type(checkbox), forms.ChoiceField)
        self.assertEquals(type(checkbox.widget), forms.RadioSelect)
        self.assertTrue(checkbox.choices)
        self.assertEquals(len(checkbox.choices), 2)

    def test_hidden_field(self):
        self.text_field.accesses.create(access_id=u'human', level=u'HIDDEN')
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertNotIn('text-input', form.fields)
