# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from formidable.models import Formidable
from formidable.serializers import fields
from formidable.serializers.common import WithNestedSerializer
from formidable.serializers.presets import PresetModelSerializer
from rest_framework import serializers


class FormidableSerializer(WithNestedSerializer):

    fields = fields.FieldSerializer(many=True)
    presets = PresetModelSerializer(many=True, required=False)

    nested_objects = ['fields', 'presets']

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields', 'id', 'presets')
        depth = 2
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, data):
        """
        The validation step called by the preset validation.

        The preset validation ensures that presets are correctly defined
        and that defined arguments are correct.

        Since we cannot check if fields set up in preset arguments exist
        inside the form itself, we must check this here.
        """
        # calling subserializer validate method (fields, and presets)
        data = super(FormidableSerializer, self).validate(data)
        # we check every field define in presets are define inside the form.
        if 'fields' in data and 'presets' in data:
            data = self.check_presets_cohesion(data)
        return data

    def check_presets_cohesion(self, data):
        presets = data['presets']
        # validation already called on fields we are sur the slug is set
        # Samet thing for argument is presets
        fields_slug = [field['slug'] for field in data['fields']]

        for preset in presets:
            arguments = preset['arguments']
            for argument in arguments:
                field_id = argument.get('field_id')
                if field_id and field_id not in fields_slug:
                    raise ValidationError(
                        'Preset ({slug}) argument is using an undefined field ({id})'.format(  # noqa
                            slug=preset['slug'], id=field_id
                        )
                    )
        return data


class ContextFormSerializer(serializers.ModelSerializer):

    fields = fields.ContextFieldSerializer(read_only=True, many=True)
    presets = PresetModelSerializer(read_only=True, many=True)

    class Meta:
        model = Formidable
        fields = ('id', 'label', 'description', 'fields', 'presets')
        depth = 2

    def __init__(self, *args, **kwargs):
        super(ContextFormSerializer, self).__init__(*args, **kwargs)
        self.fields['fields'].set_context('role', self._context['role'])
