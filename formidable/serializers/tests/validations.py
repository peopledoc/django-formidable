# -*- coding: utf-8 -*-

from django.test import TestCase

from formidable.models import Formidable
from formidable.serializers.validation import (
    MinLengthSerializer, RegexpSerializer
)


class ValidationSerializerTest(TestCase):

    def setUp(self):
        super(ValidationSerializerTest, self).setUp()
        self.form = Formidable.objects.create(
            label=u'test', description=u'test'
        )
        self.text = self.form.fields.create(
            type_id=u'text', slug=u'input-text', label=u'name',
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
            'field_id': self.text.id, 'value': u'\w+ly', 'type': 'minlength'
        }
        serializer = RegexpSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_regexp_value(self):
        data = {
            'field_id': self.text.id, 'value': u'\w+ly(', 'type': 'minlength'
        }
        serializer = RegexpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
