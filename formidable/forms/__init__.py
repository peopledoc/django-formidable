# -*- coding: utf-8 -*-
from django import forms

from formidable.forms.field_builder import FormFieldFactory, SkipField


class BaseDynamicForm(forms.Form):
    pass


def get_dynamic_form_class(formidable, role=None):

    fields = {}

    for field in formidable.fields.all():
        try:
            form_field = FormFieldFactory.produce(field, role)
        except SkipField:
            pass
        else:
            fields[field.slug] = form_field

    return type('DynamicForm', (BaseDynamicForm,), fields)
