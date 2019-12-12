import json
from os.path import join, dirname

from django.test import TestCase, override_settings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from formidable.forms import get_dynamic_form_class_from_schema
from formidable.forms.field_builder import FormFieldFactory
from formidable.register import FieldSerializerRegister, load_serializer

from demo.extra_field_toolbox import (
    ColorPickerFieldBuilder,
    ColorPickerFieldSerializer as BaseColorPickerFieldSerializer
)


class ExtraLoadingTestCase(TestCase):

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={})
    def test_field_factory_empty_settings(self):
        factory = FormFieldFactory()
        self.assertEqual(
            set(factory.field_map.keys()),
            set(factory.map.keys())
        )

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS=None)
    def test_field_factory_none_settings(self):
        factory = FormFieldFactory()
        self.assertEqual(
            set(factory.field_map.keys()),
            set(factory.map.keys())
        )

    @override_settings()
    def test_field_factory_no_settings(self):
        del settings.FORMIDABLE_EXTERNAL_FIELD_BUILDERS
        factory = FormFieldFactory()
        self.assertEqual(
            set(factory.field_map.keys()),
            set(factory.map.keys())
        )

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={
                       'color_picker': 'demo.extra_field_toolbox'
                                       '.ColorPickerFieldBuilder'})
    def test_field_factory_settings_color_picker(self):
        factory = FormFieldFactory()
        self.assertEqual(
            set(factory.field_map.keys()).union(['color_picker']),
            set(factory.map.keys())
        )
        field_builder_class = factory.map['color_picker']
        self.assertEqual(field_builder_class, ColorPickerFieldBuilder)

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={
                       'color_picker': 'is.inexistant.Class'})
    def test_field_factory_settings_inexistant(self):
        with self.assertRaises(ImportError):
            FormFieldFactory()

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={
                       'color_picker': 'django.forms.CharField'})
    def test_field_factory_settings_not_field_builder(self):
        with self.assertRaises(ImproperlyConfigured):
            FormFieldFactory()


class FillFormWithExtraFieldTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.custom_type_id = 'color_picker'
        self.field_register = FieldSerializerRegister.get_instance()

        @load_serializer(self.field_register)
        class ColorPickerFieldSerializer(BaseColorPickerFieldSerializer):
            pass

        path = join(
            dirname(__file__), 'fixtures', 'form-schema-extra-fields.json')
        with open(path) as fd:
            self.schema_data = json.load(fd)

    def tearDown(self):
        super().tearDown()
        self.field_register.pop(self.custom_type_id)

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={
                       'color_picker': 'demo.extra_field_toolbox'
                                       '.ColorPickerFieldBuilder'})
    def test_color_picker_validation_rgb(self):
        form_class = get_dynamic_form_class_from_schema(self.schema_data)

        # Valid color, according to our validator
        form = form_class(data={"favorite-color": "blue"})
        self.assertTrue(form.is_valid())

        # Invalid color
        form = form_class(data={"favorite-color": "meuh"})
        self.assertFalse(form.is_valid())
        self.assertIn('favorite-color', form.errors)

    @override_settings(FORMIDABLE_EXTERNAL_FIELD_BUILDERS={
                       'color_picker': 'demo.extra_field_toolbox'
                                       '.ColorPickerFieldBuilder'})
    def test_color_picker_validation_hex(self):
        schema_data = self.schema_data.copy()
        schema_data['fields'][0]['parameters']['color_format'] = 'hex'
        form_class = get_dynamic_form_class_from_schema(schema_data)

        # Valid HEX color
        form = form_class(data={"favorite-color": "#123456"})
        self.assertTrue(form.is_valid())

        # Bad HEX format
        form = form_class(data={"favorite-color": "#tt1234"})
        self.assertFalse(form.is_valid())
        self.assertIn('favorite-color', form.errors)

        # RGB != hex
        form = form_class(data={"favorite-color": "blue"})
        self.assertFalse(form.is_valid())
        self.assertIn('favorite-color', form.errors)
