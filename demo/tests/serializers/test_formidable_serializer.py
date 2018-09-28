from django.test import TestCase

from formidable.register import FieldSerializerRegister, load_serializer
from formidable.serializers import FormidableSerializer
from formidable.serializers.fields import BASE_FIELDS, FieldSerializer

import mock


class TestCustomFieldSerializer(TestCase):
    def setUp(self):
        field_register = FieldSerializerRegister.get_instance()
        custom_type_id = 'custom_type_id'
        self.custom_type_id = custom_type_id

        @load_serializer(field_register)
        class CustomFieldSerializer(FieldSerializer):
            type_id = custom_type_id

            class Meta(FieldSerializer.Meta):
                fields = BASE_FIELDS + ('parameters', )
                config_fields = ('meta_info', 'some_another_data')

        self.custom_field_serializer_class = CustomFieldSerializer
        self.field_register = field_register
        self.schema = {
            "label": "test",
            "description": "test",
            "fields": [
                {
                    "slug": "custom-type-id",
                    "label": "Custom field",
                    "placeholder": None,
                    "description": None,
                    "defaults": [],
                    "multiple": False,
                    "config_field": "Test test test",
                    "values": [],
                    "required": False,
                    "disabled": False,
                    "isVisible": True,
                    "type_id": custom_type_id,
                    "validations": [],
                    "order": 1,
                    "meta_info": "meta",
                    "some_another_data": "some_another_data",
                    "accesses": [
                        {
                            "id": "field-access868",
                            "level": "EDITABLE",
                            "access_id": "padawan"
                        }
                    ]
                }
            ]
        }

    def test_register(self):
        self.assertIn(self.custom_type_id, self.field_register)

    def test_custom_field_serialize(self):
        serializer = FormidableSerializer(data=self.schema)
        serializer.is_valid()
        serializer.save()
        # get field instance
        self.instance = serializer.instance
        custom_field = serializer.instance.fields.first()
        # test field instance
        self.assertIn('meta_info', custom_field.parameters)
        self.assertEqual(custom_field.parameters['meta_info'], "meta")
        self.assertIn('some_another_data', custom_field.parameters)
        self.assertEqual(
            custom_field.parameters['some_another_data'],
            "some_another_data"
        )
        # get serialized data
        data = FormidableSerializer(serializer.instance).data['fields'][0]
        # test serialized data
        self.assertIn('meta_info', data)
        self.assertIn('some_another_data', data)
        self.assertIn('parameters', data)
        # remove instance
        self.instance.delete()

    def test_context_in_field_serializer(self):
        # backup a serializer
        backup_serializer = self.field_register[self.custom_type_id]
        # mock a field serializer
        mocked_serializer = mock.MagicMock()
        self.field_register[self.custom_type_id] = mock.MagicMock(
            return_value=mocked_serializer
        )
        # test serializer with an empty context
        serializer = FormidableSerializer(data=self.schema)
        serializer.is_valid()
        self.assertEqual(mocked_serializer.custom_context, {})
        # test serializer with context
        serializer = FormidableSerializer(
            data=self.schema, context={'test': 'context'}
        )
        serializer.is_valid()
        self.assertEqual(mocked_serializer.custom_context, {'test': 'context'})
        # remove mock and revert serializer
        self.field_register[self.custom_type_id] = backup_serializer

    def tearDown(self):
        self.field_register.pop(self.custom_type_id)
