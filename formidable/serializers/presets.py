# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.serializers import Serializer, ListSerializer
from rest_framework import fields


class ClassAttrSerializer(object):

    def get_attribute(self, instance):
        return super(ClassAttrSerializer, self).get_attribute(
            instance.__class__
        )


class CharFieldClassAttr(ClassAttrSerializer, fields.CharField):
    pass


class SlugFieldClassAttr(ClassAttrSerializer, fields.SlugField):
    pass


class ListField(fields.Field):

    def to_representation(self, value):
        return list(value)


class PresetArgsSerializerList(ListSerializer):

    def get_attribute(self, instance):
        return instance.__class__._declared_arguments.values()


class PresetsArgsSerializer(Serializer):

    class Meta:
        list_serializer_class = PresetArgsSerializerList

    slug = fields.SlugField()
    label = fields.CharField()
    help_text = fields.CharField(required=False)
    placehorlder = fields.CharField(required=False)
    types = ListField()


class PresetsSerializer(Serializer):

    slug = SlugFieldClassAttr()
    label = CharFieldClassAttr()
    description = CharFieldClassAttr()
    message = CharFieldClassAttr(source='default_message')
    fields = PresetsArgsSerializer(many=True)
