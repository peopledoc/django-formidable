# -*- coding: utf-8 -*-
from django import forms

from formidable.forms.field_builder import (
    FieldBuilder as FB, FormFieldFactory as FF
)
from formidable.validators import (
    DateValidatorFactory as DVF, ValidatorFactory as VF
)


class ValidatorFactory(VF):

    def extract_validation_attribute(self, validation):
        return validation['type'], validation['message'], validation['value']


class DateValidatorFactory(DVF):

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
    validator_factory_class = DateValidatorFactory


class ChoiceFieldBuilder(FieldBuilder):

    field_class = forms.ChoiceField

    def get_field_kwargs(self):
        kwargs = super(ChoiceFieldBuilder, self).get_field_kwargs()
        kwargs['choices'] = self.get_choices()
        return kwargs

    def get_choices(self):
        for item in self.field.get('items', []):
            yield (item['value'], item['label'])


class DropdownFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.Select

    def get_field_class(self):
        if self.field['multiple']:
            return forms.MultipleChoiceField
        return super(DropdownFieldBuilder, self).get_field_class()

    def get_widget_class(self):
        if self.field['multiple']:
            return forms.SelectMultiple
        return super(DropdownFieldBuilder, self).get_widget_class()


class RadioFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.RadioSelect


class CheckboxesFieldBuilder(ChoiceFieldBuilder):

    field_class = forms.MultipleChoiceField
    widget_class = forms.CheckboxSelectMultiple


class FormFieldFactory(FF):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
        'checkbox': CheckboxFieldBuilder,
        'checkboxes': CheckboxesFieldBuilder,
        'email': EmailFieldBuilder,
        'number': IntegerFieldBuilder,
        'file': FileFieldBuilder,
        'date': DateFieldBuilder,
        'dropdown': DropdownFieldBuilder,
        'radios': RadioFieldBuilder,
    }

    def get_type_id(self, field):
        return field['type_id']
