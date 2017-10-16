# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

logger = logging.getLogger(__name__)


class NestedListSerializer(ListSerializer):

    field_id = None
    parent_name = None

    def update(self, qs, parent, validated_data):
        created_ids, updated_ids, deleted_ids = self._extract_id(
            qs, validated_data
        )

        qs.filter(**{self.field_id + '__in': list(deleted_ids)}).delete()

        objects_list = list(qs.all())
        objects_list = sorted(objects_list,
                              key=lambda x: getattr(x, self.field_id))

        ajust = 0

        validated_data = sorted(validated_data, key=lambda x: x[self.field_id])

        for index, data in enumerate(validated_data):
            data[self.parent_name] = parent.id
            if data[self.field_id] in created_ids:
                self.child.create(data)
                ajust += 1
            else:
                self.child.update(objects_list[index - ajust], data)

    def create(self, parent, validated_data):

        for data in validated_data:
            data[self.parent_name] = parent.id
            self.child.create(data)

    def _extract_id(self, qs, validated_data):
        validated_ids = {data[self.field_id] for data in validated_data}
        db_ids = {values[0] for values in qs.values_list(self.field_id)}
        updated_ids = validated_ids & db_ids
        created_ids = validated_ids - db_ids
        deleted_ids = db_ids - validated_ids
        return created_ids, updated_ids, deleted_ids

    def validate(self, data):
        """
        ensure that field_id is unique among children
        """
        data = super(NestedListSerializer, self).validate(data)

        if self.field_id:
            if len(data) != len({f[self.field_id] for f in data}):
                msg = 'The fields {field_id} must make a unique set.'.format(
                    field_id=self.field_id
                )
                raise ValidationError(msg)

        return data


class NestedListSerializerDummyUpdate(NestedListSerializer):

    def update(self, qs, parent, validated_data):
        qs.all().delete()
        return self.create(parent, validated_data)
