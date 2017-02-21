# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.models import Default
from formidable.serializers.list import NestedListSerializerDummyUpdate
from rest_framework import serializers


class DefaultListSerializer(NestedListSerializerDummyUpdate):

    field_id = 'value'
    parent_name = 'field_id'


class DefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Default
        list_serializer_class = DefaultListSerializer
        fields = ('value',)

    def to_internal_value(self, data):
        return {'value': data}

    def to_representation(self, instance):
        return instance.value
