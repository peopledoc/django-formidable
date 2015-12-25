# -*- coding: utf-8 -*-
import copy

from django.test import TestCase

from formidable.models import Formidable
from formidable.serializers.forms import FormidableSerializer
from formidable.serializers.fields import BASE_FIELDS, SerializerRegister


class RenderSerializerTestCase(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(
            label=u'testform', description=u'test form',
        )
        self.text_field = self.form.fields.create(
            type_id='text', label='test text',
            placeholder='put your name here', helptext=u'your name',
        )
        self.serializer = FormidableSerializer(instance=self.form)

    def test_ok(self):
        self.assertTrue(self.serializer.data)

    def test_register(self):
        register = SerializerRegister.get_instance()
        assert len(register) == 11

    def test_form_field(self):
        data = self.serializer.data
        self.assertIn('label', data)
        self.assertEquals(data['label'], u'testform')
        self.assertIn('description', data)
        self.assertEquals(data['description'], u'test form')

    def test_fields(self):
        data = self.serializer.data
        self.assertIn('fields', data)
        self.assertEquals(len(data['fields']), 1)

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
        self.assertEquals(text_field['helptext'], 'your name')
        self.assertEquals(text_field['default'], None)
        self.assertNotIn('multiple', text_field)
        self.assertNotIn('items', text_field)

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


class CreateSerializerTestCase(TestCase):

    data = {
        'label': u'test_create',
        'description': u'description create',
        'fields': []
    }
    fields_without_items = [
        {'slug': 'text_input', 'label': 'text label', 'type_id': 'text'}
    ]

    fields_with_items = [
        {
            'type_id': 'dropdown',
            'slug': 'dropdown-input', 'label': 'dropdown label',
            'multiple': False, 'items': {
                'tutu': 'toto',
                'tata': 'plop',
            }
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
        data['fields'] = self.fields_without_items
        serializer = FormidableSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.label, u'test_create')
        self.assertEquals(instance.description, u'description create')
        self.assertEquals(instance.fields.count(), 1)
        field = instance.fields.first()
        self.assertEquals(field.type_id, 'text')
        self.assertEquals(field.label, 'text label')
        self.assertEquals(field.slug, 'text_input')
        field.items.all()

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

    def test_create_field_without_items(self):
        data = copy.deepcopy(self.data)
        fields = copy.deepcopy(self.fields_with_items)
        fields[0].pop('items')
        data['fields'] = fields
        serializer = FormidableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fields', serializer.errors)


class UpdateFormTestCase(TestCase):

    data = {
        'label': u'edited form',
        'description': 'description edited',
        'fields': [],
    }

    fields = [
        {'type_id': 'text', 'label': 'edited field', 'slug': 'text-slug'}
    ]

    fields_items = [{
        'type_id': 'dropdown', 'label': 'edited field',
        'slug': 'dropdown-input', 'items': {
            'gun': u'desert-eagle',
            'sword': u'Andúril',
        }
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

    def test_create_items_on_update(self):
        self.dropdown_fields = self.form.fields.create(
            slug='dropdown-input', type_id='dropdown', label=u'weapons',
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
            placeholder='put your name here', helptext=u'your name',
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
