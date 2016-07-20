# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from formidable.models import Formidable
from formidable.serializers.validation import (
    MinLengthSerializer, RegexpSerializer,
    ValidationSerializer
)


class ValidationSerializerTest(TestCase):

    def setUp(self):
        super(ValidationSerializerTest, self).setUp()
        self.form = Formidable.objects.create(
            label='test', description='test'
        )
        self.text = self.form.fields.create(
            type_id='text', slug='input-text', label='name',
        )

    def test_int_value(self):
        data = {'field_id': self.text.id, 'value': 5, 'type': 'minlength'}
        serializer = MinLengthSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_non_int_value(self):
        data = {'field_id': self.text.id, 'value': 'test', 'type': 'minlength'}
        serializer = MinLengthSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_regexp_value(self):
        data = {
            'field_id': self.text.id, 'value': '\w+ly', 'type': 'minlength'
        }
        serializer = RegexpSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_regexp_value(self):
        data = {
            'field_id': self.text.id, 'value': '\w+ly(', 'type': 'minlength'
        }
        serializer = RegexpSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_update_validations(self):
        list_serializer = ValidationSerializer(many=True)
        self.text.validations.create(
            value='5', type='minlength'
        )
        list_serializer.update(
            self.text.validations,
            [{'type': 'minlength', 'value': '12'}],
            self.text
        )
        self.assertEquals(self.text.validations.count(), 1)
        validation = self.text.validations.first()
        self.assertEquals(validation.value, '12')
