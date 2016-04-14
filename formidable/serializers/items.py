# -*- coding: utf-8 -*-
from rest_framework import serializers

from formidable.models import Item
from formidable.serializers.list import NestedListSerializer


class ItemListSerializer(NestedListSerializer):

    field_id = 'key'
    parent_name = 'field_id'

    def validate(self, data):
        data = super(ItemListSerializer, self).validate(data)
        for index, item in enumerate(data):
            item['order'] = index

        return data


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        list_serializer_class = ItemListSerializer
        fields = ('key', 'value', 'help_text')
