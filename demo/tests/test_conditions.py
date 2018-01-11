# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json

from django.test import TestCase


from formidable import constants

from formidable.forms import (
    FormidableForm, fields, get_dynamic_form_class,
    get_dynamic_form_class_from_schema
)
from formidable.serializers.forms import (
    ContextFormSerializer, FormidableSerializer, contextualize
)

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class ConditionTestCase(TestCase):

    def get_form_class(self, formidable, role):
        return get_dynamic_form_class(formidable, role)

    @classmethod
    def setUpTestData(cls):
        cls.conditions_schema = json.load(open(
            os.path.join(
                TESTS_DIR, 'fixtures', 'wrong-conditions.json'
            )
        ))

    def setUp(self):
        conditions_schema = [
            {
                'name': 'My Name',
                'action': 'display_iff',
                'fields_ids': ['foo', 'bar'],
                'tests': [
                    {
                        'field_id': 'checkbox',
                        'operator': 'eq',
                        'values': [False],
                    }
                ]
            }
        ]

        class TestForm(FormidableForm):
            checkbox = fields.BooleanField(
                label='My checkbox',
                accesses={'padawan': constants.EDITABLE,
                          'jedi': constants.EDITABLE,
                          'human': constants.EDITABLE,
                          'robot': constants.REQUIRED}
            )
            foo = fields.CharField(
                label='Foo',
                accesses={'padawan': constants.EDITABLE,
                          'jedi': constants.REQUIRED,
                          'human': constants.REQUIRED,
                          'robot': constants.REQUIRED}
            )
            bar = fields.CharField(
                label='Bar',
                accesses={'padawan': constants.EDITABLE,
                          'jedi': constants.REQUIRED,
                          'human': constants.READONLY,
                          'robot': constants.REQUIRED}
            )

        self.formidable = TestForm.to_formidable(label='title')
        self.formidable.conditions = conditions_schema

    def test_jedi_displayed(self):
        form_class = self.get_form_class(self.formidable, 'jedi')
        data = {
            'foo': 'fooval',
            'checkbox': False,
        }

        form = form_class(data)
        self.assertFalse(form.is_valid())
        self.assertIn('bar', form.errors)

    def test_jedi_not_displayed(self):
        form_class = self.get_form_class(self.formidable, 'jedi')
        data = {
            'foo': 'fooval',
            'checkbox': True,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {'checkbox': True})
        self.assertTrue('bar' not in form.fields)

    def test_padawan_displayed(self):
        form_class = self.get_form_class(self.formidable, 'padawan')
        data = {
            'foo': 'fooval',
            'checkbox': False,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data,
                         {'checkbox': False, 'foo': 'fooval', 'bar': ''})

    def test_padawan_not_displayed(self):
        form_class = self.get_form_class(self.formidable, 'padawan')
        data = {
            'foo': 'fooval',
            'checkbox': True,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {'checkbox': True})
        self.assertTrue('bar' not in form.fields)

    def test_save_update(self):
        self.formidable.save()
        pk = self.formidable.pk
        self.assertEqual(self.formidable.conditions[0]['name'], 'My Name')
        # update
        self.formidable.conditions[0]['name'] = 'New Name'
        self.formidable.save()
        self.assertEqual(pk, self.formidable.pk)
        self.assertEqual(self.formidable.conditions[0]['name'], 'New Name')

    def test_no_checkbox_when_editable(self):
        form_class = self.get_form_class(self.formidable, 'jedi')
        data = {
            'foo': 'fooval',
        }

        form = form_class(data)
        # checkbox is not required, so default value (False) is present in
        # cleaned_data
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('bar', form.errors)

    def test_no_checkbox_when_required(self):
        form_class = self.get_form_class(self.formidable, 'robot')
        data = {
            'foo': 'fooval',
        }

        form = form_class(data)
        # checkbox is required, so we'll get an error on this field and there
        # won't be an entry for it in self.cleaned_data
        # As `checkbox` is missing, the conditional fields must be filtered out
        # from the result
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('checkbox', form.errors)
        self.assertNotIn('bar', form.errors)

    def test_readonly_field_displayed(self):
        form_class = self.get_form_class(self.formidable, 'human')
        data = {
            'foo': 'fooval',
            'bar': 'readonly',
            'checkbox': False,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, data)

    def test_readonly_field_displayed_and_missing(self):
        form_class = self.get_form_class(self.formidable, 'human')
        data = {
            'foo': 'fooval',
            'checkbox': False,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data,
            {
                'foo': 'fooval',
                'checkbox': False,
                'bar': '',  # default value
            }
        )

    def test_readonly_field_not_displayed(self):
        form_class = self.get_form_class(self.formidable, 'human')
        data = {
            'foo': 'fooval',
            'bar': 'readonly',
            'checkbox': True,
        }

        form = form_class(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, {'checkbox': True})

    def test_condition_field_doesnt_exist(self):
        """
        This test checks situation when the conditional fields don't exists
        in the list of fields.
        it shows that we don't raise an Exception anymore.

        You could get this situation when you specified the fields access
        that current user doesn't have an access to the conditional field.

        In the fixture 'wrong-conditions.json' you see this situation.
        Conditions are configured for the 'test-field' but current user
        doesn't have rights to read or write to it. So can't see this field
        in the 'fields' section.
        """

        try:
            get_dynamic_form_class_from_schema(self.conditions_schema)
        except KeyError:
            self.fail("Doesn't have to raise an exception here ")
        else:
            self.assertTrue(True)

    def test_filter_conditions_by_fields_ids(self):
        first_schema = contextualize(self.conditions_schema, 'TEST_ROLE')
        conditions = first_schema['conditions']
        self.assertEqual(len(conditions), 1)
        condition = conditions[0]

        self.assertEqual(condition['fields_ids'], ['first-field'])

        second_schema = contextualize(self.conditions_schema, 'TEST_ROLE2')
        conditions = second_schema['conditions']
        self.assertEqual(len(conditions), 1)
        condition = conditions[0]
        self.assertEqual(
            sorted(condition['fields_ids']),
            ['first-field', 'second-field']
        )


class ConditionFromSchemaTestCase(ConditionTestCase):

    def get_form_class(self, formidable, role):
        serializer = ContextFormSerializer(instance=formidable,
                                           context={'role': role})
        schema = serializer.data
        return get_dynamic_form_class_from_schema(schema)


class ConditionSerializerTestCase(TestCase):

    payload = {
        'label': 'My label',
        'description': 'My description',
        'fields': [
            {
                'slug': 'checkbox',
                'label': 'My checkbox',
                'type_id': 'checkbox',
                'accesses': [],
            },
            {
                'slug': 'foo',
                'label': 'Foo',
                'type_id': 'text',
                'accesses': [],
            },
            {
                'slug': 'bar',
                'label': 'Bar',
                'type_id': 'text',
                'accesses': [],
            },
        ],
        'conditions': [
            {
                'name': 'My Name',
                'action': 'display_iff',
                'fields_ids': ['foo', 'bar'],
                'tests': [
                    {
                        'field_id': 'checkbox',
                        'operator': 'eq',
                        'values': [True],
                    }
                ]
            }
        ]
    }

    def test_serializer(self):
        serializer = FormidableSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.conditions, self.payload['conditions'])
