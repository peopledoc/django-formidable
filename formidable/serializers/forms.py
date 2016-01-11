# -*- coding: utf-8 -*-
from django.utils.functional import cached_property

from rest_framework import serializers

from formidable.models import Formidable
from formidable.serializers.fields import FieldidableSerializer


class FormidableSerializer(serializers.ModelSerializer):

    fields = FieldidableSerializer(many=True)

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields', 'id')
        depth = 2
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        fields_kwargs = validated_data.pop('fields')
        form = Formidable.objects.create(**validated_data)
        self.fields_serializer.create(form, fields_kwargs)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self.fields_serializer.update(
            instance.fields, instance, fields_data,
        )
        return instance

    @cached_property
    def fields_serializer(self):
        return self.fields['fields']
