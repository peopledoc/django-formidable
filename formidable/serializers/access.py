# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from formidable.models import Access
from formidable.serializers.list import NestedListSerializer


class SimpleAccessSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        return [
            {'id': access_id} for access_id in data
        ]

    def to_internal_value(self, data):

        if type(data) is not list:
            raise ValidationError('Provide a list of accesses id')

        return data


class AccessListSerializer(NestedListSerializer):

    field_id = 'access_id'
    parent_name = 'field_id'

    def validate(self, data):
        accesses_id = [accesses['access_id'] for accesses in data]

        for access_id in settings.FORMIDABLE_ACCESSES:
            if access_id not in accesses_id:
                data.append({'access_id': access_id, 'level': 'EDITABLE'})

        return data


class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = ('access_id', 'level')
        list_serializer_class = AccessListSerializer

    def validate_access_id(self, value):
        if value not in settings.FORMIDABLE_ACCESSES:
            raise serializers.ValidationError(
                u'{} is unknown, valide access {}'.format(
                    value, settings.FORMIDABLE_ACCESSES
                )
            )
        return value
