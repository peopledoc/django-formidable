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
        fields_kwargs = None
        if 'fields' in validated_data:
            fields_kwargs = validated_data.pop('fields')

        form = Formidable.objects.create(**validated_data)

        if fields_kwargs:
            field_serializer = self.fields['fields']
            field_serializer.create(fields_kwargs, form.id)

        return form
