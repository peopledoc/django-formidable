# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy

from django.core.exceptions import ValidationError

from formidable import constants
from formidable.models import Formidable
from formidable.register import FieldSerializerRegister
from formidable.serializers import fields
from formidable.serializers.common import WithNestedSerializer
from formidable.serializers.presets import PresetModelSerializer
from rest_framework import serializers

FIELD_TYPES = FieldSerializerRegister.get_instance().to_choices()
LEVELS = [(constants.REQUIRED, 'Required'), (constants.EDITABLE, 'Editable'),
          (constants.HIDDEN, 'Hidden'), (constants.READONLY, 'Readonly')]


def check_unicity(data, key):
    if len(data) != len(set(f[key] for f in data)):
        msg = 'The fields {key} must make a unique set.'.format(
            key=key
        )
        raise ValidationError(msg)


class MyDefaultSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=256)


class MyItemSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=256)
    label = serializers.CharField(max_length=256)
    description = serializers.CharField(allow_blank=True, allow_null=True)


class MyAccessSerializer(serializers.Serializer):
    access_id = serializers.CharField(max_length=128)
    level = serializers.ChoiceField(LEVELS)

    # TODO check access_id


class MyValidationSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=256)
    type = serializers.CharField(max_length=256)
    message = serializers.CharField(allow_blank=True, allow_null=True)


class MyFieldSerializer(serializers.Serializer):
    slug = serializers.CharField(max_length=256)
    label = serializers.CharField(max_length=256)
    type_id = serializers.ChoiceField(FIELD_TYPES)
    placeholder = serializers.CharField(
        max_length=256, allow_blank=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    multiple = serializers.BooleanField(default=False)

    defaults = MyDefaultSerializer(many=True)
    items = MyItemSerializer(many=True, required=False)
    accesses = MyAccessSerializer(many=True)  # unique_together access_id
    validations = MyValidationSerializer(many=True)

    def validate(self, validated_data):
        validated_data = super(MyFieldSerializer, self)\
                            .validate(validated_data)
        if 'items' in validated_data:
            check_unicity(validated_data['items'], 'value')
        return validated_data


class MyPresetArgSerializer(serializers.Serializer):
    slug = serializers.CharField(max_length=128)
    value = serializers.CharField(
        max_length=128, allow_blank=True, allow_null=True)
    field_id = serializers.CharField(
        max_length=128, allow_blank=True, allow_null=True)


class MyPresetSerializer(serializers.Serializer):
    slug = serializers.CharField(max_length=256)
    message = serializers.CharField(allow_blank=True, allow_null=True)
    arguments = MyPresetArgSerializer(many=True)


class MyFormidableSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=256)
    description = serializers.CharField()

    fields = MyFieldSerializer(many=True)
    presets = MyPresetSerializer(many=True, required=False)

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

        if 'fields' in data:
            check_unicity(data['fields'], 'slug')

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


# How to create a context form from a form :
# replace accesses by :
#  - disabled = access.level == READONLY
#  - required = access.level == REQUIRED
#  - filter Field if access.level == HIDDEN
def get_acccess(accesses, role):
    for a in accesses:
        if a['access_id'] == role:
            return a['level']
    return constants.EDITABLE  # default


def context_fields(fields, role):
    for field in fields:
        accesses = field.pop('accesses')
        access = get_acccess(accesses, role)
        if access == constants.HIDDEN:
            continue
        field['disabled'] = access == constants.READONLY
        field['required'] = access == constants.REQUIRED
        yield field


def contextualize(form, role):
    form = copy.deepcopy(form)
    form['fields'] = list(context_fields(form['fields'], role))
    return form


def get_access_from_context_field(field):
    if field is None:
        return constants.HIDDEN
    if field['disabled']:
        return constants.READONLY
    if field['required']:
        return constants.REQUIRED
    return constants.EDITABLE


def uncontextualize_field(field):
    new_field = field.copy()  # deepcopy useless ?
    del new_field['disabled']
    del new_field['required']
    new_field['accesses'] = {}
    return new_field['slug']


def add_fields(ref_fields, new_fields):
    current_field = 0

    for field in new_fields:
        if field in ref_fields:
            # no need to insert a new field, just move the cursor
            current_field = ref_fields.index(field) + 1
        else:
            # we need to insert field at the right position
            ref_fields.insert(field)
            current_field += 1


def merge_context_forms(forms):
    # forms : role => ContextForm
    roles = forms.keys()
    fields = [uncontextualize_field(field) for field in forms[roles[0]]]

    for role in roles[1:]:
        add_fields(fields,
                   [uncontextualize_field(field) for field in forms[roles]])
    # print forms
    # print fields


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
