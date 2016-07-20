# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six
from rest_framework import serializers


class WithNestedSerializer(serializers.ModelSerializer):

    nested_objects = []

    def create(self, validated_data):
        nested_data = self.extract_nested_data(validated_data)
        instance = super(WithNestedSerializer, self).create(validated_data)
        self.create_nested_objects(instance, nested_data)
        return instance

    def create_nested_objects(self, field, nested_data):
        for name, data in six.iteritems(nested_data):
            self.fields[name].create(field, nested_data[name])

    def update_nested_objects(self, field, nested_data):
        for name, data in six.iteritems(nested_data):
            self.fields[name].update(
                getattr(field, name), field, nested_data[name]
            )

    def extract_nested_data(self, data):
        """
        Extract the data from nested objects.

        By default, DRF will raise an execption when data for nested objects
        are found.

        Data are validated beforehand, so if nested_objects is required we are
        certain to have the data.
        """
        res = {}
        for nested_object_name in self.nested_objects:
            if nested_object_name in data:
                res[nested_object_name] = data.pop(nested_object_name)
        return res

    def update(self, instance, validated_data):
        nested_data = self.extract_nested_data(validated_data)
        instance = super(WithNestedSerializer, self).update(
            instance, validated_data
        )
        self.update_nested_objects(instance, nested_data)
        return instance
