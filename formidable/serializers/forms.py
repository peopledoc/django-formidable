# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy
from collections import defaultdict

from django.conf import settings
from django.db import transaction

from formidable import constants, json_version
from formidable.forms import conditions
from formidable.models import Formidable
from formidable.serializers import fields
from formidable.serializers.common import WithNestedSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ConditionTestSerializer(serializers.Serializer):
    field_id = serializers.CharField(max_length=256, required=True)
    operator = serializers.ChoiceField(tuple(conditions.ConditionTest.mapper),
                                       required=True)
    values = serializers.ListField(
        child=serializers.JSONField(),
        allow_empty=False,
        required=True
    )


class ConditionSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    fields_ids = serializers.ListField(
        child=serializers.CharField(max_length=256),
        allow_empty=False,
        required=True
    )
    action = serializers.ChoiceField(tuple(conditions.conditions_register),
                                     required=True)
    tests = ConditionTestSerializer(
        many=True, allow_empty=False, required=True
    )


class FormidableSerializer(WithNestedSerializer):

    fields = fields.FieldSerializer(many=True)
    conditions = ConditionSerializer(many=True, required=False)

    nested_objects = ['fields']

    class Meta:
        model = Formidable
        fields = ('label', 'description', 'fields', 'id', 'conditions')
        depth = 2
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, data):
        """
        The validation step called by the condition validation.

        Since we cannot check if fields set up in conditions arguments exist
        inside the form itself, we must check this here.
        """
        # calling subserializer validate method (fields)
        data = super(FormidableSerializer, self).validate(data)
        # check every field define in conditions are defined inside the form
        if 'conditions' in data:
            data = self.check_conditions_cohesion(data)
        return data

    def create(self, validated_data):
        conditions = validated_data.pop('conditions', None)
        instance = super(FormidableSerializer, self).create(validated_data)
        if conditions:
            instance.conditions = conditions
            instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.conditions = validated_data.pop('conditions', None)
        instance = super(FormidableSerializer, self).update(
            instance, validated_data
        )
        return instance

    def _get_fields_slugs(self, data):
        return [field['slug'] for field in data.get('fields', [])]

    def get_field_type(self, data, field_id):
        return next(
            (
                f['type_id'] for f in data.get('fields', [])
                if f['slug'] == field_id
            )
        )

    def check_conditions_cohesion(self, data):
        # 1/ Check references to fields are valid
        fields_slug = self._get_fields_slugs(data)
        targets_action = defaultdict(list)

        condition_fields_allowed_types = getattr(
            settings, 'FORMIDABLE_CONDITION_FIELDS_ALLOWED_TYPES', []
        )
        index = 0
        for condition in data['conditions']:
            index += 1
            condition_name = condition.get('name') or '#{}'.format(index)
            missing_fields = []
            condition_fields_ids = []
            for field_id in condition['fields_ids']:
                targets_action[condition['action']].append(field_id)
                if field_id not in fields_slug:
                    missing_fields.append(field_id)
            for test in condition['tests']:
                field_id = test['field_id']
                condition_fields_ids.append(field_id)
                if field_id not in fields_slug:
                    missing_fields.append(field_id)

            if missing_fields:
                raise ValidationError(
                    'Condition ({name}) is using undefined fields ({ids})'.format(  # noqa
                        name=condition_name,
                        ids=', '.join(set(missing_fields))
                    )
                )
            # check field types are valid
            if condition_fields_allowed_types:
                for field_id in condition_fields_ids:
                    field_type = self.get_field_type(data, field_id)
                    if field_type not in condition_fields_allowed_types:
                        raise ValidationError(
                            'Condition ({name}) is using not allowed field type ({type})'.format(  # noqa
                                name=condition_name,
                                type=field_type
                            )
                        )
        return data

    def save(self, *args, **kwargs):
        with transaction.atomic():
            return super(FormidableSerializer, self).save(*args, **kwargs)


class ContextFormSerializer(serializers.ModelSerializer):

    fields = fields.ContextFieldSerializer(read_only=True, many=True)
    conditions = ConditionSerializer(read_only=True, many=True)

    class Meta:
        model = Formidable
        fields = ('id', 'label', 'description', 'fields', 'conditions')
        depth = 2

    def __init__(self, *args, **kwargs):
        super(ContextFormSerializer, self).__init__(*args, **kwargs)
        self.fields['fields'].set_context('role', self._context['role'])

    def to_representation(self, obj):
        data = super(ContextFormSerializer, self).to_representation(obj)
        data['version'] = json_version
        return data


def get_access(accesses, role):
    """
    Return the access' level for a given ``role``.

    """
    for access in accesses:
        if access['access_id'] == role:
            return access['level']
    return constants.EDITABLE  # default


def contextualize_fields(fields, role):
    """
    This method sets disabled/required attributes regarding the access
    level.

    """
    for field in fields:
        accesses = field.pop('accesses')
        access = get_access(accesses, role)
        if access == constants.HIDDEN:
            continue
        field['disabled'] = access == constants.READONLY
        field['required'] = access == constants.REQUIRED
        yield field


def contextualize_conditions(form):
    """
    Extract conditions and filter them using the fields that exist in the form.
    """
    # filter conditions by fields ids for current role
    field_ids = {field['slug'] for field in form['fields']}
    conditions = form.get('conditions', [])

    for condition in conditions:
        # Build the tests based on the existing fields in the form
        condition['tests'] = [
            t for t in condition['tests']
            if t['field_id'] in field_ids
        ]
        # Build the fields_ids based on the existing fields in the form.
        condition['fields_ids'] = list(
            set(condition.get('fields_ids', [])) & field_ids
        )
        # 1. If the condition "tests" is empty, remove it
        # 2. if the condition "fields_ids" is empty, remove it
        if condition['tests'] and condition['fields_ids']:
            yield condition


def contextualize(form, role):
    """
    Transform a FormidableJSON into a ContextFormJSON for a given role.

    """
    form = copy.deepcopy(form)
    form['fields'] = list(contextualize_fields(form['fields'], role))
    form['conditions'] = list(contextualize_conditions(form))
    return form
