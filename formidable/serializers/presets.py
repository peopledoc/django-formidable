# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.serializers import Serializer
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


class PresetsSerializer(Serializer):

    slug = SlugFieldClassAttr()
    label = CharFieldClassAttr()
    description = CharFieldClassAttr()
    message = CharFieldClassAttr(source='default_message')
