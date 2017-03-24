# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.forms.validations.presets import presets_register
from formidable.models import Preset, PresetArg
from formidable.serializers.child_proxy import LazyChildProxy
from formidable.serializers.common import WithNestedSerializer
from formidable.serializers.list import NestedListSerializerDummyUpdate
from rest_framework import fields
from rest_framework.serializers import (
    CharField, ListSerializer, ModelSerializer, Serializer, ValidationError
)


class PresetsArgsSerializerRegister(dict):

    lookup_field = 'has_items'

    def __init__(self):
        super(PresetsArgsSerializerRegister, self).__init__()
        self.update({
            True: PresetsArgSerializerWithItems,
            False: PresetsArgsSerializer
        })


class PresetArgsListSerializer(ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy(PresetsArgsSerializerRegister())
        super(PresetArgsListSerializer, self).__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return instance._declared_arguments.values()


class PresetsArgsSerializer(Serializer):

    class Meta:
        list_serializer_class = PresetArgsListSerializer

    slug = fields.SlugField()
    label = fields.CharField()
    description = fields.CharField(required=False, source='help_text')
    placehorlder = fields.CharField(required=False)
    types = fields.ListField()


class PresetsArgSerializerWithItems(PresetsArgsSerializer):

    items = fields.DictField()


class PresetsClassSerializer(Serializer):

    slug = fields.SlugField()
    label = fields.CharField()
    description = fields.CharField()
    message = fields.CharField(source='default_message')
    arguments = PresetsArgsSerializer(many=True)


class PresetArgModelListSerializer(NestedListSerializerDummyUpdate):
    parent_name = 'preset_id'


class PresetArgModelSerializer(ModelSerializer):

    class Meta:
        model = PresetArg
        list_serializer_class = PresetArgModelListSerializer
        exclude = ('preset',)

    def validate(self, data):
        field_id = data.get('field_id')
        value = data.get('value')
        if field_id or value:
            return data
        raise ValidationError('field_id or value have to be filled.')


class PresetListSerializer(NestedListSerializerDummyUpdate):
    parent_name = 'form_id'

    def get_attribute(self, instance):
        qs = super(PresetListSerializer, self).get_attribute(instance)
        qs = qs.prefetch_related('arguments')
        return qs


class PresetModelSerializer(WithNestedSerializer):

    preset_id = CharField(source='slug')
    arguments = PresetArgModelSerializer(many=True)

    nested_objects = ['arguments']

    class Meta:
        model = Preset
        list_serializer_class = PresetListSerializer
        exclude = ('form', 'slug')

    def validate_preset_id(self, slug):
        if slug not in presets_register.keys():
            raise ValidationError(
                '{slug} is not an available preset'.format(slug=slug)
            )
        return slug

    def validate(self, data):
        if not data.get('message'):
            data['message'] = presets_register[data['slug']].default_message
        return super(PresetModelSerializer, self).validate(data)
