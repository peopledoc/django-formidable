# -*- coding: utf-8 -*-

from django.db.models import Prefetch

from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework import exceptions

from formidable.models import Formidable, Field
from formidable.serializers import FormidableSerializer, SimpleAccessSerializer
from formidable.serializers.forms import ContextFormSerializer
from formidable.accesses import get_accesses, get_context
from formidable.serializers.presets import PresetsSerializer
from formidable.forms.validations.presets import presets_register


class FormidableDetail(RetrieveUpdateAPIView):

    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer

    def get_queryset(self):
        qs = super(FormidableDetail, self).get_queryset()
        field_qs = Field.objects.order_by('order')
        return qs.prefetch_related(Prefetch('fields', queryset=field_qs))


class FormidableCreate(CreateAPIView):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer


class ContextFormDetail(RetrieveAPIView):
    queryset = Formidable.objects.all()
    serializer_class = ContextFormSerializer

    def get_queryset(self):
        qs = super(ContextFormDetail, self).get_queryset()
        field_qs = Field.objects.order_by('order')
        return qs.prefetch_related(Prefetch('fields', queryset=field_qs))

    def get_serializer_context(self):
        context = super(ContextFormDetail, self).get_serializer_context()
        context['role'] = get_context(self.request, self.kwargs)
        return context


class AccessList(APIView):

    def get(self, request, format=None):
        serializer = SimpleAccessSerializer(data=get_accesses())
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors, status_code=400)


class PresetsList(APIView):

    def get(self, request, format=None):
        presets_declarations = [
            klass([]) for klass in presets_register.values()
        ]
        serializer = PresetsSerializer(
            many=True,
            instance=presets_declarations
        )
        return Response(serializer.data)


class ValidateView(APIView):

    def get(self, request, **kwargs):
        try:
            formidable = Formidable.objects.get(pk=kwargs['pk'])
        except Formidable.DoesNotExist:
            raise exceptions.Http404()

        role = get_context(request, kwargs)
        form_class = formidable.get_django_form_class(role)
        form = form_class(data=request.GET)
        if form.is_valid():
            return Response(status=204)
        else:
            return Response(form.errors, status=400)
