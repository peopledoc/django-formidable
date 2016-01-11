# -*- coding: utf-8 -*-

import re

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from formidable.models import Validationidable
from formidable.register import ValidationSerializerRegister, load_serializer
from formidable.serializers.child_proxy import LazyChildProxy

validation_register = ValidationSerializerRegister.get_instance()


class ListValidationSerializer(serializers.ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy(validation_register)
        return super(ListValidationSerializer, self).__init__(*args, **kwargs)

    def create(self, field, validated_data):
        for data in validated_data:
            data['field_id'] = field.id
            self.child.create(data)

    def update(self, validations, field, validated_data,):
        validations.all().delete()
        for data in validated_data:
            data['field_id'] = field.id
            self.child.create(data)


class ValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Validationidable
        fields = ('type', 'value', 'message')
        list_serializer_class = ListValidationSerializer


class IntValueChecker(object):

    def validate_value(self, value):

        try:
            int(value)
        except ValueError:
            raise ValidationError('Must be an integer')

        return value


@load_serializer(validation_register)
class MinLengthSerializer(IntValueChecker, ValidationSerializer):

    type_id = u'minlength'


@load_serializer(validation_register)
class MaxLengthSerializer(IntValueChecker, ValidationSerializer):

    type_id = u'maxlength'


@load_serializer(validation_register)
class RegexpSerializer(ValidationSerializer):

    type_id = u'regexp'

    def validate_value(self, value):

        try:
            re.compile(value)
        except Exception, e:
            raise ValidationError(u'invalide regexp,  {}'.format(e))

        return value


@load_serializer(validation_register)
class EqualSerializer(ValidationSerializer):

    type_id = u'eq'


@load_serializer(validation_register)
class NotEqualSerializer(ValidationSerializer):

    type_id = u'neq'


@load_serializer(validation_register)
class GtSerializer(ValidationSerializer):

    type_id = u'gt'


@load_serializer(validation_register)
class GteSerializer(ValidationSerializer):

    type_id = u'gte'


@load_serializer(validation_register)
class LtSerializer(ValidationSerializer):

    type_id = u'lt'


@load_serializer(validation_register)
class LteSerializer(ValidationSerializer):

    type_id = u'lte'
