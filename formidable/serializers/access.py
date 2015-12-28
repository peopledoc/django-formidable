# -*- coding: utf-8 -*-
from django.conf import settings

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

    def update(self, accesses, validated_data, field_id):

        accesses = list(accesses.all())

        for index, data in enumerate(validated_data):
            data['field_id'] = field_id
            self.child.update(accesses[index], data)


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
