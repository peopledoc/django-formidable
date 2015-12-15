# -*- coding: utf-8 -*-

from rest_framework import serializers

from formidable.models import Item


class ListItemSerializer(serializers.ListSerializer):

    def to_representation(self, items):
        return {
            item.key: item.value for item in items.all()
        }


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        list_serializer_class = ListItemSerializer
        fields = ('key', 'value')
