# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

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

        objects_list = list(qs.order_by(self.field_id).all())

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
        validated_ids = set([data[self.field_id] for data in validated_data])
        db_ids = set([values[0] for values in qs.values_list(self.field_id)])
        updated_ids = validated_ids & db_ids
        created_ids = validated_ids - db_ids
        deleted_ids = db_ids - validated_ids
        return created_ids, updated_ids, deleted_ids


class NestedListSerializerDummyUpdate(NestedListSerializer):

    def update(self, qs, parent, validated_data):
        qs.all().delete()
        return self.create(parent, validated_data)
