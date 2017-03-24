# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.accesses import get_accesses
from formidable.constants import EDITABLE
from formidable.models import Access
from formidable.serializers.list import NestedListSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class SimpleAccessSerializer(serializers.BaseSerializer):

    def to_representation(self, objects):
        return [
            {
                'id': access.id,
                'label': access.label,
                'description': access.description,
                'preview_as': access.preview_as,
            } for access in objects
        ]

    def to_internal_value(self, data):

        if type(data) is not list:
            raise ValidationError('Provide a list of accesses id')

        return data


class AccessListSerializer(NestedListSerializer):

    field_id = 'access_id'
    parent_name = 'field_id'

    def validate(self, data):
        data = super(AccessListSerializer, self).validate(data)
        accesses_id = [accesses['access_id'] for accesses in data]

        for access in get_accesses():
            if access.id not in accesses_id:
                data.append({'access_id': access.id, 'level': EDITABLE})

        return data


class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = ('access_id', 'level')
        list_serializer_class = AccessListSerializer

    def validate_access_id(self, value):
        accesses_ids = [access.id for access in get_accesses()]
        if value not in accesses_ids:
            raise serializers.ValidationError(
                '{value} is unknown, valid access {accesses_ids}'.format(
                    value=value, accesses_ids=accesses_ids
                )
            )
        return value
