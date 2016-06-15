# -*- coding: utf-8 -*-
from rest_framework import serializers

from formidable.models import Item
from formidable.serializers.list import NestedListSerializer


class ItemListSerializer(NestedListSerializer):

    field_id = 'value'
    parent_name = 'field_id'

    def validate(self, data):
        data = super(ItemListSerializer, self).validate(data)
        for index, item in enumerate(data):
            item['order'] = index

        return data

    def to_representation(self, items):
        return super(ItemListSerializer, self).to_representation(
            items.order_by('order')
        )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        list_serializer_class = ItemListSerializer
        fields = ('value', 'label', 'help_text')
