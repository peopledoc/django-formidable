# -*- coding: utf-8 -*-

from django.forms import fields
from formidable.forms import widgets


class Field(fields.Field):

    widget = widgets.TextInput

    def to_formidable(self, form, slug):
        label = self.label or slug
        kwargs = {
            'formidable': form, 'slug': slug, 'label': label,
            'help_text': self.help_text,

        }
        kwargs.update(self.get_extra_formidable_kwargs())
        widget = self.get_widget()
        widget.to_formidable(**kwargs)

    def get_widget(self):
        return self.widget

    def get_extra_formidable_kwargs(self):
        return {}


class CharField(Field, fields.CharField):
    pass


class ChoiceField(Field, fields.ChoiceField):

    widget = widgets.Select

    def get_extra_formidable_kwargs(self):
        kwargs = super(ChoiceField, self).get_extra_formidable_kwargs()
        kwargs['items'] = self.choices
        return kwargs


class BooleanField(Field, fields.BooleanField):

    widget = widgets.CheckboxInput
