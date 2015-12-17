# -*- coding: utf-8 -*-

from rest_framework import serializers

from formidable.models import Formidable
from formidable.serializers.fields import FieldidableSerializer


class FormidableSerializer(serializers.ModelSerializer):

    fields = FieldidableSerializer(many=True)

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields')
        depth = 2

    def create(self, validated_data):
        return Formidable.objects.create(**validated_data)
