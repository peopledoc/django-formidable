# -*- coding: utf-8 -*-

from django.forms import fields
from formidable.forms import widgets


class Field(fields.Field):

    widget = widgets.TextInput

    def to_formidable(self, form, slug):
        label = self.label or slug
        return self.widget.to_formidable(form, slug, label)


class CharField(Field, fields.CharField):
    pass
