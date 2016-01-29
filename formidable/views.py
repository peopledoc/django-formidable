# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response

from formidable.models import Formidable
from formidable.serializers import FormidableSerializer, SimpleAccessSerializer
from formidable.serializers.forms import ContextFormSerializer
from formidable.accesses import get_accesses, get_context


class FormidableDetail(RetrieveUpdateAPIView):

    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer

    def get_queryset(self):
        qs = super(FormidableDetail, self).get_queryset()
        return qs.prefetch_related('fields')


class FormidableCreate(CreateAPIView):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer


class ContextFormDetail(RetrieveAPIView):
    queryset = Formidable.objects.all()
    serializer_class = ContextFormSerializer

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
