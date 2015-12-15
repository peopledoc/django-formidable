# -*- coding: utf-8 -*-
from django.test import TestCase

from formidable.models import Formidable
from formidable.serializers.forms import FormidableSerializer
from formidable.serializers.fields import BASE_FIELDS, SerializerRegister


class SerializerTestCase(TestCase):

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
