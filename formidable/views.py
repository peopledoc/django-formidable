# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models import Prefetch

import six
from rest_framework import exceptions
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
)
from rest_framework.response import Response
from rest_framework.settings import perform_import
from rest_framework.views import APIView

from formidable.accesses import get_accesses, get_context
from formidable.forms.field_builder import (
    FileFieldBuilder, FormFieldFactory, SkipField
)
from formidable.forms.validations.presets import presets_register
from formidable.models import Field, Formidable
from formidable.serializers import FormidableSerializer, SimpleAccessSerializer
from formidable.serializers.forms import ContextFormSerializer
from formidable.serializers.presets import PresetsSerializer


class MetaClassView(type):
    """
    Automatically load the *list* of permissions defined in the settings.
    The key is defined in the ``settings_permissions_keys`` class
    attribute.

    If the ``settings_permissions_key`` is not defined, the default
    setting key is: ``FORMIDABLE_DEFAULT_PERMISSIONS``.
    If this default setting key is not defined either, the most
    restricted permission is fetched (e.g. the ``NoOne`` permissions
    access)
    .
    """

    def __new__(mcls, name, bases, attrs):

        if 'permission_classes' not in attrs:
            settings_key = attrs.get(
                'settings_permission_key', 'FORMIDABLE_DEFAULT_PERMISSION'
            )

            # If the settings key define is not present in the settings
            # The ``NoOne`` permission is loaded.
            modules = getattr(settings, settings_key,
                      getattr(settings, 'FORMIDABLE_DEFAULT_PERMISSION',  # noqa
                      ['formidable.permissions.NoOne']))                  # noqa

            permissions_classes = perform_import(modules, None)
            attrs['permission_classes'] = permissions_classes
        return super(MetaClassView, mcls).__new__(mcls, name, bases, attrs)


class FormidableDetail(six.with_metaclass(MetaClassView,
                       RetrieveUpdateAPIView)):

    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'

    def get_queryset(self):
        qs = super(FormidableDetail, self).get_queryset()
        field_qs = Field.objects.order_by('order')
        return qs.prefetch_related(Prefetch('fields', queryset=field_qs))


class FormidableCreate(six.with_metaclass(MetaClassView, CreateAPIView)):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'


class ContextFormDetail(six.with_metaclass(MetaClassView, RetrieveAPIView)):

    queryset = Formidable.objects.all()
    serializer_class = ContextFormSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_USING'

    def get_queryset(self):
        qs = super(ContextFormDetail, self).get_queryset()
        field_qs = Field.objects.order_by('order')
        return qs.prefetch_related(Prefetch('fields', queryset=field_qs))

    def get_serializer_context(self):
        context = super(ContextFormDetail, self).get_serializer_context()
        context['role'] = get_context(self.request, self.kwargs)
        return context


class AccessList(six.with_metaclass(MetaClassView, APIView)):

    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'

    def get(self, request, format=None):
        serializer = SimpleAccessSerializer(data=get_accesses())
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors, status_code=400)


class PresetsList(six.with_metaclass(MetaClassView, APIView)):

    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'

    def get(self, request, format=None):
        presets_declarations = [
            klass([]) for klass in presets_register.values()
        ]
        serializer = PresetsSerializer(
            many=True,
            instance=presets_declarations
        )
        return Response(serializer.data)


class ValidateView(six.with_metaclass(MetaClassView, APIView)):
    """
    This view is usually called by the UI front-end in order to validate
    data inside a form to avoid uploading file.
    The main idea is to call this view in order to validate the entire data
    except the File part. The UI front-end is not able to compute complex
    validation (through validation presets), and to avoid heavy files exchanges
    this view can validate first the data (without the file).

    The final errors in the form are sent to UI in order to display it.
    """

    settings_permission_key = 'FORMIDABLE_PERMISSION_USING'

    class ValidationFileFieldBuilder(FileFieldBuilder):

        def build(self, role):
            raise SkipField

    def get_formidable_object(self, kwargs):
        return Formidable.objects.get(pk=kwargs['pk'])

    def get(self, request, **kwargs):
        try:
            formidable = self.get_formidable_object(kwargs)
        except Formidable.DoesNotExist:
            raise exceptions.Http404()

        form_class = self.get_form_class(formidable)
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, formidable):
        return formidable.get_django_form_class(
            **self.get_form_class_kwargs()
        )

    def get_form_class_kwargs(self):
        factory = FormFieldFactory(
            field_map={'file': self.ValidationFileFieldBuilder}
        )
        return {
            'role': get_context(self.request, self.kwargs),
            'field_factory': factory,
        }

    def form_valid(self, form):
        return Response(status=204)

    def form_invalid(self, form):
        return Response(form.errors, status=400)

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        return {'data': self.request.GET}
