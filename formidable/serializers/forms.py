# -*- coding: utf-8 -*-
from django.utils.functional import cached_property

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
        fields_kwargs = validated_data.pop('fields')
        form = Formidable.objects.create(**validated_data)
        self.fields_serializer.create(fields_kwargs, form.id)
        return form

    def update(self, instance, validated_data):
        field_kwargs = validated_data.pop('fields')
        super(FormidableSerializer, self).update(instance, validated_data)
        self.fields_serializer.update(
            instance.fields, field_kwargs
        )

    @cached_property
    def fields_serializer(self):
        return self.fields['fields']
