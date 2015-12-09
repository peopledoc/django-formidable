# -*- coding: utf-8 -*-

from rest_framework import serializers

from formidable.models import Formidable, Fieldidable


class FormidableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formidable
        fields = ('label', 'description')
        depth = 1


class FieldidableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fieldidable
        fields = ('label', 'description', 'type_id')
