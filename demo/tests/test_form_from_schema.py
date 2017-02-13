# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms

from formidable.constants import REQUIRED
from formidable.forms import (
    FormidableForm, fields, get_dynamic_form_class_from_schema
)
from formidable.forms import widgets
from formidable.validators import (GTEValidator, MinLengthValidator)
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

    def test_checkbox_field(self):
        class TestCheckBoxField(FormidableForm):
            """ Test checkbox """
            checkbox = fields.BooleanField()

        formidable = TestCheckBoxField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('checkbox', form.fields)
        checkbox = form.fields['checkbox']
        self.assertEqual(type(checkbox), forms.BooleanField)

    def test_email_field(self):
        class TestemailField(FormidableForm):
            """ Test email """
            email = fields.EmailField()

        formidable = TestemailField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('email', form.fields)
        email = form.fields['email']
        self.assertEqual(type(email), forms.EmailField)

    def test_integer_field(self):
        class TestintegerField(FormidableForm):
            """ Test integer """
            integer = fields.IntegerField()

        formidable = TestintegerField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('integer', form.fields)
        integer = form.fields['integer']
        self.assertEqual(type(integer), forms.IntegerField)

    def test_file_field(self):
        class TestfileField(FormidableForm):
            """ Test file """
            file_ = fields.FileField()

        formidable = TestfileField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('file_', form.fields)
        file_ = form.fields['file_']
        self.assertEqual(type(file_), forms.FileField)

    def test_date_field(self):
        class TestdateField(FormidableForm):
            """ Test date """
            date = fields.DateField()

        formidable = TestdateField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('date', form.fields)
        date = form.fields['date']
        self.assertEqual(type(date), forms.DateField)

    def test_with_validations(self):
        class FormWithValidations(FormidableForm):
            text = fields.CharField(validators=[MinLengthValidator(4)])
            integer = fields.IntegerField(validators=[GTEValidator(42)])

        formidable = FormWithValidations.to_formidable(label='validation')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class(data={'text': 'tut', 'integer': 21})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        form = form_class(data={'text': 'tutu', 'integer': 43})
        self.assertTrue(form.is_valid())
