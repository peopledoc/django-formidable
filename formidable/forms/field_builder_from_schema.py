# -*- coding: utf-8 -*-
from django import forms

from formidable.forms.field_builder import (
    FieldBuilder as FB, FormFieldFactory as FF
)


class FieldBuilder(FB):

    field_class = forms.CharField
    widget_class = None

    def get_required(self):
        return self.field['required']

    def get_disabled(self):
        return self.field['disabled']

    def get_label(self):
        return self.field['label']

    def get_help_text(self):
        return self.field['description']

    def get_validators(self):
        return []


class TextFieldBuilder(FieldBuilder):

    widget_class = forms.TextInput


class ParagraphFieldBuilder(FieldBuilder):

    widget_class = forms.Textarea


class FormFieldFactory(FF):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
    }

    def get_type_id(self, field):
        return field['type_id']
