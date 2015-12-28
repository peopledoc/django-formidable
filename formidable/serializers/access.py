# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from formidable.models import Access


class SimpleAccessSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        return [
            {'id': access_id} for access_id in data
        ]

    def to_internal_value(self, data):

        if type(data) is not list:
            raise ValidationError('Provide a list of accesses id')

        return data


class AccessListSerializer(serializers.ListSerializer):

    def create(self, validated_data, field_id):
        for data in validated_data:
            data['field_id'] = field_id
            self.child.create(data)


class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = ('access_id', 'level')
        list_serializer_class = AccessListSerializer
