# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch

import six
from rest_framework import exceptions
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
)
from rest_framework.response import Response
from rest_framework.settings import import_from_string, perform_import
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

logger = logging.getLogger(__name__)


def extract_function(func_name):
    """
    Return a function out of a namespace

    Return None if the function is not loadable
    """
    func = None
    try:
        func = import_from_string(func_name, '')
    except (ImportError, ValueError):
        logger.error(
            "An error has occurred impossible to import %s", func_name
        )
    return func


def check_callback_configuration():
    settings_names = (
        'FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS',
        'FORMIDABLE_POST_UPDATE_CALLBACK_FAIL',
        'FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS',
        'FORMIDABLE_POST_CREATE_CALLBACK_FAIL',
    )
    settings_values = map(
        lambda k: (k, getattr(settings, k, None)),
        settings_names)
    settings_values = filter(lambda item: item[1], settings_values)
    for key, value in settings_values:
        func = extract_function(value)
        if not func:
            raise ImproperlyConfigured(
                "Settings {} points to a non-existant function: `{}`".format(
                    key, value))
    return True


class CallbackMixin(object):
    success_callback_settings = ''
    failure_callback_settings = ''
    callback_error_message = "An error has occurred with function: `%s`"

    def _call_callback(self, callback):
        """
        Tool to simply call the callback function and handle edge-cases.

        **WARNING!** the DRF request is not inherited from django core,
        `HTTPRequest`, and you should not assume they'll behave the same way.

        If you need the "true" HTTPRequest object,
        use ``self.request._request`` in your callback functions.
        """
        # If there's no callback value, it's pointless to try to extract it
        if not callback:
            return

        func = extract_function(callback)
        # Call function only if existing
        if not func:
            return
        try:
            # WARNING! the DRF request is not inherited from django core,
            # `HTTPRequest`, and you should not assume they'll behave the same
            # way.
            # If you need the "true" HTTPRequest object, use
            # ``self.request._request``
            func(self.request)
        except Exception:
            logger.error(
                self.callback_error_message, callback
            )

    def success_callback(self):
        """
        Call the failure callback function
        """
        callback = getattr(settings, self.success_callback_settings, None)
        self._call_callback(callback)

    def failure_callback(self):
        """
        Call the failure callback function
        """
        # Extract the callback function
        callback = getattr(settings, self.failure_callback_settings, None)
        self._call_callback(callback)

    def perform_create(self, serializer):
        response = super(CallbackMixin, self).perform_create(serializer)
        self.success_callback()
        return response

    def perform_update(self, serializer):
        "Perform update (overridden to handle callbacks)"
        response = super(CallbackMixin, self).perform_update(serializer)
        self.success_callback()
        return response

    def handle_exception(self, exc):
        "Handle errors/exceptions (overridden to handle callbacks)"
        response = super(CallbackMixin, self).handle_exception(exc)
        # Don't bother with the callback if it was a wrong method
        if isinstance(exc, exceptions.MethodNotAllowed):
            return response
        self.failure_callback()
        return response


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
                       CallbackMixin, RetrieveUpdateAPIView)):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'
    success_callback_settings = 'FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS'
    failure_callback_settings = 'FORMIDABLE_POST_UPDATE_CALLBACK_FAIL'

    def get_queryset(self):
        qs = super(FormidableDetail, self).get_queryset()
        field_qs = Field.objects.order_by('order')
        return qs.prefetch_related(Prefetch('fields', queryset=field_qs))


class FormidableCreate(six.with_metaclass(MetaClassView,
                       CallbackMixin, CreateAPIView)):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_BUILDER'
    success_callback_settings = 'FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS'
    failure_callback_settings = 'FORMIDABLE_POST_CREATE_CALLBACK_FAIL'


class ContextFormDetail(six.with_metaclass(MetaClassView, RetrieveAPIView)):

    queryset = Formidable.objects.all()
    serializer_class = ContextFormSerializer
    settings_permission_key = 'FORMIDABLE_PERMISSION_USING'

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
