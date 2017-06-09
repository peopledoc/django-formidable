# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import Counter, defaultdict

from django.db import transaction

from formidable.models import Formidable
from formidable.serializers import fields
from formidable.serializers.common import WithNestedSerializer
from formidable.serializers.presets import PresetModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# TODO XXX pick choicefield values from formidable.conditions.*


class ConditionTestSerializer(serializers.Serializer):
    field_id = serializers.CharField(max_length=256, required=True)
    operator = serializers.ChoiceField(('eq',), required=True)
    values = serializers.ListField(
        child=serializers.CharField(max_length=256),
        allow_empty=False,
        required=True
    )


class ConditionSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    fields_ids = serializers.ListField(
        child=serializers.CharField(max_length=256),
        allow_empty=False,
        required=True
    )
    action = serializers.ChoiceField(('display_iff',), required=True)
    tests = ConditionTestSerializer(
        many=True, allow_empty=False, required=True
    )


class FormidableSerializer(WithNestedSerializer):

    fields = fields.FieldSerializer(many=True)
    presets = PresetModelSerializer(many=True, required=False)
    conditions = ConditionSerializer(many=True, required=False)

    nested_objects = ['fields', 'presets']

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields', 'id', 'presets',
                  'conditions')
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
        if 'presets' in data:
            data = self.check_presets_cohesion(data)
        if 'conditions' in data:
            data = self.check_conditions_cohesion(data)
        return data

    def create(self, validated_data):
        conditions = validated_data.pop('conditions', None)
        instance = super(FormidableSerializer, self).create(validated_data)
        instance.conditions = conditions
        return instance

    def update(self, instance, validated_data):
        conditions = validated_data.pop('conditions', None)
        instance = super(FormidableSerializer, self).update(
            instance, validated_data
        )
        instance.conditions = conditions
        return instance

    def _get_fields_slugs(self, data):
        return [field['slug'] for field in data.get('fields', None)]

    def check_conditions_cohesion(self, data):
        # 1/ Check references to fields are valid
        fields_slug = self._get_fields_slugs(data)
        targets_action = defaultdict(list)
        for condition in data['conditions']:
            missing_fields = []
            for field_id in condition['fields_ids']:
                targets_action[condition['action']].append(field_id)
                if field_id not in fields_slug:
                    missing_fields.append(field_id)
            for test in condition['tests']:
                field_id = test['field_id']
                if field_id not in fields_slug:
                    missing_fields.append(field_id)

            if missing_fields:
                raise ValidationError(
                    'Condition ({name}) is using undefined fields ({ids})'.format(  # noqa
                        name=condition['name'],
                        ids=', '.join(set(missing_fields))
                    )
                )

        # 2/ check there is no more than one rule on a field per action
        for action, fields_ids in targets_action.items():
            counter = Counter(fields_ids)
            duplicates = [
                field for field, count in counter.items()
                if count > 1
            ]
            if duplicates:
                raise ValidationError(
                    'Action {action} in condition ({name}) is used many times for the same fields ({ids})'.format(  # noqa
                        name=condition['name'],
                        action=action,
                        ids=', '.join(duplicates)
                    )
                )

        return data

    def check_presets_cohesion(self, data):
        # Check presets references to fields are valid
        presets = data['presets']
        fields_slug = self._get_fields_slugs(data)

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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            return super(FormidableSerializer, self).save(*args, **kwargs)


class ContextFormSerializer(serializers.ModelSerializer):

    fields = fields.ContextFieldSerializer(read_only=True, many=True)
    presets = PresetModelSerializer(read_only=True, many=True)
    conditions = ConditionSerializer(read_only=True, many=True)

    class Meta:
        model = Formidable
        fields = ('id', 'label', 'description', 'fields', 'presets',
                  'conditions')
        depth = 2

    def __init__(self, *args, **kwargs):
        super(ContextFormSerializer, self).__init__(*args, **kwargs)
        self.fields['fields'].set_context('role', self._context['role'])
