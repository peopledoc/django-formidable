# -*- coding: utf-8 -*-
import copy

from django.test import TestCase

from formidable.models import Formidable
from formidable.forms import FormidableForm, fields
from formidable.serializers.forms import FormidableSerializer
from formidable.serializers.forms import ContextFormSerializer
from formidable.serializers.fields import BASE_FIELDS, FieldSerializerRegister


class RenderSerializerTestCase(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(
            label=u'testform', description=u'test form',
        )
        self.text_field = self.form.fields.create(
            type_id='text', label='test text', slug='test_text',
            placeholder='put your name here', helpText=u'your name',
        )
        self.text_field2 = self.form.fields.create(
            type_id='text', label='test text 2', slug='test_text_2',
            placeholder='put your name here', helpText=u'your name',
        )
        self.text_field.accesses.create(
            level=u'REQUIRED', access_id=u'padawan'
        )
        self.text_field2.accesses.create(
            level=u'EDITABLE', access_id=u'jedi', display='TABLE'
        )
        self.text_field.validations.create(
            type=u'MINLENGTH', value=u'5'
        )
        self.serializer = FormidableSerializer(instance=self.form)

    def test_ok(self):
        self.assertTrue(self.serializer.data)

    def test_register(self):
        register = FieldSerializerRegister.get_instance()
        assert len(register) == 13

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
        for field in BASE_FIELDS:
            self.assertIn(field, field_text)

    def test_text_field(self):
        data = self.serializer.data
        text_field = data['fields'][0]
        self.assertEquals(text_field['type_id'], u'text')
        self.assertEquals(text_field['label'], u'test text')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['helpText'], 'your name')
        self.assertEquals(text_field['default'], None)
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], u'padawan')
        self.assertEquals(accesses['level'], u'REQUIRED')
        self.assertEquals(accesses['display'], None)

    def test_text_field2(self):
        data = self.serializer.data
        text_field = data['fields'][1]
        self.assertEquals(text_field['type_id'], u'text')
        self.assertEquals(text_field['label'], u'test text 2')
        self.assertEquals(text_field['placeholder'], 'put your name here')
        self.assertEquals(text_field['helpText'], 'your name')
        self.assertEquals(text_field['default'], None)
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)
        self.assertIn('accesses', text_field)
        self.assertEquals(len(text_field['accesses']), 1)
        accesses = text_field['accesses'][0]
        self.assertEquals(accesses['access_id'], u'jedi')
        self.assertEquals(accesses['level'], u'EDITABLE')
        self.assertEquals(accesses['display'], 'TABLE')

    def test_dropdown_field(self):
        self.form.fields.all().delete()
        self.dropdown = self.form.fields.create(
            type_id='dropdown', label=u'choose your weapon',
        )
        self.dropdown.items.create(key='tutu', value='toto')
        self.dropdown.items.create(key=u'plop', value=u'Intérnätiônal')
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in BASE_FIELDS:
            self.assertIn(field, data)
        self.assertIn('multiple', data)
        self.assertEquals(data['multiple'], False)
        self.assertIn('items', data)
        self.assertEquals(len(data['items'].keys()), 2)
        self.assertEquals(len(data['items'].values()), 2)

    def test_helptext_field(self):
        self.form.fields.all().delete()
        self.help_text = self.form.fields.create(
            type_id='helpText', slug='your help text',
            helpText=u'Please enter your information here'
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in BASE_FIELDS:
            if field == u'label':
                continue
            self.assertIn(field, data)
        self.assertEqual(data['helpText'],
                         'Please enter your information here')

    def test_title_field(self):
        self.form.fields.all().delete()
        self.title = self.form.fields.create(
            type_id='title', slug='my title',
            label=u'This is on onboarding form.'
        )
        serializer = FormidableSerializer(instance=self.form)
        data = serializer.data['fields'][0]
        for field in BASE_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['label'],
                         'This is on onboarding form.')


class RenderContextSerializer(TestCase):

    def test_required_field(self):

        class TestForm(FormidableForm):
            name = fields.CharField(label=u'Your Name', accesses={
                'jedi': 'REQUIRED',
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
                'jedi': 'EDITABLE',
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
                'jedi': 'READONLY',
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
                'jedi': 'HIDDEN',
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
            'multiple': False, 'items': {
                'tutu': 'toto',
                'tata': 'plop',
            },
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
            'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
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
            'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
            'validations': [
                {
                    'type': 'IS_DATE_IN_THE_FUTURE',
                    'value': 'false',
                },
            ]
        }
    ]

    format_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'helpText',
            'helpText': 'Hello',
            'accesses': [],
        }
    ]
    format_without_field_helptext = [
        {
            'slug': 'myhelptext',
            'type_id': 'helpText',
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

    def test_create_form(self):
        serializer = FormidableSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, u'test_create')
        self.assertEquals(instance.description, u'description create')
        self.assertEquals(instance.fields.count(), 0)

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

    def test_create_helptext(self):
        data = copy.deepcopy(self.data)
        data['fields'] = self.format_field_helptext
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.fields.count(), 1)
        qs = instance.fields.filter(type_id='helpText', helpText='Hello')
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


class UpdateFormTestCase(TestCase):

    data = {
        'label': u'edited form',
        'description': 'description edited',
        'fields': [],
    }

    fields = [
        {
            'type_id': 'text', 'label': 'edited field', 'slug': 'text-slug',
            'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
            'validations': [{'type': 'MAXLENGTH', 'value': '128'}]
        }
    ]

    fields_items = [{
        'type_id': 'dropdown', 'label': 'edited field',
        'slug': 'dropdown-input', 'items': {
            'gun': u'desert-eagle',
            'sword': u'Andúril',
        },
        'accesses': [{'access_id': 'padawan', 'level': 'REQUIRED'}],
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
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level='REQUIRED'
        )
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_items)
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
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
            placeholder='put your name here', helpText=u'your name',
        )
        self.text_field.accesses.create(
            access_id='padawan', level='REQUIRED'
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
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level='EDITABLE'
        )
        self.dropdown_fields.items.create(key=u'gun', value=u'eagle')
        self.dropdown_fields.items.create(key=u'sword', value=u'excalibur')
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
        qs = field.accesses.filter(access_id='padawan', level=u'REQUIRED')
        self.assertTrue(qs.exists())

    def test_delete_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
        )
        self.dropdown_fields.items.create(key=u'gun', value=u'eagle')
        self.dropdown_fields.items.create(key=u'sword', value=u'excalibur')
        serializer = FormidableSerializer(instance=self.form, data=self.data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 0)

    def test_delete_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
        )
        self.dropdown_fields.accesses.create(
            access_id='padawan', level='REQUIRED'
        )
        self.dropdown_fields.items.create(key=u'gun', value=u'eagle')
        self.dropdown_fields.items.create(key=u'sword', value=u'excalibur')
        data = copy.deepcopy(self.data)
        data['fields'] = copy.deepcopy(self.fields_items)
        data['fields'][0]['items'] = {}
        serializer = FormidableSerializer(instance=self.form, data=data)
        self.assertTrue(serializer.is_valid())
        form = serializer.save()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.items.count(), 0)
