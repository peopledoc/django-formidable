# -*- coding: utf-8 -*-

import re

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from formidable.models import Validation
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
        model = Validation
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

    type_id = u'MINLENGTH'


@load_serializer(validation_register)
class MaxLengthSerializer(IntValueChecker, ValidationSerializer):

    type_id = u'MAXLENGTH'


@load_serializer(validation_register)
class RegexpSerializer(ValidationSerializer):

    type_id = u'REGEXP'

    def validate_value(self, value):

        try:
            re.compile(value)
        except Exception as e:
            raise ValidationError(u'invalide regexp,  {}'.format(e))

        return value


@load_serializer(validation_register)
class EqualSerializer(ValidationSerializer):

    type_id = u'EQ'


@load_serializer(validation_register)
class NotEqualSerializer(ValidationSerializer):

    type_id = u'NEQ'


@load_serializer(validation_register)
class GtSerializer(ValidationSerializer):

    type_id = u'GT'


@load_serializer(validation_register)
class GteSerializer(ValidationSerializer):

    type_id = u'GTE'


@load_serializer(validation_register)
class LtSerializer(ValidationSerializer):

    type_id = u'LT'


@load_serializer(validation_register)
class LteSerializer(ValidationSerializer):

    type_id = u'LTE'


@load_serializer(validation_register)
class AgeAboveSerializer(IntValueChecker, ValidationSerializer):

    type_id = u'IS_AGE_ABOVE'


@load_serializer(validation_register)
class AgeUnderSerializer(IntValueChecker, ValidationSerializer):

    type_id = u'IS_AGE_UNDER'


@load_serializer(validation_register)
class FutureDateSerializer(ValidationSerializer):

    type_id = u'IS_DATE_IN_THE_FUTURE'

    def validate_value(self, value):
        if value in ['t', "true"]:
            return "true"
        else:
            return "false"
