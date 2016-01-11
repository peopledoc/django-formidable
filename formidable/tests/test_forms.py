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
        self.text_field.accesses.create(access_id=u'padawan',
                                        level=u'REQUIRED')
        self.text_field.accesses.create(access_id=u'jedi',
                                        level=u'EDITABLE')
        self.text_field.accesses.create(access_id=u'human',
                                        level=u'HIDDEN')

    def test_text_input(self):
        form_class = self.form.get_django_form_class(role=u'padawan')
        form = form_class()
        self.assertIn('text-input', form.fields)
        text = form.fields['text-input']
        self.assertEquals(text.required, True)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.TextInput)

    def test_paragraph_input(self):
        paragraph = self.form.fields.create(
            slug=u'area-input', type_id=u'paragraph', label=u'type a msg'
        )
        paragraph.accesses.create(access_id=u'padawan', level=u'EDITABLE')
        form_class = self.form.get_django_form_class(role=u'padawan')
        form = form_class()
        self.assertIn('area-input', form.fields)
        text = form.fields['area-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.Textarea)

    def test_hidden_field(self):
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertNotIn('text-input', form.fields)
