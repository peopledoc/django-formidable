# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms

from formidable.models import Formidable
from formidable.forms import field_builder
from formidable.forms.validations.presets import presets_register


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

    def clean(self):
        cleaned_data = super(BaseDynamicForm, self).clean()
        for rule in self.rules:
            rule(cleaned_data)
        return cleaned_data


def get_dynamic_form_class(formidable, role=None):

    attrs = OrderedDict()

    for field in formidable.fields.order_by('order').all():
        try:
            form_field = field_builder.FormFieldFactory.produce(field, role)
        except field_builder.SkipField:
            pass
        else:
            attrs[field.slug] = form_field

    attrs['rules'] = presets_register.build_rules(formidable)
    return type('DynamicForm', (BaseDynamicForm,), attrs)


class FormidableForm(forms.Form):

    @classmethod
    def to_formidable(cls, label, description=u''):
        form = Formidable.objects.create(label=label, description=description)
        order = 0
        for slug, field in cls.declared_fields.items():
            field.to_formidable(form, order, slug)
            order += 1
        return form
