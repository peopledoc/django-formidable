# -*- coding: utf-8 -*-
"""
This module exposes everything needed to generate a standard django form class
from a formidable object.

Given a formidable object, you can use :func:`get_dynamic_form_class` to get
its corresponding django form class.
"""
from collections import OrderedDict

from django import forms

from formidable.models import Formidable
from formidable.forms import field_builder
from formidable.forms.validations.presets import presets_register


class FormidableBoundFieldCache(dict):
    """
    In Django 1.8, bound fields are handled in the form context (__getitem__).
    However, we want to inject our own BoundField for FormatField in order to
    handle labels differently.
    This can be achieved by implementing the get_bound_field method in our
    field (available in Django >= 1.9). For now, if the method exists,
    the bound_field is switched-in at the form level.
    """
    def __setitem__(self, key, bf):
        form, field, name = bf.form, bf.field, bf.name
        if hasattr(field, 'get_bound_field'):
            bf = field.get_bound_field(form, name)
        return super(FormidableBoundFieldCache, self).__setitem__(key, bf)


class BaseDynamicForm(forms.Form):
    """
    This class is used to generate the final Django form class corresponding to
    the formidable object.

    Please do not use this class directly, rather, you should check the
    endpoint :func:`get_dynamic_form_class`
    """

    def __init__(self, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        self._bound_fields_cache = FormidableBoundFieldCache()

    def clean(self):
        cleaned_data = super(BaseDynamicForm, self).clean()
        for rule in self.rules:
            rule(cleaned_data)
        return cleaned_data


def get_dynamic_form_class(formidable, role=None, field_factory=None):
    """
    This is the main method for getting a django form class from a formidable
    object.

    .. code-block:: python

        form_obj = Formidable.objects.get(pk=42)
        django_form_class = get_dynamic_form_class(form_obj)

    The optional :params:`role` argument provides a way to get the form class
    according to the access rights you specify by role. The :params:`role` must
    be a role id, as defined by the code pointed to in
    settings.FORMIDABLE_ACCESS_RIGHTS_LOADER.

    .. code-block:: python

        form_obj = Formidable.objects.get(pk=42)
        django_form_class = get_dynamic_form_class(form_obj, role='jedi')

    """

    attrs = OrderedDict()
    field_factory = field_factory or field_builder.FormFieldFactory

    for field in formidable.fields.order_by('order').all():
        try:
            form_field = field_factory.produce(field, role)
        except field_builder.SkipField:
            pass
        else:
            attrs[field.slug] = form_field

    attrs['rules'] = presets_register.build_rules(formidable)
    return type('DynamicForm', (BaseDynamicForm,), attrs)


class FormidableForm(forms.Form):
    """
    This is the main class available to build a formidable object with Django's
    form API syntax.

    It provides a class method :meth:`to_formidable` which saves the declared
    form as a formidable objects.

    Check the formidable.forms.fields module to see what fields are available
    when defining your form.

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
