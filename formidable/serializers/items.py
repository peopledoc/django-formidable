# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.models import Item
from formidable.serializers.list import NestedListSerializer
from rest_framework import serializers


class ItemListSerializer(NestedListSerializer):

    field_id = 'value'
    parent_name = 'field_id'

    def validate(self, data):
        data = super(ItemListSerializer, self).validate(data)
        for index, item in enumerate(data):
            item['order'] = index

        return data


class ItemSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False, allow_null=True,
                                        allow_blank=True, source='help_text')

    def to_internal_value(self, data):
        # XXX FIX ME: temporary fix
        if 'help_text' in data:
            data['description'] = data.pop('help_text')
        return super(ItemSerializer, self).to_internal_value(data)

    class Meta:
        model = Item
        list_serializer_class = ItemListSerializer
        fields = ('value', 'label', 'description')
