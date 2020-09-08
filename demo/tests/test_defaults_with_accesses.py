from django.test import TestCase
from formidable.forms import (
    FormidableForm, fields
)
from formidable import constants
from formidable.forms import get_dynamic_form_class


class AccessesTestCaseTestForm(FormidableForm):
    editable_text = fields.CharField(
        label='Editable text',
        accesses={'jedi': constants.EDITABLE},
        default='Default value (editable)'
    )
    readonly_text = fields.CharField(
        label='Readonly text',
        accesses={'jedi': constants.READONLY},
        default='Default value (readonly)'
    )
    readonly_dropdown = fields.MultipleChoiceField(
        label='Readonly dropdown',
        accesses={'jedi': constants.READONLY},
        defaults=['val1', 'val2'],
        choices=[
            ('val1', 'Default value 1 (readonly)'),
            ('val2', 'Default value 2 (readonly)'),
            ('val3', 'Value 3')]
    )
    hidden_field = fields.CharField(
        label='Hidden text',
        accesses={'jedi': constants.HIDDEN},
        default='Default value (hidden)'
    )


class AccessesTestCase(TestCase):

    def setUp(self):
        super().setUp()
        form_class = AccessesTestCaseTestForm
        self.formidable = form_class.to_formidable(label='title')

    def test_readonly_field_with_default_filled(self):
        form_class = get_dynamic_form_class(self.formidable, 'jedi')
        data = {
            'editable_text': 'Default value (editable)',
            'readonly_text': 'Default value (readonly)',
            'readonly_dropdown': ['val1', 'val2'],
            'hidden_text': 'Default value (hidden)'
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {
            'editable_text': 'Default value (editable)',
            'readonly_text': 'Default value (readonly)',
            'readonly_dropdown': ['val1', 'val2'],

        })

    def test_readonly_field_with_default_empty(self):
        form_class = get_dynamic_form_class(self.formidable, 'jedi')
        data = {
            'editable_text': '',
            'readonly_text': '',
            'readonly_dropdown': '',
            'hidden_text': ''
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {
            'editable_text': '',
            'readonly_dropdown': ['val1', 'val2'],
            'readonly_text': 'Default value (readonly)'
        })

    def test_readonly_field_with_default_filled_other(self):
        form_class = get_dynamic_form_class(self.formidable, 'jedi')
        data = {
            'editable_text': '',
            'readonly_text': 'Wrong value',
            'readonly_dropdown': ['wrong', 'value'],
            'hidden_text': 'Wrong value'
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {
            'editable_text': '',
            'readonly_dropdown': ['val1', 'val2'],
            'readonly_text': 'Default value (readonly)'
        })
