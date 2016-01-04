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

    def create(self, validated_data, field):

        for data in validated_data:
            data['field_id'] = field.id
            self.child.create(data)

    def update(self, accesses, validated_data, field):

        accesses = list(accesses.order_by('access_id').all())

        validated_data = sorted(validated_data, key=lambda x: x['access_id'])

        for index, data in enumerate(validated_data):
            if field.accesses.filter(access_id=data['access_id']).exists():
                self.child.update(accesses[index], data)
            else:
                self.child.create(data)

    def validate(self, data):
        accesses_id = [accesses['access_id'] for accesses in data]

        for access_id in settings.FORMIDABLE_ACCESSES:
            if access_id not in accesses_id:
                data.append({'access_id': access_id, 'level': 'editable'})

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
