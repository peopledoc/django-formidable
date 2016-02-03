# -*- coding: utf-8 -*-
from django import forms

from formidable.models import Formidable
from formidable.forms import field_builder


class FormidableBoundFieldCache(dict):
    """
    In django 1.8 boundfield per field are handle in the form context
    (__getitem__).
    But, we want to inject our own BoundField for FormatField in order to
    handle label differently.
    This goal is reached by implementing in our field get_bound_field
    (available in django >= 1.9), for the moment the if the method exist
    the bound_field is switched in the form level.
    """
    def __setitem__(self, key, bf):
        form, field, name = bf.form, bf.field, bf.name
        if hasattr(field, 'get_bound_field'):
            bf = field.get_bound_field(form, name)
        return super(FormidableBoundFieldCache, self).__setitem__(key, bf)


class BaseDynamicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        self._bound_fields_cache = FormidableBoundFieldCache()


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
