# -*- coding: utf-8 -*-
from django import forms

from formidable.models import Formidable
from formidable.forms import field_builder


class BaseDynamicForm(forms.Form):
    pass


def get_dynamic_form_class(formidable, role=None):

    fields = {}

    for field in formidable.fields.all():
        try:
            form_field = field_builder.FormFieldFactory.produce(field, role)
        except field_builder.SkipField:
            pass
        else:
            fields[field.slug] = form_field

    return type('DynamicForm', (BaseDynamicForm,), fields)


class FormidableForm(forms.Form):

    @classmethod
    def to_formidable(cls, label, description=u''):
        form = Formidable.objects.create(label=label, description=description)
        for slug, field in cls.declared_fields.items():
            field.to_formidable(form, slug)
        return form
