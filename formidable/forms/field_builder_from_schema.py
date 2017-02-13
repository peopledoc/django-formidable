# -*- coding: utf-8 -*-
from django import forms

from formidable.forms.field_builder import (
    FieldBuilder as FB, FormFieldFactory as FF
)
from formidable.validators import ValidatorFactory as VF


class ValidatorFactory(VF):

    def extract_validation_attribute(self, validation):
        return validation['type'], validation['message'], validation['value']


class FieldBuilder(FB):

    field_class = forms.CharField
    widget_class = None
    validator_factory_class = ValidatorFactory

    def get_required(self):
        return self.field['required']

    def get_disabled(self):
        return self.field['disabled']

    def get_label(self):
        return self.field['label']

    def get_help_text(self):
        return self.field['description']

    def get_validations(self):
        return self.field['validations']

    def get_accesses(self, role):
        # No need to compute accesses, the schema is already contextualized.
        return None


class TextFieldBuilder(FieldBuilder):

    widget_class = forms.TextInput


class ParagraphFieldBuilder(FieldBuilder):

    widget_class = forms.Textarea


class CheckboxFieldBuilder(FieldBuilder):
    field_class = forms.BooleanField


class EmailFieldBuilder(FieldBuilder):
    field_class = forms.EmailField


class IntegerFieldBuilder(FieldBuilder):
    field_class = forms.IntegerField


class FileFieldBuilder(FieldBuilder):
    field_class = forms.FileField


class DateFieldBuilder(FieldBuilder):
    field_class = forms.DateField


class FormFieldFactory(FF):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
        'checkbox': CheckboxFieldBuilder,
        'email': EmailFieldBuilder,
        'number': IntegerFieldBuilder,
        'file': FileFieldBuilder,
        'date': DateFieldBuilder,
    }

    def get_type_id(self, field):
        return field['type_id']
