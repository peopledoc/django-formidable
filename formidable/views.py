# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib

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

    def dispatch(self, request, *args, **kwargs):
        # Being forced to do this in dispatch() rather than post() because
        # ValidationErrors can be raised in dispatch and we don't go through
        # the post() method
        response = super(FormidableCreate, self).dispatch(
            request, *args, **kwargs)

        # Is the response a success or a failure?
        if request.method == 'POST':
            success = response.status_code == 201
            if success:
                callback = getattr(
                    settings, 'FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS', None)
            else:
                callback = getattr(
                    settings, 'FORMIDABLE_POST_CREATE_CALLBACK_FAIL', None)

            if callback:
                module, meth_name = callback.rsplit('.', 1)
                if six.PY3:
                    imported_module = importlib.import_module(module)
                else:
                    imported_module = importlib.import_module(
                        module, [meth_name])
                func = getattr(imported_module, meth_name)
                func(request)
        return response


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

    settings_permission_key = 'FORMIDABLE_PERMISSION_USING'

    def get_formidable_object(self, kwargs):
        return Formidable.objects.get(pk=kwargs['pk'])

    def get(self, request, **kwargs):
        try:
            formidable = self.get_formidable_object(kwargs)
        except Formidable.DoesNotExist:
            raise exceptions.Http404()

        role = get_context(request, kwargs)
        form_class = formidable.get_django_form_class(role)
        form = form_class(data=request.GET)
        if form.is_valid():
            return Response(status=204)
        else:
            return Response(form.errors, status=400)
