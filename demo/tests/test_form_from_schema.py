# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms
from freezegun import freeze_time

from formidable.constants import REQUIRED
from formidable.forms import (
    FormidableForm, fields, get_dynamic_form_class_from_schema
)
from formidable.forms import widgets
from formidable.forms.validations.presets import (
    ConfirmationPresets
)
from formidable.models import PresetArg
from formidable.validators import (
    GTEValidator, MinLengthValidator, AgeAboveValidator
)
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

    def test_dropdown_field(self):
        class WithDropdown(FormidableForm):
            weapon = fields.ChoiceField(
                widget=widgets.Select,
                choices=(('gun', 'Eagles'), ('sword', 'Excalibur'))
            )

        formidable = WithDropdown.to_formidable(label='dropdown')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('weapon', form.fields)
        self.assertEqual(type(form.fields['weapon']), forms.ChoiceField)
        self.assertEqual(type(form.fields['weapon'].widget), forms.Select)
        self.assertIn(('gun', 'Eagles'), form.fields['weapon'].choices)
        self.assertIn(('sword', 'Excalibur'), form.fields['weapon'].choices)

    def test_dropdown_multiple(self):
        class WithDropdown(FormidableForm):
            weapon = fields.ChoiceField(
                widget=widgets.SelectMultiple,
                choices=(('gun', 'Eagles'), ('sword', 'Excalibur'))
            )

        formidable = WithDropdown.to_formidable(label='dropdown')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form = get_dynamic_form_class_from_schema(schema)()
        self.assertIn('weapon', form.fields)
        self.assertEqual(
            type(form.fields['weapon']), forms.MultipleChoiceField
        )
        self.assertEqual(
            type(form.fields['weapon'].widget), forms.SelectMultiple
        )
        self.assertIn(('gun', 'Eagles'), form.fields['weapon'].choices)
        self.assertIn(('sword', 'Excalibur'), form.fields['weapon'].choices)

    @freeze_time('2021-01-01')
    def test_date_field_with_validation(self):
        class TestdateField(FormidableForm):
            """ Test date """
            date = fields.DateField(validators=[AgeAboveValidator(21)])

        formidable = TestdateField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class(data={'date': '1990-01-01'})
        self.assertIn('date', form.fields)
        date = form.fields['date']
        self.assertEqual(type(date), forms.DateField)
        self.assertTrue(form.is_valid())

        form = form_class(data={'date': '2015-01-01'})
        self.assertFalse(form.is_valid())

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

    def test_with_presets(self):

        class FormWithPresets(FormidableForm):

            class Meta:
                presets = [
                    ConfirmationPresets([
                        PresetArg(slug='left', field_id='email'),
                        PresetArg(slug='right', field_id='email_confirm')
                    ])
                ]

            email = fields.EmailField()
            email_confirm = fields.EmailField()

        formidable = FormWithPresets.to_formidable(label='validation')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class(data={
            'email': 'test@test.tld', 'email_confirm': 'toto@test.tld'
        })
        self.assertFalse(form.is_valid())
        form = form_class(data={
            'email': 'test@test.tld', 'email_confirm': 'test@test.tld'
        })
        self.assertTrue(form.is_valid())
