# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms
from freezegun import freeze_time

from formidable.constants import REQUIRED
from formidable.forms import (
    FormidableForm, fields, get_dynamic_form_class_from_schema
)
from formidable.forms import (
    field_builder, field_builder_from_schema, widgets
)
from formidable.forms.validations.presets import (
    ConfirmationPresets
)
from formidable.models import PresetArg
from formidable.serializers.forms import contextualize
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
        self.assertIn('paragraph', form.fields)
        charfield = form.fields['paragraph']
        self.assertEqual(type(charfield), forms.CharField)
        self.assertEqual(type(charfield.widget), forms.Textarea)
        self.assertFalse(charfield.required)

    def test_help_text(self):
        class TestHelpTextField(FormidableForm):
            """
            Test help text

            """
            helptext = fields.HelpTextField(text='My Help Text')

        formidable = TestHelpTextField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('helptext', form.fields)
        helptext = form.fields['helptext']
        self.assertEqual(type(helptext), fields.HelpTextField)
        self.assertEqual(type(helptext.widget), widgets.HelpTextWidget)
        self.assertFalse(helptext.required)

    def test_help_text_label(self):
        class TestHelpTextField(FormidableForm):
            """
            Test help text

            """
            helptext = fields.HelpTextField(text='My Help Text')

        formidable = TestHelpTextField.to_formidable(label='label')
        schema = contextualize(formidable.to_json(), 'jedi')

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('helptext', form.fields)
        helptext = form.fields['helptext']
        self.assertEqual(type(helptext), fields.HelpTextField)
        self.assertEqual(type(helptext.widget), widgets.HelpTextWidget)
        self.assertFalse(helptext.required)
        self.assertIsNone(helptext.label)

    def test_separator(self):
        class TestSeparatorField(FormidableForm):
            """
            Test for separator

            """
            separator = fields.SeparatorField()

        formidable = TestSeparatorField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('separator', form.fields)
        separator = form.fields['separator']
        self.assertEqual(type(separator), fields.SeparatorField)
        self.assertEqual(type(separator.widget), widgets.SeparatorWidget)
        self.assertFalse(separator.required)

    def test_title(self):
        class TestTitleField(FormidableForm):
            """
            Test for separator

            """
            title = fields.TitleField()

        formidable = TestTitleField.to_formidable(label='label')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('title', form.fields)
        title = form.fields['title']
        self.assertEqual(type(title), fields.TitleField)
        self.assertEqual(type(title.widget), widgets.TitleWidget)
        self.assertFalse(title.required)

    def test_checkbox_field(self):
        class TestCheckBoxField(FormidableForm):
            """ Test checkbox """
            checkbox = fields.BooleanField()

        formidable = TestCheckBoxField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
        self.assertIn('email', form.fields)
        email = form.fields['email']
        self.assertEqual(type(email), forms.EmailField)

    def test_integer_field(self):
        class TestintegerField(FormidableForm):
            """ Test integer """
            integer = fields.NumberField()

        formidable = TestintegerField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
        self.assertIn('integer', form.fields)
        integer = form.fields['integer']
        self.assertEqual(type(integer), forms.DecimalField)

    def test_file_field(self):
        class TestfileField(FormidableForm):
            """ Test file """
            file_ = fields.FileField()

        formidable = TestfileField.to_formidable(label='label')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
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

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()
        self.assertIn('weapon', form.fields)
        self.assertEqual(
            type(form.fields['weapon']), forms.MultipleChoiceField
        )
        self.assertEqual(
            type(form.fields['weapon'].widget), forms.SelectMultiple
        )
        self.assertIn(('gun', 'Eagles'), form.fields['weapon'].choices)
        self.assertIn(('sword', 'Excalibur'), form.fields['weapon'].choices)

    def test_radio_field(self):
        class TestRadioField(FormidableForm):
            radioinput = fields.ChoiceField(
                widget=widgets.RadioSelect,
                choices=(('yes', 'Yes'), ('no', 'No')),
            )

        formidable = TestRadioField.to_formidable(label='form-with-radio')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('radioinput', form.fields)
        self.assertEqual(
            type(form.fields['radioinput']), forms.ChoiceField
        )
        self.assertEqual(
            type(form.fields['radioinput'].widget), forms.RadioSelect
        )
        self.assertIn(('yes', 'Yes'), form.fields['radioinput'].choices)
        self.assertIn(('no', 'No'), form.fields['radioinput'].choices)

    def test_checkbox_multiple_field(self):

        choices = (
            ('BELGIUM', 'Chouffe'), ('GERMANY', 'Paulaner'),
            ('FRANCE', 'Antidote')
        )

        class TestCheckboxesField(FormidableForm):

            checkboxesinput = fields.MultipleChoiceField(
                widget=widgets.CheckboxSelectMultiple,
                choices=choices,
            )

        formidable = TestCheckboxesField.to_formidable(label='checkboxes')
        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data

        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class()

        self.assertIn('checkboxesinput', form.fields)

        checkboxes = form.fields['checkboxesinput']

        self.assertEqual(type(checkboxes), forms.MultipleChoiceField)
        self.assertEqual(type(checkboxes.widget), forms.CheckboxSelectMultiple)
        self.assertIn(('BELGIUM', 'Chouffe'), checkboxes.choices)
        self.assertIn(('FRANCE', 'Antidote'), checkboxes.choices)
        self.assertIn(('GERMANY', 'Paulaner'), checkboxes.choices)

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
            integer = fields.NumberField(validators=[GTEValidator(42.4)])

        formidable = FormWithValidations.to_formidable(label='validation')

        schema = ContextFormSerializer(instance=formidable, context={
            'role': 'jedi'
        }).data
        form_class = get_dynamic_form_class_from_schema(schema)
        form = form_class(data={'text': 'tut', 'integer': 21.0})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        form = form_class(data={'text': 'tutu', 'integer': 43.2})
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

    def test_mapping(self):
        """
        Simple test to make sure that every widget is implemented.

        """
        self.assertEqual(
            set(field_builder.FormFieldFactory.field_map),
            set(field_builder_from_schema.FormFieldFactory.field_map)
        )
