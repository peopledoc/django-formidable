# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms

from formidable.constants import REQUIRED
from formidable.forms import (
    FormidableForm, fields, get_dynamic_form_class_from_schema
)
from formidable.forms import widgets
from formidable.serializers.forms import ContextFormSerializer


class TestFormFromSchema(TestCase):

    def test_charfield(self):
        class TestCharField(FormidableForm):
            """ Test charfield """
            charfield = fields.CharField()

        formidable = TestCharField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('charfield', form.fields)
        charfield = form.fields['charfield']
        self.assertEqual(type(charfield), forms.CharField)
        self.assertFalse(charfield.required)

    def test_required_charfield(self):
        class TestCharField(FormidableForm):
            """ Test charfield """
            charfield = fields.CharField(accesses={'jedi': REQUIRED})

        formidable = TestCharField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('charfield', form.fields)
        charfield = form.fields['charfield']
        self.assertEqual(type(charfield), forms.CharField)
        self.assertTrue(charfield.required)

    def test_paragraph_field(self):
        class TestParagraphField(FormidableForm):
            """ Test Paraprah """
            paragraph = fields.CharField(widget=widgets.Textarea)

        formidable = TestParagraphField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('paragraph', form.fields)
        charfield = form.fields['paragraph']
        self.assertEqual(type(charfield), forms.CharField)
        self.assertEqual(type(charfield.widget), forms.Textarea)
        self.assertFalse(charfield.required)
