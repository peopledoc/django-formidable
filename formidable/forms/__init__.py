# -*- coding: utf-8 -*-
"""
This module expose entire part to get a standard django form class from
a formidable object.

The main end point to consider is :func:`get_dynamic_form_class`, with this
function and given a formidable object, you can get the django form class
corresponding to form built.
"""
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
    """
    This class is used to build the final django form class corresponding to
    the formidable object. Please do not use directly this class, consider the
    end point :func:`get_dynamic_form_class`
    """

    def __init__(self, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        self._bound_fields_cache = FormidableBoundFieldCache()

    def clean(self):
        cleaned_data = super(BaseDynamicForm, self).clean()
        for rule in self.rules:
            rule(cleaned_data)
        return cleaned_data


def get_dynamic_form_class(formidable, role=None):
    """
    This is the main method to get a django form class corresponding to
    a formidable object.

    .. code-block:: python

        form_obj = Formidable.objects.get(pk=42)
        django_form_class = get_dynamic_form_class(form_obj)

    The optional role argument provides to you a way to get the form class
    according to access you specify by role. The :params:`role` has be
    a role id defined by yourself.

    .. code-block:: python

        form_obj = Formidable.objects.get(pk=42)
        django_form_class = get_dynamic_form_class(form_obj, role='jedi')

    """

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
    """
    This is the main class available to build a formidable object with django
    syntax form API. Its provides a classmethod :meth:`to_formidable` in order
    to save the declared form as a formidable objects.

    Consider the fields declared in formidable.forms.fields module in order to
    describe your form.


    .. code-block:: python

        from formidable.forms import FormidableForm, fields


        class MyForm(FormidableForm):
            name = fields.CharField()
            first_name = fields.CharField()

        formidable_instance = MyForm.to_formidable()

    """

    @classmethod
    def to_formidable(cls, label, description=u''):
        form = Formidable.objects.create(label=label, description=description)
        order = 0
        for slug, field in cls.declared_fields.items():
            field.to_formidable(form, order, slug)
            order += 1
        return form
