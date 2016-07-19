# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six


def call_right_serializer_by_instance(meth):

    def _wrapper(self, instance, *args, **kwargs):

        type_id = getattr(instance, self.lookup_field)
        serializer = self.get_right_serializer(type_id)
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(instance, *args, **kwargs)

    return _wrapper


def call_right_serializer_by_attrs(meth):

    def _wrapper(self, attrs, *args, **kwargs):

        lookup = self.lookup_field
        serializer = self.get_right_serializer(attrs[lookup])
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(attrs, *args, **kwargs)

    return _wrapper


def call_all_serializer(meth):

    def _wrapper(self, *args, **kwargs):

        for serializer in self.get_all_serializer():
            meth_name = getattr(serializer, meth.__name__)
            return meth_name(*args, **kwargs)

    return _wrapper


class LazyChildProxy(object):

    def __init__(self, register):
        self.lookup_field = register.lookup_field
        self.register = {
            key: value() for key, value in six.iteritems(register)
        }

    def get_right_serializer(self, type_id):
        return self.register[type_id]

    def get_all_serializer(self):
        return [serializer for serializer in self.register.values()]

    @call_right_serializer_by_instance
    def to_representation(self, instance):
        pass

    @call_all_serializer
    def bind(self, *args, **kwargs):
        pass

    @call_right_serializer_by_attrs
    def run_validation(self):
        pass

    @call_right_serializer_by_attrs
    def create(self, attrs):
        pass

    @call_right_serializer_by_instance
    def update(self, instance, validated_data):
        pass
