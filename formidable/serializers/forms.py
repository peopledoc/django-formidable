# -*- coding: utf-8 -*-

from rest_framework import serializers

from formidable.models import Formidable
from formidable.serializers import fields
from formidable.serializers.common import WithNestedSerializer
from formidable.serializers.presets import PresetModelSerializer


class FormidableSerializer(WithNestedSerializer):

    fields = fields.FieldidableSerializer(many=True)
    presets = PresetModelSerializer(many=True, required=False)

    nested_objects = ['fields', 'presets']

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields', 'id', 'presets')
        depth = 2
        extra_kwargs = {'id': {'read_only': True}}


class ContextFormSerializer(serializers.ModelSerializer):

    fields = fields.ContextFieldSerializer(read_only=True, many=True)

    class Meta:
        model = Formidable
        fields = ('id', 'label', 'description', 'fields')
        depth = 2

    def __init__(self, *args, **kwargs):
        super(ContextFormSerializer, self).__init__(*args, **kwargs)
        self.fields['fields'].set_context('role', self._context['role'])
