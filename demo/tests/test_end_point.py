# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy
from functools import reduce

from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.test.utils import CaptureQueriesContext

import django_perf_rec

from formidable import constants
from formidable.forms import FormidableForm, fields
from formidable.json_migrations.utils import merge_context_forms
from formidable.models import Formidable
from formidable.serializers.fields import BASE_FIELDS, FieldSerializerRegister
from formidable.serializers.forms import (
    ContextFormSerializer, FormidableSerializer, contextualize
)

RENDER_BASE_FIELDS = list(set(BASE_FIELDS) - set(['order']))


class RenderSerializerTestCase(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(
            label='testform', description='test form',
        )
        self.text_field = self.form.fields.create(
            type_id='text', label='test text', slug='test_text',
            placeholder='put your name here', help_text='your name',
            order=self.form.get_next_field_order()
        )
        self.text_field2 = self.form.fields.create(
            type_id='text', label='test text 2', slug='test_text_2',
            placeholder='put your name here', help_text='your name',
            order=self.form.get_next_field_order()
        )
        self.text_field2.defaults.create(value='Roméo')
        self.text_field.accesses.create(
            level=constants.REQUIRED, access_id='padawan'
        )
        self.text_field2.accesses.create(
            level=constants.EDITABLE, access_id='jedi'
        )
        self.text_field.validations.create(
            type='MINLENGTH', value='5'
        )
        self.serializer = FormidableSerializer(instance=self.form)

    def test_ok(self):
        self.assertTrue(self.serializer.data)

    def test_register(self):
        register = FieldSerializerRegister.get_instance()
        assert len(register) == 14

    def test_render_in_order(self):
        self.text_field3 = self.form.fields.create(
            type_id='text', label='test text 2', slug='test_text_3',
            placeholder='put your name here', help_text='your name',
            order=self.form.get_next_field_order()
        )
        data = self.serializer.data
        ordered_slug = ['test_text', 'test_text_2', 'test_text_3']
        for index, field in enumerate(data['fields']):
            self.assertEqual(ordered_slug[index], field['slug'])

    def test_form_field(self):
        data = self.serializer.data
        self.assertIn('label', data)
        self.assertEquals(data['label'], 'testform')
        self.assertIn('description', data)
        self.assertEquals(data['description'], 'test form')
        self.assertEquals(data['id'], self.form.pk)

    def test_fields(self):
        data = self.serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 2)

    def test_base_field_for_fieldidable(self):
        field_text = self.serializer.data['fields'][0]
        for field in RENDER_BASE_FIELDS:
            self.assertIn(field, field_text)

    def test_text_field(self):
        data = self.serializer.data
        text_field = data['fields'][0]
        self.assertEquals(text_field['type_id'], 'text')
        self.assertEquals(text_field['label'], 'test text')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['description'], 'your name')
        self.assertEquals(text_field['defaults'], [])
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], 'padawan')
        self.assertEquals(accesses['level'], constants.REQUIRED)

    def test_text_field2(self):
        data = self.serializer.data
        text_field = data['fields'][1]
        self.assertEquals(text_field['type_id'], 'text')
        self.assertEquals(text_field['label'], 'test text 2')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['description'], 'your name')
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], 'jedi')
        self.assertEquals(accesses['level'], constants.EDITABLE)
        self.assertIn('defaults', text_field)
        defaults = text_field['defaults']
        self.assertEqual(type(defaults), list)
        self.assertEqual(len(defaults), 1)
        self.assertEqual(defaults[0], 'Roméo')

    def test_dropdown_field(self):
        self.form.fields.all().delete()
        self.dropdown = self.form.fields.create(
            type_id='dropdown', label='choose your weapon',
            order=self.form.get_next_field_order()
        )
        order = self.dropdown.get_next_order()
        self.dropdown.items.create(value='tutu', label='toto', order=order)
        self.dropdown.items.create(value='plop', label='Intérnätiônal',
                                   order=order + 1)
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in RENDER_BASE_FIELDS:
            self.assertIn(field, data)
        self.assertIn('multiple', data)
        self.assertEquals(data['multiple'], False)
        self.assertIn('items', data)
        self.assertEquals(len(data['items']), 2)

    def test_helptext_field(self):
        self.form.fields.all().delete()
        self.help_text = self.form.fields.create(
            type_id='help_text', slug='your help text',
            help_text='Please enter your information here',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in list(set(RENDER_BASE_FIELDS) - set(['label'])):
            self.assertIn(field, data)
        self.assertEqual(data['description'],
                         'Please enter your information here')

    def test_title_field(self):
        self.form.fields.all().delete()
        self.title = self.form.fields.create(
            type_id='title', slug='my title',
            label='This is on onboarding form.',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in set(RENDER_BASE_FIELDS) - set(['description']):
            self.assertIn(field, data)
        self.assertEqual(data['label'],
                         'This is on onboarding form.')
        self.assertNotIn('description', data)

    def test_email_field(self):
        self.form.fields.all().delete()
        self.email = self.form.fields.create(
            type_id='email', slug='email',
            label='Your email',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in RENDER_BASE_FIELDS:
            self.assertIn(field, data)

    def test_separator_field(self):
        self.form.fields.all().delete()
        self.sepa = self.form.fields.create(
            type_id='separator', slug='sepa',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        self.assertEqual(data['type_id'], 'separator')
        self.assertNotIn('label', data)
        self.assertNotIn('help_text', data)

    def test_queryset(self):
        class MyTestForm(FormidableForm):
            first_name = fields.CharField(default='foo')
            last_name = fields.CharField()
            origin = fields.ChoiceField(choices=(
                ('fr', 'France'),
                ('us', 'United States'),
            ))

        formidable = MyTestForm.to_formidable(label='test')
        serializer = FormidableSerializer(instance=formidable)
        # FIXME: Don't know if we still have to maintain this test
        # Could be a duplicate of another.
        with django_perf_rec.record(path='perfs/'):
            serializer.data


class MergeContextForms(TestCase):
    def check_jedi_and_padawan(self, form):
        """
        What we want to do is :
        FormidableJSON "F"
        ->
        'contextualized' into ContextFormJSONs (dict with role as key) "C"
        ->
        merged into a Formidable JSON "F'"
        ->
        'contextualized' into ContextFormJSONs "C'"

        We can't garanty that F == F' (ContextFormSerializer loses information)
        But what we really want to check is that C == C' (except for `id`s)
        """
        jedi_form = ContextFormSerializer(form,
                                          context={'role': 'jedi'}).data
        pdw_form = ContextFormSerializer(form,
                                         context={'role': 'padawan'}).data
        contextform_dict = {
            'jedi': jedi_form,
            'padawan': pdw_form,
        }
        base_form_json = merge_context_forms(contextform_dict)
        self.assertEqual(form.description, base_form_json['description'])
        self.assertEqual(form.label, base_form_json['label'])

        serializer = FormidableSerializer(data=base_form_json)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        jedi_form2 = ContextFormSerializer(instance,
                                           context={'role': 'jedi'}).data
        pdw_form2 = ContextFormSerializer(instance,
                                          context={'role': 'padawan'}).data
        self.assertEqual(jedi_form['fields'], jedi_form2['fields'])
        self.assertEqual(pdw_form['fields'], pdw_form2['fields'])

    def test_all_accesses(self):
        class TestForm(FormidableForm):
            field1 = fields.CharField(label='Field1', accesses={
                'jedi': constants.REQUIRED,
            })
            field2 = fields.CharField(label='Field2', accesses={
                'jedi': constants.HIDDEN,
            })
            field3 = fields.CharField(label='Field3', accesses={
                'jedi': constants.EDITABLE,
            })
            field4 = fields.CharField(label='Field4', accesses={
                'jedi': constants.READONLY,
            })
            field5 = fields.CharField(label='Field5', accesses={
                'jedi': constants.REQUIRED,
            })
        form = TestForm.to_formidable(label='test', description="test form")
        self.check_jedi_and_padawan(form)

    def test_hidden_fields(self):
        class TestForm(FormidableForm):
            field1 = fields.CharField(label='Field1', accesses={
                'padawan': constants.REQUIRED,
                'jedi': constants.HIDDEN,
            })
            field2 = fields.CharField(label='Field2', accesses={
                'padawan': constants.HIDDEN,
                'jedi': constants.REQUIRED,
            })
            field3 = fields.CharField(label='Field3', accesses={
                'padawan': constants.REQUIRED,
                'jedi': constants.HIDDEN,
            })
        form = TestForm.to_formidable(label='test', description="test form")
        self.check_jedi_and_padawan(form)


class RenderContextSerializer(TestCase):

    def test_required_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your Name', accesses={
                'jedi': constants.REQUIRED,
            })

        form = TestForm.to_formidable(label='title')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)
        field = data['fields'][0]
        self.assertIn('required', field)
        self.assertTrue(field['required'])
        self.assertIn('disabled', field)
        self.assertFalse(field['disabled'])

    def test_editable_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your Name', accesses={
                'jedi': constants.EDITABLE,
            })

        form = TestForm.to_formidable(label='title')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)
        field = data['fields'][0]
        self.assertIn('required', field)
        self.assertFalse(field['required'])
        self.assertIn('disabled', field)
        self.assertFalse(field['disabled'])

    def test_readonly_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your Name', accesses={
                'jedi': constants.READONLY,
            })

        form = TestForm.to_formidable(label='title')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)
        field = data['fields'][0]
        self.assertIn('required', field)
        self.assertFalse(field['required'])
        self.assertIn('disabled', field)
        self.assertTrue(field['disabled'])

    def test_hidden_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your Name', accesses={
                'jedi': constants.HIDDEN,
            })

        form = TestForm.to_formidable(label='title')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 0)

        # Other access are availabel

        serializer = ContextFormSerializer(form, context={'role': 'human'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)

    def test_with_defaults(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your name', default='Roméo')

        form = TestForm.to_formidable(label='title')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)
        field = data['fields'][0]
        self.assertIn('defaults', field)
        defaults = field['defaults']
        self.assertEqual(defaults, ['Roméo'])

    def test_contextualize(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your name', default='Roméo')

        form = TestForm.to_formidable(label='title')
        contextualized_data = contextualize(form.to_json(), role='jedi')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        serializer_data = serializer.data

        self.assertIn('fields', serializer_data)
        self.assertEquals(len(serializer_data['fields']), 1)

        for field in set(BASE_FIELDS) - {'accesses', 'order', 'set'}:
            # We skip `items` and `multiple` because they are not
            # serialized by FormidableSerializer for CharField
            self.assertEquals(
                contextualized_data['fields'][0][field],
                serializer_data['fields'][0][field]
            )

    def test_contextualize_with_accesses(self):

        class TestForm(FormidableForm):
            editable = fields.CharField(
                label='Your name',
                default='Roméo'
            )
            required = fields.CharField(
                label='Your name',
                default='Roméo',
                accesses={'jedi': constants.REQUIRED}
            )
            readonly = fields.CharField(
                label='Your name',
                default='Roméo',
                accesses={'jedi': constants.READONLY}
            )
            hidden = fields.CharField(
                label='Your name',
                default='Roméo',
                accesses={'jedi': constants.HIDDEN}
            )

        form = TestForm.to_formidable(label='title')
        contextualized_data = contextualize(form.to_json(), role='jedi')

        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        serializer_data = serializer.data

        self.assertIn('fields', serializer_data)
        # We should have 4 fields, but the hidden one is skipped
        self.assertEquals(len(serializer_data['fields']), 3)

        for field in set(BASE_FIELDS) - {'accesses', 'order', 'set'}:
            # We skip `items` and `multiple` because they are not
            # serialized by FormidableSerializer for CharField
            self.assertEquals(
                contextualized_data['fields'][0][field],
                serializer_data['fields'][0][field]
            )

        editable_field = contextualized_data['fields'][0]
        self.assertEquals(editable_field['slug'], 'editable')
        self.assertFalse(editable_field['disabled'])
        self.assertFalse(editable_field['required'])

        required_field = contextualized_data['fields'][1]
        self.assertEquals(required_field['slug'], 'required')
        self.assertFalse(required_field['disabled'])
        self.assertTrue(required_field['required'])

        readonly_field = contextualized_data['fields'][2]
        self.assertEquals(readonly_field['slug'], 'readonly')
        self.assertTrue(readonly_field['disabled'])
        self.assertFalse(readonly_field['required'])

    def test_queryset(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label='Your name', default='Roméo')
            label = fields.CharField(label='label', default='Roméo')
            salary = fields.NumberField()
            birthdate = fields.DateField()

        form = TestForm.to_formidable(label='title')
        serializer = ContextFormSerializer(form, context={'role': 'jedi'})

        # FIXME: Don't know if we still need to maintain this test
        # Could be a duplicate of another.
        with django_perf_rec.record(path='perfs/'):
            serializer.data

    def test_no_condition(self):

        class MyTestForm(FormidableForm):
            value = fields.NumberField()
            threshold = fields.NumberField(
                accesses={
                    'padawan': constants.READONLY,
                    'jedi': constants.REQUIRED
                }
            )

        form = MyTestForm.to_formidable(label='test')
        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('conditions', data)
        self.assertEquals(data['conditions'], [])

    def test_conditions(self):
        conditions = [
            {
                'fields_ids': ['value'],
                'action': 'display_iff',
                'name': 'my condition',
                'tests': [
                    {
                        'field_id': 'threshold',
                        'operator': 'eq',
                        'values': ['12'],
                    },
                ],
            },
        ]

        class MyTestForm(FormidableForm):
            value = fields.NumberField()
            threshold = fields.NumberField()

        form = MyTestForm.to_formidable(label='test')
        form.conditions = conditions
        serializer = ContextFormSerializer(form, context={'role': 'jedi'})
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('conditions', data)
        self.assertEquals(len(data['conditions']), 1)
        self.assertEquals(conditions[0], data['conditions'][0])


class CreateSerializerTestCase(TestCase):

    data = {
        'label': 'test_create',
        'description': 'description create',
        'fields': [],
    }

    fields_without_items = [
        {
            'slug': 'text_input', 'label': 'text label', 'type_id': 'text',
            'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
            'validations': [{'type': 'MINLENGTH', 'value': 5, 'message': 'é'}],
        },
    ]

    fields_with_items = [
        {
            'type_id': 'dropdown',
            'slug': 'dropdown-input', 'label': 'dropdown label',
            'multiple': False, 'items': [
                {'value': 'tutu', 'label': 'toto'},
                {'value': 'tata', 'label': 'plop'},
            ],
            'accesses': [
                {'access_id': 'padawan', 'level': 'REQUIRED'},
            ],
        },
    ]

    fields_with_items_empty_description = [
        {
            'type_id': 'dropdown',
            'slug': 'dropdown-input', 'label': 'dropdown label',
            'multiple': False, 'items': [
                {'value': 'tutu', 'label': 'toto', 'description': ''},
                {'value': 'tata', 'label': 'plop'},
            ],
            'description': '',
            'accesses': [
                {'access_id': 'padawan', 'level': 'REQUIRED'},
            ],
        },
    ]

    fields_with_validation = [
        {
            'slug': 'text_input',
            'label': 'text label',
            'type_id': 'text',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED},
            ],
            'validations': [
                {
                    'type': 'MINLENGTH',
                    'value': '5',
                },
            ],
        },
        {
            'slug': 'input-date',
            'label': 'licence driver',
            'type_id': 'date',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'validations': [
                {
                    'type': 'IS_DATE_IN_THE_FUTURE',
                    'value': 'false',
                },
            ],
        },
    ]

    fields_with_defaults = [
        {
            'slug': 'text',
            'label': 'state',
            'type_id': 'dropdown',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'defaults': ['france'],
            'items': [
                {
                    'value': 'france',
                    'label': 'France',
                },
                {
                    'value': 'england',
                    'label': 'England',
                },
            ],
        },
    ]

    radios_buttons_fields = [
        {
            'slug': 'test-radios',
            'label': 'test-radios-buttons',
            'type_id': 'radios_buttons',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'items': [
                {'value': 'tutu', 'label': 'toto'},
                {'value': 'foo', 'label': 'bar'},
            ],
        },
    ]

    valid_conditions = [
        {
            'fields_ids': ['input-date'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'text_input',
                    'operator': 'eq',
                    'values': ['text'],
                },
            ],
        },
    ]

    valid_conditions_invalid_ref = [
        {
            'fields_ids': ['missing'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'unknown',
                    'operator': 'eq',
                    'values': ['text'],
                },
            ],
        },
    ]

    valid_conditions_invalid_action = [
        {
            'fields_ids': ['input-date'],
            'action': 'bad-action',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'text_input',
                    'operator': 'eq',
                    'values': ['text'],
                },
            ],
        },
    ]

    valid_conditions_invalid_op = [
        {
            'fields_ids': ['input-date'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'text_input',
                    'operator': 'BAD',
                    'values': ['text'],
                },
            ],
        },
    ]

    valid_conditions_invalid_test = [
        {
            'fields_ids': ['input-date'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [],
        },
    ]

    valid_conditions_invalid_dup = [
        {
            'fields_ids': ['input-date'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'text_input',
                    'operator': 'eq',
                    'values': ['text'],
                },
            ],
        },
        {
            'fields_ids': ['input-date'],
            'action': 'display_iff',
            'name': 'my condition',
            'tests': [
                {
                    'field_id': 'text_input',
                    'operator': 'eq',
                    'values': ['text'],
                },
            ],
        },
    ]

    format_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'help_text',
            'description': 'Hello',
            'accesses': [],
        },
    ]
    format_without_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'help_text',
            'accesses': [],
        },
    ]
    format_field_title = [
        {
            'slug': 'mytitle',
            'type_id': 'title',
            'label': 'This is an Onboarding Form.',
            'accesses': [],
        },
    ]
    format_field_separator = [
        {
            'slug': 'sepa',
            'type_id': 'separator',
            'accesses': [],
        },
    ]

    def test_create_form(self):
        serializer = FormidableSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, 'test_create')
        self.assertEquals(instance.description, 'description create')
        self.assertEquals(instance.fields.count(), 0)

    def test_create_form_conditions(self):
        """
        deserialize a form with valid `conditions` then compare the object
        created with the data in the payload
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        form.refresh_from_db()
        self.assertEqual(len(form.conditions), 1)
        condition = form.conditions[0]
        self.assertIn('name', condition)
        self.assertEqual(condition['name'], 'my condition')
        self.assertIn('action', condition)
        self.assertEqual(condition['action'], 'display_iff')
        self.assertIn('fields_ids', condition)
        self.assertEqual(condition['fields_ids'], ['input-date'])
        self.assertIn('tests', condition)
        self.assertEqual(len(condition['tests']), 1)
        test = condition['tests'][0]
        self.assertIn('operator', test)
        self.assertEqual(test['operator'], 'eq')
        self.assertIn('field_id', test)
        self.assertEqual(test['field_id'], 'text_input')
        self.assertIn('values', test)
        self.assertEqual(test['values'], ['text'])

    def test_conditions_on_update(self):
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        # update with conditions
        data['conditions'] = copy.deepcopy(self.valid_conditions)
        serializer = FormidableSerializer(instance=form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        # reload form from the database, ensure conditions were saved
        form.refresh_from_db()
        self.assertEqual(len(form.conditions), 1)
        condition = form.conditions[0]
        self.assertIn('name', condition)
        self.assertEqual(condition['name'], 'my condition')
        self.assertIn('action', condition)
        self.assertEqual(condition['action'], 'display_iff')
        self.assertIn('fields_ids', condition)
        self.assertEqual(condition['fields_ids'], ['input-date'])
        self.assertIn('tests', condition)
        self.assertEqual(len(condition['tests']), 1)
        test = condition['tests'][0]
        self.assertIn('operator', test)
        self.assertEqual(test['operator'], 'eq')
        self.assertIn('field_id', test)
        self.assertEqual(test['field_id'], 'text_input')
        self.assertIn('values', test)
        self.assertEqual(test['values'], ['text'])

    def test_create_form_conditions_invalid_reference(self):
        """
        deserialize a form that has conditions that references non existing
        fields
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_ref)
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(len(serializer.errors['non_field_errors']), 1)
        self.assertIn(
            serializer.errors['non_field_errors'][0],
            ['Condition (my condition) is using undefined fields (unknown, missing)',  # noqa
             'Condition (my condition) is using undefined fields (missing, unknown)']  # noqa
        )

    def test_create_form_conditions_invalid_reference_no_name(self):
        """
        deserialize a form that has conditions that references non existing
        fields + No condition name
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_ref)
        del data['conditions'][0]['name']
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(len(serializer.errors['non_field_errors']), 1)
        self.assertIn(
            serializer.errors['non_field_errors'][0],
            ['Condition (#1) is using undefined fields (unknown, missing)',
             'Condition (#1) is using undefined fields (missing, unknown)']
        )

    def test_create_form_conditions_invalid_reference_empty_name(self):
        """
        deserialize a form that has conditions that references non existing
        fields + Empty or "None" condition name
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_ref)
        for value in ('', None):
            data['conditions'][0]['name'] = value
            serializer = FormidableSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('non_field_errors', serializer.errors)
            self.assertEqual(len(serializer.errors['non_field_errors']), 1)
            self.assertIn(
                serializer.errors['non_field_errors'][0],
                ['Condition (#1) is using undefined fields (unknown, missing)',
                 'Condition (#1) is using undefined fields (missing, unknown)']
            )

    def test_create_form_conditions_invalid_action(self):
        """
        deserialize a form that has conditions using unknown action
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(
            self.valid_conditions_invalid_action
        )
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['conditions'][0]['action'][0],
            '"bad-action" is not a valid choice.'
        )

    def test_create_form_conditions_invalid_op(self):
        """
        deserialize a form that has a condition using an unknown operator in
        its tests
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_op)
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['conditions'][0]['tests'][0]['operator'][0],
            '"BAD" is not a valid choice.'
        )

    def test_create_form_conditions_invalid_test(self):
        """
        deserialize a form that has a condition with an empty tests list
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_test)
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['conditions'][0]['tests']['non_field_errors'][0],
            'This list may not be empty.'
        )

    def test_create_form_conditions_invalid_dup(self):
        """
        deserialize a form that has two conditions display_iff for the same
        field
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions_invalid_dup)
        serializer = FormidableSerializer(data=data)
        # TODO decide if the validation should fail
        # now that we allow multiple conditions for one field
        self.assertTrue(serializer.is_valid())

    def test_create_form_conditions_null_name(self):
        """
        validate a form when condition has a name=None.
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions)
        data['conditions'][0]['name'] = None
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        form.refresh_from_db()
        self.assertEqual(len(form.conditions), 1)
        condition = form.conditions[0]
        self.assertIn('name', condition)
        self.assertIsNone(condition['name'])

    def test_create_form_conditions_empty_name(self):
        """
        validate a form when condition has a name="".
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions)
        data['conditions'][0]['name'] = ""
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        form.refresh_from_db()
        self.assertEqual(len(form.conditions), 1)
        condition = form.conditions[0]
        self.assertIn('name', condition)
        self.assertEqual(condition['name'], "")

    def test_create_form_conditions_no_name(self):
        """
        validate a form when condition has a no name.
        """
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['conditions'] = copy.deepcopy(self.valid_conditions)
        del data['conditions'][0]['name']
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        form.refresh_from_db()
        self.assertEqual(len(form.conditions), 1)
        condition = form.conditions[0]
        self.assertNotIn('name', condition)

    def test_create_field(self):
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_without_items)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEquals(instance.label, 'test_create')
        self.assertEquals(instance.description, 'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.filter(type_id='text').first()
        self.assertEquals(field.type_id, 'text')
        self.assertEquals(field.label, 'text label')
        self.assertEquals(field.slug, 'text_input')
        self.assertEquals(field.items.count(), 0)
        # just one access has been specified, check the the other are created
        # with default value
        self.assertEquals(field.accesses.count(), 5)

    def test_create_ordering(self):
        # aggregate fields
        def extend(l, elt):
            l.extend(elt)
            return l

        fields = reduce(extend, [
            self.fields_with_items, self.fields_without_items,
            self.format_field_helptext, self.format_field_separator,
            self.format_field_title
        ], [])
        data = copy.deepcopy(self.data)
        data['fields'] = fields
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertTrue(form.fields.filter(
            slug='dropdown-input', order=0
        ).exists())
        self.assertTrue(form.fields.filter(
            slug='text_input', order=1
        ).exists())
        self.assertTrue(form.fields.filter(
            slug='myhelptext', order=2
        ).exists())
        self.assertTrue(form.fields.filter(
            slug='sepa', order=3
        ).exists())
        self.assertTrue(form.fields.filter(
            slug='mytitle', order=4
        ).exists())

    def test_create_order(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_validation
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.fields.count(), 2)
        self.assertTrue(
            instance.fields.filter(order=0, slug='text_input').exists()
        )
        self.assertTrue(
            instance.fields.filter(order=1, slug='input-date').exists()
        )

    def test_create_field_with_validations(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_validation
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.fields.count(), 2)
        field = instance.fields.filter(type_id='date').first()
        self.assertEquals(field.validations.count(), 1)
        validation = field.validations.first()
        self.assertEquals(validation.value, 'false')

    def test_create_fields_with_defaults(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_defaults
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertEqual(field.defaults.count(), 1)
        self.assertTrue(field.defaults.filter(value='france').exists())

    def test_create_field_error_validations(self):
        data = copy.deepcopy(self.data)
        fields_data = copy.deepcopy(self.fields_with_validation)
        fields_data[0]['validations'][0]['value'] = 'test'
        data['fields'] = fields_data
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_field_with_items(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_items
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEquals(instance.label, 'test_create')
        self.assertEquals(instance.description, 'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertEquals(field.type_id, 'dropdown')
        self.assertEquals(field.label, 'dropdown label')
        self.assertEquals(field.slug, 'dropdown-input')
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(value='tutu', label='toto').exists()
        )
        self.assertTrue(
            field.items.filter(value='tata', label='plop').exists()
        )
        self.assertEquals(field.accesses.count(), 5)

    def test_create_empty_description(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_items_empty_description
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEquals(instance.label, 'test_create')
        self.assertEquals(instance.description, 'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertEquals(field.slug, 'dropdown-input')
        self.assertEquals(field.help_text, '')
        self.assertEquals(field.items.count(), 2)
        item = field.items.first()
        self.assertEquals(item.help_text, '')

    def test_create_field_without_items(self):
        data = copy.deepcopy(self.data)
        fields = copy.deepcopy(self.fields_with_items)
        fields[0].pop('items')
        data['fields'] = fields
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fields', serializer.errors)

    def test_create_wrong_access(self):
        data = copy.deepcopy(self.data)
        fields = copy.deepcopy(self.fields_with_items)
        fields[0]['accesses'][0]['access_id'] = 'wrong'
        data['fields'] = fields
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fields', serializer.errors)

    def test_create_radios_buttons_field(self):
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.radios_buttons_fields)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertTrue(field.type_id, 'radios_buttons')
        self.assertEqual(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(order=0, value='tutu', label='toto').exists()
        )
        self.assertTrue(
            field.items.filter(order=1, value='foo', label='bar').exists()
        )

    def test_create_helptext(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.format_field_helptext
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        qs = instance.fields.filter(type_id='help_text', help_text='Hello')
        self.assertTrue(qs.exists())

    def test_create_helptext_wrong(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.format_without_field_helptext
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_title(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.format_field_title
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        qs = instance.fields.filter(
            type_id='title', label='This is an Onboarding Form.'
        )
        self.assertTrue(qs.exists())

    def test_create_sepa(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.format_field_separator
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        qs = instance.fields.filter(
            type_id='separator', slug='sepa'
        )
        self.assertTrue(qs.exists())


class CreateSerializerTransactionTestCase(TransactionTestCase):

    def test_unique_transaction(self):
        data = copy.deepcopy(CreateSerializerTestCase.data)
        data['fields'] = CreateSerializerTestCase.fields_with_items
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with CaptureQueriesContext(connection) as capture:
            serializer.save()
        begin_count = sum(1 for query in capture.captured_queries
                          if query['sql'] == 'BEGIN')
        self.assertEqual(begin_count, 1)


class UpdateFormTestCase(TestCase):

    data = {
        'label': 'edited form',
        'description': 'description edited',
        'fields': [],
    }

    fields = [
        {
            'type_id': 'text', 'label': 'edited field', 'slug': 'text-slug',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'validations': [{'type': 'MAXLENGTH', 'value': '128'}]
        },
    ]

    fields_with_validation = [
        {
            'slug': 'text_input',
            'label': 'text label',
            'type_id': 'text',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'validations': [
                {
                    'type': 'MINLENGTH',
                    'value': '5',
                },
            ],
        },
        {
            'slug': 'input-date',
            'label': 'licence driver',
            'type_id': 'date',
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED}
            ],
            'validations': [
                {
                    'type': 'IS_DATE_IN_THE_FUTURE',
                    'value': 'false',
                },
            ],
        },
    ]

    fields_items = [
        {
            'type_id': 'dropdown', 'label': 'edited field',
            'slug': 'dropdown-input', 'items': [
                {'value': 'gun', 'label': 'desert-eagle'},
                {'value': 'sword', 'label': 'Andúril'}
            ],
            'accesses': [
                {'access_id': 'padawan', 'level': constants.REQUIRED},
            ],
        },
    ]

    fields_with_defaults = [{
        'slug': 'state',
        'label': 'state',
        'type_id': 'dropdown',
        'accesses': [
            {'access_id': 'padawan', 'level': constants.REQUIRED},
        ],
        'items': [
            {'value': 'france', 'label': 'France'},
        ],
        'defaults': ['france'],
    }]

    def setUp(self):
        super(UpdateFormTestCase, self).setUp()
        self.form = Formidable.objects.create(
            label='testform', description='test form',
        )

    def test_update_simple(self):
        serializer = FormidableSerializer(instance=self.form, data=self.data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.label, 'edited form')

    def test_create_defaults_on_update(self):
        self.form.fields.create(
            type_id='dropdown', label='state', slug='text',
            order=3,
        )
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_defaults)
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        field = instance.fields.get(slug='state')
        self.assertEqual(field.defaults.count(), 1)
        self.assertTrue(field.defaults.filter(value='france').exists())

    def test_update_defaults(self):
        field = self.form.fields.create(
            type_id='dropdown', label='state', slug='text',
            order=3,
        )
        field.defaults.create(value='england')
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_defaults)
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        field = instance.fields.get(slug='state')
        self.assertEqual(field.defaults.count(), 1)
        self.assertTrue(field.defaults.filter(value='france').exists())

    def test_order_on_update(self):
        self.form.fields.create(type_id='text', slug='already-there', order=0)
        fields_to_update = self.fields + self.fields_items + [
            {'type_id': 'text', 'slug': 'already-there', 'label': 'tutu',
                'accesses': []},
        ]
        data = copy.deepcopy(self.data)
        data['fields'] = fields_to_update
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertTrue(
            self.form.fields.filter(slug='text-slug', order=0).exists()
        )
        self.assertTrue(
            self.form.fields.filter(slug='dropdown-input', order=1).exists()
        )
        self.assertTrue(
            self.form.fields.filter(slug='already-there', order=2).exists()
        )

    def test_create_field_on_update(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.type_id, 'text')
        # check accesses are fully created
        self.assertEquals(field.accesses.count(), 5)

    def test_create_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label='weapons',
            order=self.form.get_next_field_order()
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level='REQUIRED'
        )
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_items)
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(value='sword', label='Andúril').exists()
        )
        self.assertTrue(
            field.items.filter(value='gun', label='desert-eagle').exists()
        )

    def test_update_fields(self):
        self.text_field = self.form.fields.create(
            type_id='text', label='test text', slug='text-slug',
            placeholder='put your name here', help_text='your name',
            order=self.form.get_next_field_order()
        )
        self.text_field.accesses.create(
            access_id='padawan', level=constants.REQUIRED
        )
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        field = form.fields.first()
        self.assertEquals(self.text_field.pk, field.pk)
        self.assertEquals(field.label, 'edited field')

    def test_update_fields_items(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label='weapons',
            order=self.form.get_next_field_order()
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level=constants.EDITABLE
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(
            value='gun', label='eagle', order=order
        )
        self.dropdown_fields.items.create(
            value='sword', label='excalibur', order=order + 1
        )
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_items
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        field = form.fields.first()
        self.assertEquals(self.dropdown_fields.pk, field.pk)
        self.assertEquals(field.label, 'edited field')
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(value='gun', label='desert-eagle').exists()
        )
        self.assertTrue(
            field.items.filter(value='sword', label='Andúril').exists()
        )
        qs = field.accesses.filter(
            access_id='padawan', level=constants.REQUIRED
        )
        self.assertTrue(qs.exists())

    def test_delete_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label='weapons',
            order=self.form.get_next_field_order()
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(value='gun', label='eagle',
                                          order=order)
        self.dropdown_fields.items.create(value='sword', label='excalibur',
                                          order=order + 1)
        serializer = FormidableSerializer(instance=self.form, data=self.data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 0)

    def test_delete_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label='weapons',
            order=self.form.get_next_field_order()
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level=constants.REQUIRED
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(
            value='gun', label='eagle', order=order
        )
        self.dropdown_fields.items.create(
            value='sword', label='excalibur', order=order + 1
        )
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_items)
        data['fields'][0]['items'] = []
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.items.count(), 0)


class CreateSerializerMigrationTestCase(TestCase):
    data = {
        'label': 'test_create',
        'description': 'description create',
        'fields': [
            {
                'type_id': 'dropdown',
                'slug': 'dropdown-input', 'label': 'dropdown label',
                'help_text': 'Field Help',
                'multiple': False,
                'items': [
                    {'value': 'tutu', 'label': 'toto', 'help_text': 'Item Help'},  # noqa
                    {'value': 'tata', 'label': 'plop'},
                ],
                'accesses': [],
            },
        ],
    }

    def test_create(self):
        serializer = FormidableSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        self.assertEqual(form.fields.all()[0].help_text, 'Field Help')
        self.assertEqual(form.fields.all()[0].items.all()[0].help_text,
                         'Item Help')
