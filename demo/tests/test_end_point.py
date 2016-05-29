# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import copy
from functools import reduce

from django.test import TestCase

from formidable import constants
from formidable.models import Formidable
from formidable.forms import FormidableForm, fields
from formidable.serializers.forms import FormidableSerializer
from formidable.serializers.forms import ContextFormSerializer
from formidable.serializers.fields import BASE_FIELDS, FieldSerializerRegister
from formidable.serializers.presets import PresetsSerializer
from formidable.serializers.presets import PresetsArgsSerializer
from formidable.serializers.presets import PresetsArgSerializerWithItems
from formidable.forms.validations import presets


RENDER_BASE_FIELDS = list(set(BASE_FIELDS) - set(['order']))


class RenderSerializerTestCase(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(
            label=u'testform', description=u'test form',
        )
        self.text_field = self.form.fields.create(
            type_id='text', label='test text', slug='test_text',
            placeholder='put your name here', help_text=u'your name',
            order=self.form.get_next_field_order()
        )
        self.text_field2 = self.form.fields.create(
            type_id='text', label='test text 2', slug='test_text_2',
            placeholder='put your name here', help_text=u'your name',
            order=self.form.get_next_field_order()
        )
        self.text_field.accesses.create(
            level=constants.REQUIRED, access_id=u'padawan'
        )
        self.text_field2.accesses.create(
            level=constants.EDITABLE, access_id=u'jedi', display='TABLE'
        )
        self.text_field.validations.create(
            type=u'MINLENGTH', value=u'5'
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
            placeholder='put your name here', help_text=u'your name',
            order=self.form.get_next_field_order()
        )
        data = self.serializer.data
        ordered_slug = ['test_text', 'test_text_2', 'test_text_3']
        for index, field in enumerate(data['fields']):
            self.assertEqual(ordered_slug[index], field['slug'])

    def test_form_field(self):
        data = self.serializer.data
        self.assertIn('label', data)
        self.assertEquals(data['label'], u'testform')
        self.assertIn('description', data)
        self.assertEquals(data['description'], u'test form')
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
        self.assertEquals(text_field['type_id'], u'text')
        self.assertEquals(text_field['label'], u'test text')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['help_text'], 'your name')
        self.assertEquals(text_field['default'], None)
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], u'padawan')
        self.assertEquals(accesses['level'], constants.REQUIRED)
        self.assertEquals(accesses['display'], None)

    def test_text_field2(self):
        data = self.serializer.data
        text_field = data['fields'][1]
        self.assertEquals(text_field['type_id'], u'text')
        self.assertEquals(text_field['label'], u'test text 2')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['help_text'], 'your name')
        self.assertEquals(text_field['default'], None)
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], u'jedi')
        self.assertEquals(accesses['level'], constants.EDITABLE)
        self.assertEquals(accesses['display'], 'TABLE')

    def test_dropdown_field(self):
        self.form.fields.all().delete()
        self.dropdown = self.form.fields.create(
            type_id='dropdown', label=u'choose your weapon',
            order=self.form.get_next_field_order()
        )
        order = self.dropdown.get_next_order()
        self.dropdown.items.create(key='tutu', value='toto', order=order)
        self.dropdown.items.create(key=u'plop', value=u'Intérnätiônal',
                                   order=order+1)
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
            help_text=u'Please enter your information here',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in list(set(RENDER_BASE_FIELDS) - set(['label'])):
            self.assertIn(field, data)
        self.assertEqual(data['help_text'],
                         'Please enter your information here')

    def test_title_field(self):
        self.form.fields.all().delete()
        self.title = self.form.fields.create(
            type_id='title', slug='my title',
            label=u'This is on onboarding form.',
            order=self.form.get_next_field_order()
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in set(RENDER_BASE_FIELDS) - set(['help_text']):
            self.assertIn(field, data)
        self.assertEqual(data['label'],
                         'This is on onboarding form.')
        self.assertNotIn('help_text', data)

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


class RenderContextSerializer(TestCase):

    def test_required_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label=u'Your Name', accesses={
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
            name = fields.CharField(label=u'Your Name', accesses={
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
            name = fields.CharField(label=u'Your Name', accesses={
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
            name = fields.CharField(label=u'Your Name', accesses={
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


class CreateSerializerTestCase(TestCase):

    data = {
        'label': u'test_create',
        'description': u'description create',
        'fields': []
    }
    fields_without_items = [
        {
            'slug': 'text_input', 'label': 'text label', 'type_id': 'text',
            'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
            'validations': [{'type': 'MINLENGTH', 'value': 5, 'message': u'é'}]
        }
    ]

    fields_with_items = [
        {
            'type_id': 'dropdown',
            'slug': 'dropdown-input', 'label': 'dropdown label',
            'multiple': False, 'items': [
                {'key': 'tutu', 'value': 'toto'},
                {'key': 'tata', 'value': 'plop'},
            ],
            'accesses': [{
                'access_id': 'padawan', 'level': 'REQUIRED'
            }]
        }
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
            ]
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
            ]
        }
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
                {'key': 'tutu', 'value': 'toto'},
                {'key': 'foo', 'value': 'bar'},
            ]
        }
    ]

    valid_presets = [{
        'preset_id': 'confirmation',
        'message': 'not the same',
        'arguments': [{
            'slug': 'left',
            'field_id': 'input-date',
        }, {
            'slug': 'right',
            'field_id': 'text_input',
        }],
    }]

    presets_with_wrong_parameters = [
      {
        'preset_id': 'confirmation',
        'message': 'noteq!',
        'arguments': [{
          'slug': 'left',
          'field_id': 'testField2',
        }, {
          'slug': 'comparator',
          'value': 'eq',
        }, {
          'slug': 'right',
          'field_id': 'testField3',
        }]
      }
    ]

    format_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'help_text',
            'help_text': 'Hello',
            'accesses': [],
        }
    ]
    format_without_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'help_text',
            'accesses': [],
        }
    ]
    format_field_title = [
        {
            'slug': 'mytitle',
            'type_id': 'title',
            'label': 'This is an Onboarding Form.',
            'accesses': [],
        }
    ]
    format_field_separator = [
        {
            'slug': 'sepa',
            'type_id': 'separator',
            'accesses': [],
        }
    ]

    def test_create_form(self):
        serializer = FormidableSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, u'test_create')
        self.assertEquals(instance.description, u'description create')
        self.assertEquals(instance.fields.count(), 0)

    def test_create_form_presets(self):
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_with_validation)
        data['presets'] = copy.deepcopy(self.valid_presets)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        self.assertEqual(form.presets.count(), 1)
        preset = form.presets.first()
        self.assertTrue(
            preset.arguments.filter(
                slug='left', field_id='input-date').exists()
        )
        self.assertTrue(
            preset.arguments.filter(
                slug='right', field_id='text_input').exists()
        )

    def test_create_form_with_presets_invalid_argument(self):
        data = copy.deepcopy(self.data)
        data['presets'] = copy.deepcopy(self.presets_with_wrong_parameters)
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn(
            serializer.errors['non_field_errors'][0],
            'Preset (confirmation) argument is using an undefined field (testField2)'  # noqa
        )

    def test_create_field(self):
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_without_items)
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, u'test_create')
        self.assertEquals(instance.description, u'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.filter(type_id=u'text').first()
        self.assertEquals(field.type_id, 'text')
        self.assertEquals(field.label, 'text label')
        self.assertEquals(field.slug, 'text_input')
        self.assertEquals(field.items.count(), 0)
        # just one access has been specified, check the the other are created
        # with default value
        self.assertEquals(field.accesses.count(), 4)

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
        field = instance.fields.filter(type_id=u'date').first()
        self.assertEquals(field.validations.count(), 1)
        validation = field.validations.first()
        self.assertEquals(validation.value, 'false')

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
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, u'test_create')
        self.assertEquals(instance.description, u'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertEquals(field.type_id, 'dropdown')
        self.assertEquals(field.label, 'dropdown label')
        self.assertEquals(field.slug, 'dropdown-input')
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(key='tutu', value='toto').exists()
        )
        self.assertTrue(
            field.items.filter(key='tata', value='plop').exists()
        )
        self.assertEquals(field.accesses.count(), 4)

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
        fields[0]['accesses'][0]['access_id'] = u'wrong'
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
            field.items.filter(order=0, key='tutu', value='toto').exists()
        )
        self.assertTrue(
            field.items.filter(order=1, key='foo', value='bar').exists()
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


class UpdateFormTestCase(TestCase):

    data = {
        'label': u'edited form',
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
        }
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
            ]
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
            ]
        }
    ]

    valid_presets = [{
        'preset_id': 'confirmation',
        'message': 'not the same',
        'arguments': [{
            'slug': 'left',
            'field_id': 'input-date',
        }, {
            'slug': 'right',
            'field_id': 'text_input',
        }],
    }]

    fields_items = [{
        'type_id': 'dropdown', 'label': 'edited field',
        'slug': 'dropdown-input', 'items': [
            {'key': 'gun', 'value': 'desert-eagle'},
            {'key': 'sword', 'value': 'Andúril'}
        ],
        'accesses': [
            {'access_id': 'padawan', 'level': constants.REQUIRED}
        ],
    }]

    def setUp(self):
        super(UpdateFormTestCase, self).setUp()
        self.form = Formidable.objects.create(
            label=u'testform', description=u'test form',
        )

    def test_update_simple(self):
        serializer = FormidableSerializer(instance=self.form, data=self.data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.label, u'edited form')

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

    def test_presets_on_update(self):
        preset = self.form.presets.create(slug='comparison', message='compare')
        preset.arguments.create(slug='left', field_id='field1')
        preset.arguments.create(slug='right', value='12')
        preset.arguments.create(slug='operator')
        self.assertEqual(self.form.presets.count(), 1)
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_with_validation
        data['presets'] = self.valid_presets
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()
        self.assertEqual(form.pk, self.form.pk)
        self.assertEqual(form.presets.count(), 1)
        preset = form.presets.first()
        self.assertEqual(preset.arguments.count(), 2)
        self.assertTrue(
            preset.arguments.filter(
                slug='left', field_id='input-date').exists()
        )
        self.assertTrue(
            preset.arguments.filter(
                slug='right', field_id='text_input').exists()
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
        self.assertEquals(field.accesses.count(), 4)

    def test_create_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
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
            field.items.filter(key=u'sword', value=u'Andúril').exists()
        )
        self.assertTrue(
            field.items.filter(key=u'gun', value=u'desert-eagle').exists()
        )

    def test_update_fields(self):
        self.text_field = self.form.fields.create(
            type_id='text', label='test text', slug='text-slug',
            placeholder='put your name here', help_text=u'your name',
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
        self.assertEquals(field.label, u'edited field')

    def test_update_fields_items(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
            order=self.form.get_next_field_order()
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level=constants.EDITABLE
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(
            key=u'gun', value=u'eagle', order=order
        )
        self.dropdown_fields.items.create(
            key=u'sword', value=u'excalibur', order=order+1
        )
        data = copy.deepcopy(self.data)
        data['fields'] = self.fields_items
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        field = form.fields.first()
        self.assertEquals(self.dropdown_fields.pk, field.pk)
        self.assertEquals(field.label, u'edited field')
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(key='gun', value='desert-eagle').exists()
        )
        self.assertTrue(
            field.items.filter(key='sword', value=u'Andúril').exists()
        )
        qs = field.accesses.filter(
            access_id='padawan', level=constants.REQUIRED
        )
        self.assertTrue(qs.exists())

    def test_delete_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
            order=self.form.get_next_field_order()
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(key=u'gun', value=u'eagle',
                                          order=order)
        self.dropdown_fields.items.create(key=u'sword', value=u'excalibur',
                                          order=order+1)
        serializer = FormidableSerializer(instance=self.form, data=self.data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 0)

    def test_delete_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
            order=self.form.get_next_field_order()
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level=constants.REQUIRED
        )
        order = self.dropdown_fields.get_next_order()
        self.dropdown_fields.items.create(
            key=u'gun', value=u'eagle', order=order
        )
        self.dropdown_fields.items.create(
            key=u'sword', value=u'excalibur', order=order+1
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


class TestPresetsSerializerRender(TestCase):

    class PresetsTest(presets.Presets):

        label = 'test-label'
        slug = 'test-slug'
        description = 'this is a test'
        default_message = 'thrown message when error test'

        class MetaParameters:
            pass

    class PresetsTestWithArgs(presets.Presets):

        label = 'test-label-args'
        slug = 'test-slug-args'
        description = 'this is a test with argument'
        default_message = 'you shouldnt see this'

        class MetaParameters(object):
            lhs = presets.PresetFieldArgument(label='lhs')
            rhs = presets.PresetValueArgument(
                label='Rhs', slug='test-rhs',
                items={'tutu': 'toto', 'foo': 'bar'},
            )

    def test_render_preset_attr(self):
        preset_instance = self.PresetsTest([])
        serializer = PresetsSerializer(preset_instance)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('label', data)
        self.assertEqual(data['label'], 'test-label')
        self.assertIn('slug', data)
        self.assertEqual(data['slug'], 'test-slug')
        self.assertIn('description', data)
        self.assertEqual(data['description'], 'this is a test')
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'thrown message when error test')

    def test_render_class_attr(self):
        preset_instance = self.PresetsTest([])
        preset_instance.description = 'oh no !'
        serializer = PresetsSerializer(preset_instance)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('description', data)
        self.assertNotEqual(data['description'], 'oh no !')
        self.assertEqual(data['description'], 'this is a test')

    def test_render_preset_field_arg(self):
        field_arg = presets.PresetFieldArgument(
            slug='test', label='test',
            help_text='pick up the field to validated'
        )
        serializer = PresetsArgsSerializer(field_arg)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('slug', data)
        self.assertEqual(data['slug'], 'test')
        self.assertIn('label', data)
        self.assertEqual(data['label'], 'test')
        self.assertIn('help_text', data)
        self.assertEqual(data['help_text'], 'pick up the field to validated')
        self.assertIn('types', data)
        self.assertEqual(len(data['types']), 1)
        self.assertIn('field', data['types'])

    def test_render_preset_with_items(self):
        field_arg = presets.PresetValueArgument(
            slug='test', label='test',
            help_text='pick up the field to validated',
            items={'foo': 'bar', 'tutu': 'toto'}
        )
        serializer = PresetsArgSerializerWithItems(instance=field_arg)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 2)
        self.assertIn('foo', data['items'])
        self.assertEqual(data['items']['foo'], 'bar')

    def test_render_preset_value_arg(self):
        field_arg = presets.PresetValueArgument(
            slug='test', label='test',
            help_text='pick up the value to compare'
        )
        serializer = PresetsArgsSerializer(field_arg)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('slug', data)
        self.assertEqual(data['slug'], 'test')
        self.assertIn('label', data)
        self.assertEqual(data['label'], 'test')
        self.assertIn('help_text', data)
        self.assertEqual(data['help_text'], 'pick up the value to compare')
        self.assertIn('types', data)
        self.assertEqual(len(data['types']), 1)
        self.assertIn('value', data['types'])

    def test_render_preset_hybrid_arg(self):
        field_arg = presets.PresetFieldOrValueArgument(
            slug='test', label='test',
            help_text='pick up the value to compare'
        )
        serializer = PresetsArgsSerializer(field_arg)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('slug', data)
        self.assertEqual(data['slug'], 'test')
        self.assertIn('label', data)
        self.assertEqual(data['label'], 'test')
        self.assertIn('help_text', data)
        self.assertEqual(data['help_text'], 'pick up the value to compare')
        self.assertIn('types', data)
        self.assertEqual(len(data['types']), 2)
        self.assertIn('value', data['types'])
        self.assertIn('field', data['types'])

    def test_render_preset_with_argument(self):
        preset_instance = self.PresetsTestWithArgs(arguments=[])
        serializer = PresetsSerializer(preset_instance)
        self.assertTrue(serializer.data)
        data = serializer.data
        self.assertIn('arguments', data)
        self.assertEqual(len(data['arguments']), 2)
