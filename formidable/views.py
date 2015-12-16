# -*- coding: utf-8 -*-

from rest_framework.generics import RetrieveAPIView, CreateAPIView

from formidable.models import Formidable
from formidable.serializers import FormidableSerializer


class FormidableDetail(RetrieveAPIView):

    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer

    def get_queryset(self):
        qs = super(FormidableDetail, self).get_queryset()
        return qs.prefetch_related('fields')


class FormidableUpdate(CreateAPIView):
    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer

    def create(self, *args, **kwargs):
        return super(FormidableUpdate, self).create(*args, **kwargs)
