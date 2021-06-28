from django.test import TestCase

from formidable.models import Formidable
from formidable.serializers.validation import (
    MinLengthSerializer, RegexpSerializer,
    ValidationSerializer, FutureDateSerializer
)


class ValidationSerializerTest(TestCase):
    increment = 0

    def setUp(self):
        self.form = Formidable.objects.create(
            label='test', description='test'
        )
        self.increment += 1
        self.text_field = self.form.fields.create(
            type_id='text',
            slug='input-text-{}'.format(self.increment),
            label='name',
            order=1,
        )

    def test_int_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'MINLENGTH',
            'value': 5,
        }
        serializer = MinLengthSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_non_int_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'MINLENGTH',
            'value': 'test',
        }
        serializer = MinLengthSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_regexp_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'REGEXP',
            'value': r'\w+ly',
        }
        serializer = RegexpSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_regexp_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'REGEXP',
            'value': r'\w+ly(',
        }
        serializer = RegexpSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_valid_bool_future_date_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'IS_DATE_IN_THE_FUTURE',
            'value': True,
        }
        serializer = FutureDateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_string_future_date_value(self):
        data = {
            'field_id': self.text_field.id,
            'type': 'IS_DATE_IN_THE_FUTURE',
            'value': 'true',
        }
        serializer = FutureDateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_update_validations(self):
        list_serializer = ValidationSerializer(many=True)
        self.text_field.validations.create(
            type='MINLENGTH',
            value='5',
        )
        list_serializer.update(
            self.text_field.validations,
            self.text_field,
            [{
                'type': 'MINLENGTH',
                'value': '12'
            }],
        )
        self.assertEquals(self.text_field.validations.count(), 1)
        validation = self.text_field.validations.first()
        self.assertEquals(validation.value, '12')
