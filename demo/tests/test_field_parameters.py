from django.test import TestCase

from formidable.forms import FormidableForm
from formidable.register import FieldSerializerRegister, load_serializer

from demo.extra_field_toolbox import ColorPickerField
from demo.extra_field_toolbox import (
    ColorPickerFieldSerializer as BaseColorPickerFieldSerializer
)


class WithParametrizedField(FormidableForm):
    "Form with Parametrized field"
    field = ColorPickerField(parameters={"color_format": "hex"})


class TestToFormidableParametrizedField(TestCase):

    def setUp(self):
        super().setUp()
        self.field_register = FieldSerializerRegister.get_instance()

        @load_serializer(self.field_register)
        class ColorPickerFieldSerializer(BaseColorPickerFieldSerializer):
            pass

    def tearDown(self):
        super().tearDown()
        self.field_register.pop(BaseColorPickerFieldSerializer.type_id)

    def test_to_formidable(self):
        formidable_form = WithParametrizedField.to_formidable(
            label="Form"
        )
        field = formidable_form.fields.first()
        self.assertEqual(field.parameters, {"color_format": 'hex'})

    def test_to_json(self):
        formidable_form = WithParametrizedField.to_formidable(
            label="Form"
        )
        form_schema = formidable_form.to_json()
        field = form_schema['fields'][0]
        self.assertEqual(field['parameters'], {'color_format': 'hex'})
