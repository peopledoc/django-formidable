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



class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        exclude = ('id',)
