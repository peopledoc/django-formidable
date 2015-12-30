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

    def create(self, validated_data, field):
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
