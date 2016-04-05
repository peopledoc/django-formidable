# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.serializers import Serializer, ListSerializer
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import CharField
from rest_framework import fields


from formidable.models import Preset, PresetArg
from formidable.forms.validations.presets import presets_register
from formidable.serializers.list import NestedListSerializerDummyUpdate
from formidable.serializers.common import WithNestedSerializer


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


class PresetArgListSerializer(NestedListSerializerDummyUpdate):
    parent_name = 'preset_id'


class PresetArgModelSerializer(ModelSerializer):

    class Meta:
        model = PresetArg
        list_serializer_class = PresetArgListSerializer
        exclude = ('preset',)

    def validate(self, data):
        field_id = data.get('field_id')
        value = data.get('value')
        if field_id or value:
            return data
        raise ValidationError('field_id or value have to be filled.')


class PresetListSerializer(NestedListSerializerDummyUpdate):
    parent_name = 'form_id'


class PresetModelSerializer(WithNestedSerializer):

    preset_id = CharField(source='slug')
    fields = PresetArgModelSerializer(source='arguments', many=True)

    nested_objects = ['fields']

    class Meta:
        model = Preset
        list_serializer_class = PresetListSerializer
        exclude = ('form', 'slug')

    def validate(self, data):
        if not data.get('message'):
            data['message'] = presets_register[data['slug']].default_message
        return super(PresetModelSerializer, self).validate(data)

    def to_internal_value(self, data):
        return super(PresetModelSerializer, self).to_internal_value(data)
