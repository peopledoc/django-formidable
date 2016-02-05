# -*- coding: utf-8 -*-
import logging

from rest_framework.serializers import ListSerializer

logger = logging.getLogger(__name__)


class NestedListSerializer(ListSerializer):

    field_id = None
    parent_name = None

    def update(self, qs, field, validated_data):
        created_ids, updated_ids, deleted_ids = self._extract_id(
            qs, validated_data
        )

        qs.filter(**{self.field_id + '__in': list(deleted_ids)}).delete()

        objects_list = list(qs.order_by(self.field_id).all())

        ajust = 0

        validated_data = sorted(validated_data, key=lambda x: x[self.field_id])

        for index, data in enumerate(validated_data):

            data[self.parent_name] = field.id
            final_data = self.get_update_data(index, data)
            if data[self.field_id] in created_ids:
                self.child.create(final_data)
                ajust += 1
            else:
                self.child.update(objects_list[index-ajust], final_data)

    def get_update_data(self, index, data):
        return data

    def create(self, field, validated_data):

        for index, data in enumerate(validated_data):
            data[self.parent_name] = field.id
            self.child.create(self.get_create_data(index, data))

    def get_create_data(self, index, data):
        return data

    def _extract_id(self, qs, validated_data):
        validated_ids = set([data[self.field_id] for data in validated_data])
        db_ids = set([values[0] for values in qs.values_list(self.field_id)])
        updated_ids = validated_ids & db_ids
        created_ids = validated_ids - db_ids
        deleted_ids = db_ids - validated_ids
        return created_ids, updated_ids, deleted_ids
